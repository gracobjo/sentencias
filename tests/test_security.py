"""
Tests para el módulo de seguridad
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import tempfile
import shutil
from sentencias_app.security import (
    FileValidator, 
    FileSecurityError, 
    validate_and_save_file,
    get_file_info,
    cleanup_old_files
)

class TestFileValidator:
    """Tests para FileValidator"""
    
    def test_validate_file_size_valid(self, file_validator_instance, mock_upload_file):
        """Test validación de tamaño válido"""
        # Mock del contenido del archivo
        mock_upload_file.file.read.return_value = b"x" * 1024  # 1KB
        mock_upload_file.file.seek.return_value = None
        
        result = file_validator_instance.validate_file_size(mock_upload_file)
        assert result is True
    
    def test_validate_file_size_too_large(self, file_validator_instance, mock_upload_file):
        """Test validación de tamaño demasiado grande"""
        # Mock del contenido del archivo (más de 50MB)
        mock_upload_file.file.read.return_value = b"x" * (51 * 1024 * 1024)
        mock_upload_file.file.seek.return_value = None
        
        with pytest.raises(FileSecurityError, match="Archivo demasiado grande"):
            file_validator_instance.validate_file_size(mock_upload_file)
    
    def test_sanitize_filename_valid(self, file_validator_instance):
        """Test sanitización de nombre válido"""
        result = file_validator_instance.sanitize_filename("documento.pdf")
        assert result == "documento.pdf"
    
    def test_sanitize_filename_dangerous_chars(self, file_validator_instance):
        """Test sanitización de caracteres peligrosos"""
        result = file_validator_instance.sanitize_filename("doc<>:\"/\\|?*.pdf")
        assert result == "doc___________.pdf"
    
    def test_sanitize_filename_path_traversal(self, file_validator_instance):
        """Test sanitización contra path traversal"""
        result = file_validator_instance.sanitize_filename("../../../etc/passwd")
        assert result == "etc_passwd"
    
    def test_sanitize_filename_empty(self, file_validator_instance):
        """Test sanitización de nombre vacío"""
        with pytest.raises(FileSecurityError, match="Nombre de archivo vacío"):
            file_validator_instance.sanitize_filename("")
    
    def test_validate_file_extension_valid(self, file_validator_instance):
        """Test validación de extensión válida"""
        result = file_validator_instance.validate_file_extension("documento.pdf")
        assert result is True
    
    def test_validate_file_extension_invalid(self, file_validator_instance):
        """Test validación de extensión inválida"""
        with pytest.raises(FileSecurityError, match="Extensión no permitida"):
            file_validator_instance.validate_file_extension("documento.exe")
    
    def test_validate_mime_type_valid(self, file_validator_instance, mock_upload_file):
        """Test validación de MIME type válido"""
        # Mock del contenido PDF
        mock_upload_file.file.read.return_value = b"%PDF-1.4\nTest content"
        mock_upload_file.file.seek.return_value = None
        
        with patch('sentencias_app.security.magic.from_buffer', return_value='application/pdf'):
            result = file_validator_instance.validate_mime_type(mock_upload_file)
            assert result is True
    
    def test_validate_mime_type_invalid(self, file_validator_instance, mock_upload_file):
        """Test validación de MIME type inválido"""
        mock_upload_file.file.read.return_value = b"fake content"
        mock_upload_file.file.seek.return_value = None
        
        with patch('sentencias_app.security.magic.from_buffer', return_value='application/octet-stream'):
            with pytest.raises(FileSecurityError, match="Tipo MIME no permitido"):
                file_validator_instance.validate_mime_type(mock_upload_file)
    
    def test_scan_for_malicious_content_clean(self, file_validator_instance, mock_upload_file):
        """Test escaneo de contenido limpio"""
        mock_upload_file.file.read.return_value = b"Este es un documento legal limpio."
        mock_upload_file.file.seek.return_value = None
        
        result = file_validator_instance.scan_for_malicious_content(mock_upload_file)
        assert result is True
    
    def test_scan_for_malicious_content_script(self, file_validator_instance, mock_upload_file):
        """Test escaneo de contenido con script malicioso"""
        mock_upload_file.file.read.return_value = b"<script>alert('xss')</script>"
        mock_upload_file.file.seek.return_value = None
        
        with pytest.raises(FileSecurityError, match="Contenido potencialmente malicioso"):
            file_validator_instance.scan_for_malicious_content(mock_upload_file)
    
    def test_generate_secure_filename(self, file_validator_instance):
        """Test generación de nombre seguro"""
        result = file_validator_instance.generate_secure_filename("documento.pdf")
        assert result.endswith(".pdf")
        assert "documento" in result
        assert len(result) > len("documento.pdf")  # Debe incluir timestamp y hash
    
    def test_validate_file_complete_success(self, file_validator_instance, mock_upload_file, temp_dir):
        """Test validación completa exitosa"""
        # Configurar mock para validación exitosa
        mock_upload_file.file.read.return_value = b"%PDF-1.4\nTest content"
        mock_upload_file.file.seek.return_value = None
        
        with patch('sentencias_app.security.magic.from_buffer', return_value='application/pdf'):
            with patch('sentencias_app.security.SECURE_UPLOAD_DIR', temp_dir):
                filename, path = file_validator_instance.validate_file(mock_upload_file)
                assert filename.endswith(".pdf")
                assert path.startswith(str(temp_dir))
    
    def test_validate_file_complete_failure(self, file_validator_instance, mock_upload_file):
        """Test validación completa con fallo"""
        # Configurar mock para fallo en validación
        mock_upload_file.file.read.return_value = b"fake content"
        mock_upload_file.file.seek.return_value = None
        
        with patch('sentencias_app.security.magic.from_buffer', return_value='application/octet-stream'):
            with pytest.raises(FileSecurityError):
                file_validator_instance.validate_file(mock_upload_file)

class TestSecurityFunctions:
    """Tests para funciones de seguridad"""
    
    def test_validate_and_save_file_success(self, mock_upload_file, temp_dir):
        """Test función validate_and_save_file exitosa"""
        mock_upload_file.file.read.return_value = b"%PDF-1.4\nTest content"
        mock_upload_file.file.seek.return_value = None
        
        with patch('sentencias_app.security.magic.from_buffer', return_value='application/pdf'):
            with patch('sentencias_app.security.SECURE_UPLOAD_DIR', temp_dir):
                filename, path = validate_and_save_file(mock_upload_file)
                assert filename.endswith(".pdf")
                assert Path(path).exists()
    
    def test_get_file_info(self, temp_dir):
        """Test función get_file_info"""
        test_file = temp_dir / "test.pdf"
        test_file.write_bytes(b"test content")
        
        info = get_file_info(str(test_file))
        assert info["filename"] == "test.pdf"
        assert info["size"] == len(b"test content")
        assert "created" in info
        assert "modified" in info
        assert info["is_secure"] is True
    
    def test_get_file_info_nonexistent(self):
        """Test función get_file_info con archivo inexistente"""
        with pytest.raises(FileSecurityError, match="Archivo no encontrado"):
            get_file_info("/path/to/nonexistent/file.pdf")
    
    def test_cleanup_old_files(self, temp_dir):
        """Test función cleanup_old_files"""
        # Crear archivo antiguo
        old_file = temp_dir / "old_file.pdf"
        old_file.write_bytes(b"old content")
        
        # Simular archivo antiguo modificando timestamp
        import time
        old_timestamp = time.time() - (31 * 24 * 60 * 60)  # 31 días atrás
        os.utime(old_file, (old_timestamp, old_timestamp))
        
        with patch('sentencias_app.security.SECURE_UPLOAD_DIR', temp_dir):
            cleanup_old_files(max_age_days=30)
            assert not old_file.exists()
    
    def test_cleanup_old_files_recent(self, temp_dir):
        """Test función cleanup_old_files con archivo reciente"""
        # Crear archivo reciente
        recent_file = temp_dir / "recent_file.pdf"
        recent_file.write_bytes(b"recent content")
        
        with patch('sentencias_app.security.SECURE_UPLOAD_DIR', temp_dir):
            cleanup_old_files(max_age_days=30)
            assert recent_file.exists()  # No debe eliminarse
