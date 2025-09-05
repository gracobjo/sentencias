#!/usr/bin/env python3
"""
Diagnóstico de conectividad para Jira
"""
import requests
import socket
import ssl

def test_domain_connectivity(domain):
    """Probar conectividad a un dominio específico"""
    print(f"🔍 Probando conectividad a: {domain}")
    
    try:
        # Probar resolución DNS
        ip = socket.gethostbyname(domain)
        print(f"✅ DNS resuelto: {domain} → {ip}")
        
        # Probar conexión HTTPS
        response = requests.get(f"https://{domain}", timeout=10, verify=True)
        print(f"✅ HTTPS accesible: {response.status_code}")
        return True
        
    except socket.gaierror:
        print(f"❌ Error DNS: No se puede resolver {domain}")
        return False
    except requests.exceptions.SSLError:
        print(f"❌ Error SSL: Problema de certificado en {domain}")
        return False
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout: {domain} no responde")
        return False
    except requests.exceptions.ConnectionError:
        print(f"🔌 Error de conexión: No se puede conectar a {domain}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    print("🔧 Diagnóstico de conectividad para Jira")
    print("=" * 50)
    
    # Dominios críticos para Jira
    domains = [
        "gracobjo.atlassian.net",
        "id-frontend.prod-east.frontend.public.atl-paas.net",
        "atlassian.net",
        "api.atlassian.com"
    ]
    
    results = {}
    for domain in domains:
        results[domain] = test_domain_connectivity(domain)
        print()
    
    print("=" * 50)
    print("📊 Resumen:")
    for domain, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {domain}")
    
    if not results["id-frontend.prod-east.frontend.public.atl-paas.net"]:
        print("\n🚨 PROBLEMA IDENTIFICADO:")
        print("El dominio id-frontend.prod-east.frontend.public.atl-paas.net")
        print("no es accesible. Este es el dominio que Jira necesita para")
        print("cargar los scripts de JavaScript.")
        print("\n💡 Soluciones:")
        print("1. Verificar configuración de firewall/proxy")
        print("2. Contactar al administrador de red")
        print("3. Probar desde otra red")

if __name__ == "__main__":
    main()
