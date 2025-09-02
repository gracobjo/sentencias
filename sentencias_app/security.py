"""
Módulo de seguridad para uploads de archivos
Implementa validación robusta, sanitización y verificación de archivos
"""

import os
import re
import hashlib
import mimetypes
from pathlib import Path
from typing import List, Optional, Tuple
from fastapi import HTTPException, UploadFile
import magic
import logging

logger = logging.getLogger(__name__)

# Configuración de seguridad
ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.doc', '.docx'}
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'text/plain',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_FILENAME_LENGTH = 255
UPLOAD_DIR = Path("uploads")
SECURE_UPLOAD_DIR = UPLOAD_DIR / "secure"

class FileSecurityError(Exception):
    """Excepción personalizada para errores de seguridad de archivos"""
    pass

class FileValidator:
    """Validador de archivos con múltiples capas de seguridad"""
    
    def __init__(self):
        self.ensure_secure_directories()
    
    def ensure_secure_directories(self):
        """Crear directorios seguros para uploads"""
        try:
            SECURE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            # Establecer permisos restrictivos
            os.chmod(SECURE_UPLOAD_DIR, 0o755)
            logger.info(f"Directorio seguro creado: {SECURE_UPLOAD_DIR}")
        except Exception as e:
            logger.error(f"Error creando directorio seguro: {e}")
            raise FileSecurityError(f"No se pudo crear directorio seguro: {e}")
    
    def validate_file_size(self, file: UploadFile) -> bool:
        """Validar tamaño del archivo"""
        try:
            # Leer el archivo para obtener su tamaño real
            content = file.file.read()
            file.file.seek(0)  # Resetear posición
            
            if len(content) > MAX_FILE_SIZE:
                raise FileSecurityError(
                    f"Archivo demasiado grande. Máximo permitido: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
                )
            return True
        except Exception as e:
            logger.error(f"Error validando tamaño: {e}")
            raise FileSecurityError(f"Error validando tamaño del archivo: {e}")
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitizar nombre de archivo para prevenir path traversal"""
        if not filename:
            raise FileSecurityError("Nombre de archivo vacío")
        
        # Remover caracteres peligrosos
        dangerous_chars = r'[<>:"/\\|?*\x00-\x1f]'
        sanitized = re.sub(dangerous_chars, '_', filename)
        
        # Remover puntos al inicio (path traversal)
        sanitized = sanitized.lstrip('.')
        
        # Limitar longitud
        if len(sanitized) > MAX_FILENAME_LENGTH:
            name, ext = os.path.splitext(sanitized)
            sanitized = name[:MAX_FILENAME_LENGTH-len(ext)] + ext
        
        # Asegurar que no esté vacío después de sanitización
        if not sanitized or sanitized == '_':
            sanitized = f"archivo_{hashlib.md5(filename.encode()).hexdigest()[:8]}"
        
        return sanitized
    
    def validate_file_extension(self, filename: str) -> bool:
        """Validar extensión del archivo"""
        if not filename:
            return False
        
        ext = Path(filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise FileSecurityError(
                f"Extensión no permitida: {ext}. Permitidas: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        return True
    
    def validate_mime_type(self, file: UploadFile) -> bool:
        """Validar tipo MIME del archivo"""
        try:
            # Leer los primeros bytes para detectar MIME
            content = file.file.read(1024)
            file.file.seek(0)  # Resetear posición
            
            # Detectar MIME type real
            mime_type = magic.from_buffer(content, mime=True)
            
            if mime_type not in ALLOWED_MIME_TYPES:
                raise FileSecurityError(
                    f"Tipo MIME no permitido: {mime_type}. Permitidos: {', '.join(ALLOWED_MIME_TYPES)}"
                )
            
            # Verificar que el MIME coincida con la extensión
            expected_mime = mimetypes.guess_type(file.filename)[0]
            if expected_mime and expected_mime != mime_type:
                logger.warning(f"MIME mismatch: expected {expected_mime}, got {mime_type}")
            
            return True
        except Exception as e:
            logger.error(f"Error validando MIME type: {e}")
            raise FileSecurityError(f"Error validando tipo de archivo: {e}")
    
    def scan_for_malicious_content(self, file: UploadFile) -> bool:
        """Escanear contenido en busca de patrones maliciosos"""
        try:
            content = file.file.read()
            file.file.seek(0)  # Resetear posición
            
            # Patrones maliciosos comunes
            malicious_patterns = [
                rb'<script[^>]*>',
                rb'javascript:',
                rb'vbscript:',
                rb'onload\s*=',
                rb'onerror\s*=',
                rb'<iframe[^>]*>',
                rb'<object[^>]*>',
                rb'<embed[^>]*>',
                rb'<link[^>]*>',
                rb'<meta[^>]*>',
            ]
            
            content_lower = content.lower()
            for pattern in malicious_patterns:
                if re.search(pattern, content_lower):
                    raise FileSecurityError(
                        f"Contenido potencialmente malicioso detectado: {pattern.decode()}"
                    )
            
            return True
        except Exception as e:
            if isinstance(e, FileSecurityError):
                raise
            logger.error(f"Error escaneando contenido: {e}")
            raise FileSecurityError(f"Error escaneando archivo: {e}")
    
    def generate_secure_filename(self, original_filename: str) -> str:
        """Generar nombre de archivo seguro único"""
        sanitized = self.sanitize_filename(original_filename)
        
        # Añadir timestamp y hash para unicidad
        import time
        timestamp = int(time.time())
        hash_suffix = hashlib.md5(f"{original_filename}{timestamp}".encode()).hexdigest()[:8]
        
        name, ext = os.path.splitext(sanitized)
        return f"{name}_{timestamp}_{hash_suffix}{ext}"
    
    def validate_file(self, file: UploadFile) -> Tuple[str, str]:
        """
        Validar archivo completo y retornar nombre seguro y ruta
        Retorna: (nombre_seguro, ruta_completa)
        """
        try:
            # Validaciones básicas
            if not file.filename:
                raise FileSecurityError("Nombre de archivo no proporcionado")
            
            # Validar extensión
            self.validate_file_extension(file.filename)
            
            # Validar tamaño
            self.validate_file_size(file)
            
            # Validar MIME type
            self.validate_mime_type(file)
            
            # Escanear contenido
            self.scan_for_malicious_content(file)
            
            # Generar nombre seguro
            secure_filename = self.generate_secure_filename(file.filename)
            secure_path = SECURE_UPLOAD_DIR / secure_filename
            
            logger.info(f"Archivo validado exitosamente: {file.filename} -> {secure_filename}")
            return secure_filename, str(secure_path)
            
        except Exception as e:
            logger.error(f"Error validando archivo {file.filename}: {e}")
            raise FileSecurityError(f"Error de validación: {e}")
    
    def save_secure_file(self, file: UploadFile, secure_path: str) -> bool:
        """Guardar archivo de forma segura"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(secure_path), exist_ok=True)
            
            # Escribir archivo
            with open(secure_path, "wb") as f:
                content = file.file.read()
                f.write(content)
            
            # Establecer permisos restrictivos
            os.chmod(secure_path, 0o644)
            
            logger.info(f"Archivo guardado de forma segura: {secure_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error guardando archivo: {e}")
            raise FileSecurityError(f"Error guardando archivo: {e}")

# Instancia global del validador
file_validator = FileValidator()

def validate_and_save_file(file: UploadFile) -> Tuple[str, str]:
    """
    Función de conveniencia para validar y guardar archivo
    Retorna: (nombre_seguro, ruta_completa)
    """
    secure_filename, secure_path = file_validator.validate_file(file)
    file_validator.save_secure_file(file, secure_path)
    return secure_filename, secure_path

def get_file_info(file_path: str) -> dict:
    """Obtener información de un archivo guardado"""
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileSecurityError("Archivo no encontrado")
        
        stat = path.stat()
        return {
            "filename": path.name,
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "is_secure": str(path).startswith(str(SECURE_UPLOAD_DIR))
        }
    except Exception as e:
        logger.error(f"Error obteniendo info del archivo: {e}")
        raise FileSecurityError(f"Error obteniendo información: {e}")

def cleanup_old_files(max_age_days: int = 30):
    """Limpiar archivos antiguos del directorio seguro"""
    try:
        import time
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 60 * 60
        
        for file_path in SECURE_UPLOAD_DIR.iterdir():
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    file_path.unlink()
                    logger.info(f"Archivo antiguo eliminado: {file_path}")
    except Exception as e:
        logger.error(f"Error limpiando archivos antiguos: {e}")
