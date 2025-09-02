"""
Configuración de pytest y fixtures para tests
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sentencias_app.main import app
from sentencias_app.security import FileValidator

@pytest.fixture
def client():
    """Cliente de prueba para FastAPI"""
    return TestClient(app)

@pytest.fixture
def temp_dir():
    """Directorio temporal para tests"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)

@pytest.fixture
def sample_pdf_file(temp_dir):
    """Archivo PDF de muestra para tests"""
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n174\n%%EOF"
    pdf_path = temp_dir / "test_document.pdf"
    pdf_path.write_bytes(pdf_content)
    return pdf_path

@pytest.fixture
def sample_txt_file(temp_dir):
    """Archivo TXT de muestra para tests"""
    txt_content = "Este es un documento de prueba para análisis legal.\nContiene información sobre incapacidad permanente."
    txt_path = temp_dir / "test_document.txt"
    txt_path.write_text(txt_content, encoding="utf-8")
    return txt_path

@pytest.fixture
def mock_analizador_ia():
    """Mock del analizador de IA"""
    mock = Mock()
    mock.analizar_documento.return_value = {
        "frases_clave": ["incapacidad permanente", "análisis legal"],
        "categorias": ["ipp", "inss"],
        "confianza": 0.85,
        "modelo_ia": True
    }
    return mock

@pytest.fixture
def mock_analizador_basico():
    """Mock del analizador básico"""
    mock = Mock()
    mock.analizar_documento.return_value = {
        "frases_clave": ["incapacidad permanente"],
        "categorias": ["ipp"],
        "confianza": 0.60,
        "modelo_ia": False
    }
    return mock

@pytest.fixture
def file_validator_instance():
    """Instancia del validador de archivos para tests"""
    return FileValidator()

@pytest.fixture
def mock_upload_file():
    """Mock de UploadFile para tests"""
    mock_file = Mock()
    mock_file.filename = "test_document.pdf"
    mock_file.content_type = "application/pdf"
    mock_file.file.read.return_value = b"%PDF-1.4\nTest content"
    mock_file.file.seek.return_value = None
    return mock_file

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Configurar entorno de prueba"""
    # Variables de entorno para tests
    os.environ["ENVIRONMENT"] = "test"
    os.environ["SECRET_KEY"] = "test_secret_key"
    
    # Crear directorios necesarios
    test_dirs = ["uploads", "uploads/secure", "sentencias", "models", "logs"]
    for dir_name in test_dirs:
        Path(dir_name).mkdir(exist_ok=True)
    
    yield
    
    # Limpiar después de los tests
    for dir_name in test_dirs:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name, ignore_errors=True)

@pytest.fixture
def sample_frases_clave():
    """Datos de frases clave de muestra"""
    return {
        "ipp": {
            "frases": ["incapacidad permanente parcial", "IPP"],
            "total": 2
        },
        "inss": {
            "frases": ["instituto nacional", "INSS"],
            "total": 2
        }
    }
