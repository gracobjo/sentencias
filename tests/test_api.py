"""
Tests para endpoints de la API
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import json

class TestAPIEndpoints:
    """Tests para endpoints de la API"""
    
    def test_health_endpoint(self, client):
        """Test del endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"
        assert "timestamp" in data
    
    def test_documentos_endpoint(self, client):
        """Test del endpoint de documentos"""
        response = client.get("/api/documentos")
        assert response.status_code == 200
        data = response.json()
        assert "documentos" in data
        assert isinstance(data["documentos"], list)
    
    def test_frases_clave_endpoint(self, client):
        """Test del endpoint de frases clave"""
        response = client.get("/api/frases-clave")
        assert response.status_code == 200
        data = response.json()
        assert "frases_clave" in data
        assert isinstance(data["frases_clave"], dict)
    
    def test_analisis_predictivo_endpoint(self, client):
        """Test del endpoint de análisis predictivo"""
        with patch('sentencias_app.main.ANALIZADOR_IA_DISPONIBLE', True):
            response = client.get("/api/analisis-predictivo")
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert "analisis_predictivo" in data
            assert "insights_juridicos" in data
    
    def test_upload_endpoint_success(self, client, sample_pdf_file):
        """Test del endpoint de upload exitoso"""
        with open(sample_pdf_file, "rb") as f:
            files = {"file": ("test.pdf", f, "application/pdf")}
            data = {
                "document_type": "sentencia",
                "extract_entities": "true",
                "analyze_arguments": "true"
            }
            
            with patch('sentencias_app.main.ANALIZADOR_IA_DISPONIBLE', False):
                response = client.post("/upload", files=files, data=data)
                assert response.status_code == 200
                result = response.json()
                assert "resultado" in result
                assert "nombre_archivo" in result
    
    def test_upload_endpoint_invalid_file(self, client):
        """Test del endpoint de upload con archivo inválido"""
        # Crear archivo con extensión no permitida
        files = {"file": ("test.exe", b"fake content", "application/octet-stream")}
        data = {"document_type": "sentencia"}
        
        response = client.post("/upload", files=files, data=data)
        assert response.status_code == 400
        assert "Error de seguridad" in response.json()["detail"]
    
    def test_upload_endpoint_no_file(self, client):
        """Test del endpoint de upload sin archivo"""
        response = client.post("/upload")
        assert response.status_code == 422  # Validation error
    
    def test_analisis_documento_endpoint(self, client, sample_txt_file):
        """Test del endpoint de análisis de documento"""
        with patch('sentencias_app.main.ANALIZADOR_IA_DISPONIBLE', False):
            response = client.post(
                "/api/analizar",
                json={"ruta_archivo": str(sample_txt_file)}
            )
            assert response.status_code == 200
            data = response.json()
            assert "resultado" in data
            assert "frases_clave" in data["resultado"]
    
    def test_analisis_documento_endpoint_invalid_file(self, client):
        """Test del endpoint de análisis con archivo inexistente"""
        response = client.post(
            "/api/analizar",
            json={"ruta_archivo": "/path/to/nonexistent/file.pdf"}
        )
        assert response.status_code == 400
        assert "No se pudo leer el archivo" in response.json()["detail"]
    
    def test_generar_demanda_endpoint(self, client):
        """Test del endpoint de generación de demanda"""
        with patch('sentencias_app.main.ANALIZADOR_IA_DISPONIBLE', False):
            response = client.post(
                "/api/demanda-base/txt",
                json={
                    "documentos": ["test1.pdf", "test2.pdf"],
                    "metadatos": {
                        "nombre": "Juan Pérez",
                        "dni": "12345678A",
                        "grado_principal": "IPP"
                    }
                }
            )
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/plain; charset=utf-8"
    
    def test_extract_metadatos_endpoint(self, client):
        """Test del endpoint de extracción de metadatos"""
        response = client.post(
            "/api/extract/demanda",
            json={"documentos": ["test1.pdf", "test2.pdf"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert "sugerencias" in data
        assert "metadatos" in data
    
    def test_cors_headers(self, client):
        """Test de headers CORS"""
        response = client.options("/api/documentos")
        assert response.status_code == 200
        # CORS headers deberían estar configurados en la app
    
    def test_api_error_handling(self, client):
        """Test de manejo de errores en API"""
        # Test con endpoint inexistente
        response = client.get("/api/endpoint-inexistente")
        assert response.status_code == 404
    
    def test_api_response_format(self, client):
        """Test del formato de respuesta de la API"""
        response = client.get("/api/documentos")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        
        # Verificar que la respuesta es JSON válido
        data = response.json()
        assert isinstance(data, dict)
    
    def test_analisis_predictivo_with_ia(self, client):
        """Test del análisis predictivo con IA disponible"""
        with patch('sentencias_app.main.ANALIZADOR_IA_DISPONIBLE', True):
            with patch('sentencias_app.main.AnalizadorLegal') as mock_analizador:
                mock_instance = Mock()
                mock_instance.analizar_documento.return_value = {
                    "frases_clave": ["test"],
                    "categorias": ["ipp"],
                    "confianza": 0.9
                }
                mock_analizador.return_value = mock_instance
                
                response = client.get("/api/analisis-predictivo")
                assert response.status_code == 200
                data = response.json()
                assert data["metadata"]["modelo_ia"] is True
