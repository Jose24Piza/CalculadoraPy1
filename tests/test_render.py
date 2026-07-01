# test_render.py - Script para pruebas en entorno Render

import subprocess
import sys
import os
import json
from datetime import datetime
import requests

def run_tests():
    """Ejecuta todas las pruebas y genera reporte"""
    print("🧪 Ejecutando pruebas para Render...")
    
    # Configurar PYTHONPATH
    os.environ['PYTHONPATH'] = f"{os.getcwd()}:{os.environ.get('PYTHONPATH', '')}"
    
    # Ejecutar pruebas con pytest
    result = subprocess.run([
        'pytest', 'tests/',
        '-v',
        '--cov=.',
        '--cov-report=term-missing',
        '--cov-report=html',
        '--junitxml=test-results-render.xml'
    ], capture_output=True, text=True)
    
    # Guardar resultados para Render
    results = {
        'timestamp': datetime.now().isoformat(),
        'environment': os.environ.get('FLASK_ENV', 'unknown'),
        'service': os.environ.get('RENDER_SERVICE_NAME', 'unknown'),
        'return_code': result.returncode,
        'success': result.returncode == 0,
        'git_commit': os.environ.get('RENDER_GIT_COMMIT', 'unknown'),
        'git_branch': os.environ.get('RENDER_GIT_BRANCH', 'unknown')
    }
    
    with open('test-results-render.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Mostrar resultados en logs de Render
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    if result.returncode == 0:
        print("✅ Todos los tests pasaron - Listo para despliegue en Render")
    else:
        print("❌ Tests fallaron - Despliegue cancelado")
    
    return result.returncode

def health_check_render():
    """Verifica el health check en Render"""
    service_url = f"https://{os.environ.get('RENDER_SERVICE_NAME', 'calculadorapy')}.onrender.com"
    health_url = f"{service_url}/health"
    
    try:
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Health check exitoso en {service_url}")
            return True
        else:
            print(f"⚠️ Health check falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return False

if __name__ == "__main__":
    exit_code = run_tests()
    if exit_code == 0:
        health_check_render()
    sys.exit(exit_code)