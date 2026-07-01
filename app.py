# app.py - Aplicación para Render
from flask import Flask, jsonify, request
from datetime import datetime
import os
import sys
import logging

# Configurar logging para Render
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Importar Calculadora
try:
    from calculadora import Calculator
    calc = Calculator()
    logger.info("✅ Calculadora importada correctamente")
except ImportError as e:
    logger.error(f"❌ Error importando Calculadora: {e}")
    calc = None

app = Flask(__name__)

# Variables de entorno de Render
RENDER_SERVICE_NAME = os.environ.get('RENDER_SERVICE_NAME', 'calculadorapy')
RENDER_SERVICE_ID = os.environ.get('RENDER_SERVICE_ID', 'unknown')
RENDER_GIT_COMMIT = os.environ.get('RENDER_GIT_COMMIT', 'unknown')
RENDER_GIT_BRANCH = os.environ.get('RENDER_GIT_BRANCH', 'unknown')
FLASK_ENV = os.environ.get('FLASK_ENV', 'production')

@app.route('/')
def index():
    """Página principal"""
    return jsonify({
        'service': RENDER_SERVICE_NAME,
        'environment': FLASK_ENV,
        'status': 'running',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'git_commit': RENDER_GIT_COMMIT,
        'git_branch': RENDER_GIT_BRANCH
    })

@app.route('/health')
def health_check():
    """Health check para Render"""
    return jsonify({
        'status': 'healthy',
        'service': RENDER_SERVICE_NAME,
        'environment': FLASK_ENV,
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200

@app.route('/api/sum', methods=['POST'])
def api_sum():
    """API para sumar dos números"""
    data = request.get_json()
    if not data or 'a' not in data or 'b' not in data:
        return jsonify({'error': 'Faltan parámetros a y b'}), 400
    
    try:
        a = float(data['a'])
        b = float(data['b'])
        result = calc.sum(a, b) if calc else a + b
        logger.info(f"Suma: {a} + {b} = {result}")
        return jsonify({
            'operation': 'sum',
            'a': a,
            'b': b,
            'result': result
        })
    except Exception as e:
        logger.error(f"Error en suma: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/perimeter', methods=['POST'])
def api_perimeter():
    """API para calcular perímetro de rectángulo"""
    data = request.get_json()
    if not data or 'largo' not in data or 'ancho' not in data:
        return jsonify({'error': 'Faltan parámetros largo y ancho'}), 400
    
    try:
        largo = float(data['largo'])
        ancho = float(data['ancho'])
        if not calc:
            return jsonify({'error': 'Calculadora no disponible'}), 500
        result = calc.perimetro_rectangulo(largo, ancho)
        logger.info(f"Perímetro: {largo} x {ancho} = {result}")
        return jsonify({
            'operation': 'perimeter',
            'largo': largo,
            'ancho': ancho,
            'perimeter': result
        })
    except Exception as e:
        logger.error(f"Error en perímetro: {e}")
        return jsonify({'error': str(e)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Error interno: {error}")
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Iniciando servicio {RENDER_SERVICE_NAME} en puerto {port}")
    logger.info(f"📊 Entorno: {FLASK_ENV}")
    logger.info(f"🔗 Git: {RENDER_GIT_BRANCH}@{RENDER_GIT_COMMIT[:8]}")
    app.run(host='0.0.0.0', port=port, debug=False)