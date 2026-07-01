# render_metrics.py - Script para monitoreo con Render
import time
import os
import json
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

class RenderMetrics:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
        self.response_times = []
        self.deployments = []
        self.service_name = os.environ.get('RENDER_SERVICE_NAME', 'calculadorapy')
        self.environment = os.environ.get('FLASK_ENV', 'production')
    
    def record_request(self, response_time, success=True):
        """Registra una solicitud"""
        self.request_count += 1
        self.response_times.append(response_time)
        if not success:
            self.error_count += 1
    
    def get_metrics(self):
        """Obtiene todas las métricas"""
        uptime = time.time() - self.start_time
        avg_response = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        error_rate = (self.error_count / self.request_count * 100) if self.request_count > 0 else 0
        
        return {
            'service': self.service_name,
            'environment': self.environment,
            'uptime': uptime,
            'uptime_hours': uptime / 3600,
            'total_requests': self.request_count,
            'avg_response_time': avg_response,
            'error_rate': error_rate,
            'last_deployment': self.get_last_deployment(),
            'timestamp': datetime.now().isoformat(),
            'render_environment': os.environ.get('RENDER', 'Not running on Render'),
            'render_service_id': os.environ.get('RENDER_SERVICE_ID', 'N/A')
        }
    
    def get_last_deployment(self):
        """Obtiene información del último despliegue en Render"""
        try:
            deploy_time = os.environ.get('RENDER_DEPLOY_TIME', 'Not available')
            deploy_commit = os.environ.get('RENDER_GIT_COMMIT', 'Not available')
            return {
                'time': deploy_time,
                'commit': deploy_commit,
                'branch': os.environ.get('RENDER_GIT_BRANCH', 'main')
            }
        except:
            return {'time': 'Not available', 'commit': 'Not available'}

# Endpoint de health check para Render
@app.route('/health')
def health_check():
    """Health check endpoint requerido por Render"""
    return jsonify({
        'status': 'healthy',
        'service': os.environ.get('RENDER_SERVICE_NAME', 'calculadorapy'),
        'timestamp': datetime.now().isoformat(),
        'environment': os.environ.get('FLASK_ENV', 'production')
    }), 200

# Endpoint de métricas
@app.route('/metrics')
def get_metrics():
    """Endpoint para obtener métricas de la aplicación"""
    metrics = render_metrics.get_metrics()
    return jsonify(metrics), 200

render_metrics = RenderMetrics()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))