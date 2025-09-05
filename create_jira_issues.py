#!/usr/bin/env python3
"""
Script para crear issues en Jira usando la REST API
"""
import requests
import json
import base64
from typing import List, Dict

class JiraManager:
    def __init__(self, base_url: str, email: str, api_token: str, project_key: str):
        self.base_url = base_url
        self.email = email
        self.api_token = api_token
        self.project_key = project_key
        self.headers = {
            'Authorization': f'Basic {base64.b64encode(f"{email}:{api_token}".encode()).decode()}',
            'Content-Type': 'application/json'
        }
    
    def create_epic(self, summary: str, description: str) -> Dict:
        """Crear un Epic en Jira"""
        data = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Epic"}
            }
        }
        
        response = requests.post(
            f"{self.base_url}/rest/api/3/issue",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Error creating epic: {response.text}")
    
    def create_story(self, summary: str, description: str, epic_key: str, priority: str = "Medium", story_points: int = 5) -> Dict:
        """Crear una User Story en Jira"""
        data = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Story"},
                "priority": {"name": priority},
                "customfield_10014": story_points,  # Story Points field (puede variar)
                "customfield_10008": epic_key  # Epic Link field (puede variar)
            }
        }
        
        response = requests.post(
            f"{self.base_url}/rest/api/3/issue",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Error creating story: {response.text}")

# Configuración - Ajusta estos valores
JIRA_BASE_URL = "https://gracobjo.atlassian.net"
EMAIL = "gracobjo@gmail.com"  # Tu email real de Atlassian
API_TOKEN = "YOUR_API_TOKEN_HERE"      # ⚠️ REEMPLAZA con tu token real de https://id.atlassian.com/manage-profile/security/api-tokens
PROJECT_KEY = "SCRUM"                # ⚠️ VERIFICA que sea la clave correcta de tu proyecto

def main():
    jira = JiraManager(JIRA_BASE_URL, EMAIL, API_TOKEN, PROJECT_KEY)
    
    # Definir los epics
    epics = [
        {
            "summary": "Sprint 1: Optimización del Sistema IA",
            "description": "Mejorar y estabilizar el sistema de IA implementado"
        },
        {
            "summary": "Sprint 2: Mejoras en la Interfaz de Usuario", 
            "description": "Mejorar la experiencia de usuario y usabilidad"
        },
        {
            "summary": "Sprint 3: Funcionalidades Avanzadas de Demanda",
            "description": "Expandir las capacidades de generación de demandas"
        },
        {
            "summary": "Sprint 4: Integración y APIs",
            "description": "Mejorar la integración con sistemas externos"
        },
        {
            "summary": "Sprint 5: Escalabilidad y Rendimiento",
            "description": "Preparar el sistema para mayor carga de usuarios"
        },
        {
            "summary": "Sprint 6: Testing y Calidad",
            "description": "Asegurar la calidad y estabilidad del sistema"
        },
        {
            "summary": "Sprint 7: Documentación y Entrenamiento",
            "description": "Documentar completamente el sistema y preparar para producción"
        }
    ]
    
    # Crear epics
    epic_keys = {}
    for epic in epics:
        try:
            result = jira.create_epic(epic["summary"], epic["description"])
            epic_key = result["key"]
            epic_keys[epic["summary"]] = epic_key
            print(f"✅ Epic creado: {epic_key} - {epic['summary']}")
        except Exception as e:
            print(f"❌ Error creando epic: {e}")
    
    # Definir algunas user stories de ejemplo
    stories = [
        {
            "summary": "Optimizar modelo SBERT para mejorar precisión",
            "description": "Como desarrollador quiero optimizar el modelo SBERT para mejorar la precisión del análisis de documentos legales",
            "epic": "Sprint 1: Optimización del Sistema IA",
            "priority": "High",
            "story_points": 8
        },
        {
            "summary": "Implementar drag & drop para subir documentos",
            "description": "Como usuario quiero una interfaz más intuitiva para subir documentos con drag & drop",
            "epic": "Sprint 2: Mejoras en la Interfaz de Usuario",
            "priority": "High",
            "story_points": 5
        }
    ]
    
    # Crear user stories
    for story in stories:
        try:
            epic_key = epic_keys.get(story["epic"])
            if epic_key:
                result = jira.create_story(
                    story["summary"],
                    story["description"],
                    epic_key,
                    story["priority"],
                    story["story_points"]
                )
                print(f"✅ Story creada: {result['key']} - {story['summary']}")
            else:
                print(f"⚠️ Epic no encontrado para: {story['epic']}")
        except Exception as e:
            print(f"❌ Error creando story: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando creación de Epics en Jira...")
    print(f"📧 Email: {EMAIL}")
    print(f"🔗 URL: {JIRA_BASE_URL}")
    print(f"📋 Proyecto: {PROJECT_KEY}")
    print("=" * 50)
    
    try:
        main()
        print("=" * 50)
        print("✅ Proceso completado!")
    except Exception as e:
        print(f"❌ Error general: {e}")
