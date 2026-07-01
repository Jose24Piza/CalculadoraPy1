import os
import sys
import json
import requests
from datetime import datetime

class RenderDeploy:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.render.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def deploy_service(self, service_id):
        """Despliega un servicio en Render"""
        url = f"{self.base_url}/services/{service_id}/deploys"
        response = requests.post(url, headers=self.headers)
        
        if response.status_code == 201:
            deploy_data = response.json()
            deploy_id = deploy_data.get('id')
            print(f"✅ Despliegue iniciado: {deploy_id}")
            
            # Esperar a que el despliegue termine
            return self.wait_for_deploy(service_id, deploy_id)
        else:
            print(f"❌ Error en despliegue: {response.status_code}")
            print(response.text)
            return False
    
    def wait_for_deploy(self, service_id, deploy_id, timeout=300):
        """Espera a que el despliegue termine"""
        url = f"{self.base_url}/services/{service_id}/deploys/{deploy_id}"
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                deploy_status = response.json()
                status = deploy_status.get('status')
                print(f"⏳ Estado del despliegue: {status}")
                
                if status == 'live':
                    print("✅ Despliegue completado exitosamente")
                    return True
                elif status in ['failed', 'canceled']:
                    print(f"❌ Despliegue fallido: {status}")
                    return False
                
                time.sleep(5)
            else:
                print(f"⚠️ Error obteniendo estado: {response.status_code}")
                time.sleep(5)
        
        print("❌ Timeout esperando despliegue")
        return False
    
    def health_check(self, service_url):
        """Verifica que el servicio esté funcionando"""
        try:
            response = requests.get(f"{service_url}/health", timeout=10)
            if response.status_code == 200:
                print("✅ Health check exitoso")
                return True
            else:
                print(f"⚠️ Health check falló: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error en health check: {e}")
            return False

def main():
    """Función principal de despliegue"""
    print("🚀 Iniciando proceso de despliegue...")
    
    # Obtener configuración
    api_key = os.environ.get('RENDER_API_KEY')
    staging_service = os.environ.get('RENDER_STAGING_SERVICE_ID')
    production_service = os.environ.get('RENDER_PRODUCTION_SERVICE_ID')
    environment = os.environ.get('DEPLOY_ENV', 'staging')
    
    if not api_key:
        print("❌ RENDER_API_KEY no configurada")
        sys.exit(1)
    
    deployer = RenderDeploy(api_key)
    
    # Determinar servicio a desplegar
    service_id = staging_service if environment == 'staging' else production_service
    service_url = f"https://calculadorapy-{environment}.onrender.com"
    
    if not service_id:
        print(f"❌ RENDER_{environment.upper()}_SERVICE_ID no configurado")
        sys.exit(1)
    
    # Desplegar
    print(f"📦 Desplegando en {environment}...")
    if deployer.deploy_service(service_id):
        print("✅ Despliegue completado")
        
        # Health check
        print("🏥 Realizando health check...")
        if deployer.health_check(service_url):
            print("✅ Servicio funcionando correctamente")
        else:
            print("⚠️ Health check falló, pero el despliegue fue exitoso")
        
        # Guardar registro de despliegue
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'environment': environment,
            'service_id': service_id,
            'service_url': service_url,
            'status': 'success'
        }
        
        with open('deploy-log.json', 'w') as f:
            json.dump(log_data, f, indent=2)
        
        sys.exit(0)
    else:
        print("❌ Despliegue falló")
        sys.exit(1)

if __name__ == "__main__":
    main()