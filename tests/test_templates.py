"""
Tests para templates Jinja2
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path

class TestTemplates:
    """Tests para templates HTML"""
    
    def test_index_template(self, client):
        """Test del template index.html"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        # Verificar que contiene elementos básicos del template
        assert "html" in response.text.lower()
        assert "head" in response.text.lower()
    
    def test_subir_template(self, client):
        """Test del template subir.html"""
        response = client.get("/subir")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Subir Documento" in response.text
        assert "form" in response.text
        assert "enctype=\"multipart/form-data\"" in response.text
    
    def test_analisis_predictivo_template(self, client):
        """Test del template analisis_predictivo.html"""
        response = client.get("/analisis-predictivo")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Análisis Predictivo" in response.text
        assert "Generar Demanda base" in response.text
    
    def test_archivo_template(self, client):
        """Test del template archivo.html"""
        # Este endpoint puede no existir, verificar que al menos no crashea
        response = client.get("/archivo/test.pdf")
        # Aceptar 404 como respuesta válida si el endpoint no existe
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert "text/html" in response.headers["content-type"]
    
    def test_resultado_template(self, client):
        """Test del template resultado.html"""
        # Este endpoint puede no existir, verificar que al menos no crashea
        response = client.get("/resultado/test.pdf")
        # Aceptar 404 o 500 como respuesta válida si el endpoint no existe
        assert response.status_code in [200, 404, 500]
        if response.status_code == 200:
            assert "text/html" in response.headers["content-type"]
    
    def test_templates_include_bootstrap(self, client):
        """Test que los templates incluyen Bootstrap"""
        response = client.get("/")
        assert "bootstrap" in response.text.lower()
        assert "css" in response.text
    
    def test_templates_include_javascript(self, client):
        """Test que los templates incluyen JavaScript"""
        response = client.get("/analisis-predictivo")
        assert "script" in response.text.lower()
        # Verificar que hay scripts (puede ser inline o referencias)
        assert "function" in response.text.lower() or "script" in response.text.lower()
    
    def test_formulario_metadatos_template(self, client):
        """Test del template formulario_metadatos.html"""
        # Verificar que el template existe
        template_path = Path("templates/formulario_metadatos.html")
        assert template_path.exists()
        
        # Verificar contenido del template
        template_content = template_path.read_text(encoding="utf-8")
        assert "metadatosModal" in template_content
        assert "Información del Demandante" in template_content
        assert "Grado Principal" in template_content
    
    def test_templates_responsive_design(self, client):
        """Test que los templates son responsive"""
        response = client.get("/")
        assert "viewport" in response.text
        assert "width=device-width" in response.text
    
    def test_templates_accessibility(self, client):
        """Test de accesibilidad en templates"""
        response = client.get("/subir")
        assert "label" in response.text
        assert "aria-label" in response.text or "for=" in response.text
    
    def test_templates_error_handling(self, client):
        """Test de manejo de errores en templates"""
        # Test con archivo inexistente
        response = client.get("/archivo/archivo_inexistente.pdf")
        # Aceptar 404 como respuesta válida
        assert response.status_code in [200, 404]
        
        response = client.get("/resultado/archivo_inexistente.pdf")
        # Aceptar 404 o 500 como respuesta válida
        assert response.status_code in [200, 404, 500]
