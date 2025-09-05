#!/usr/bin/env python3
"""
Script para probar la conectividad con Jira
"""
import requests
import base64

# Configuración
EMAIL = "gracobjo@gmail.com"
API_TOKEN = "YOUR_API_TOKEN_HERE"

# URLs a probar
URLS_TO_TEST = [
    "https://gracobjo.atlassian.net",
    "https://gracobjo.atlassian.com",
    "https://atlassian.net",
    "https://atlassian.com"
]

def test_connection(base_url):
    """Probar conexión a una URL de Jira"""
    headers = {
        'Authorization': f'Basic {base64.b64encode(f"{EMAIL}:{API_TOKEN}".encode()).decode()}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Probar endpoint de proyectos
        response = requests.get(
            f"{base_url}/rest/api/3/project",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Conexión exitosa a {base_url}")
            print(f"📋 Proyectos encontrados: {len(projects)}")
            for project in projects[:3]:  # Mostrar solo los primeros 3
                print(f"   - {project['key']}: {project['name']}")
            return True
        else:
            print(f"❌ Error HTTP {response.status_code} en {base_url}")
            print(f"   Respuesta: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout en {base_url}")
        return False
    except requests.exceptions.ConnectionError:
        print(f"🔌 Error de conexión en {base_url}")
        return False
    except Exception as e:
        print(f"❌ Error en {base_url}: {e}")
        return False

def main():
    print("🔍 Probando conectividad con Jira...")
    print(f"📧 Email: {EMAIL}")
    print("=" * 50)
    
    for url in URLS_TO_TEST:
        print(f"\n🌐 Probando: {url}")
        test_connection(url)
    
    print("\n" + "=" * 50)
    print("💡 Si ninguna URL funciona, verifica:")
    print("1. Tu conexión a internet")
    print("2. La URL correcta de tu instancia de Jira")
    print("3. Que el API token sea válido")

if __name__ == "__main__":
    main()
