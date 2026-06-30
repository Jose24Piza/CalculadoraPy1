import pytest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculadora import Calculator

class TestCalculator:
    """Pruebas para la clase Calculator"""
    
    @classmethod
    def setup_class(cls):
        """Configuración inicial para todas las pruebas"""
        cls.calc = Calculator()
    
    # ============ PRUEBAS PARA SUMA ============
    def test_suma_correcta(self):
        """Prueba caso correcto: 2 + 3 = 5"""
        assert self.calc.sum(2, 3) == 5
    
    def test_suma_con_negativos(self):
        """Prueba caso límite: números negativos"""
        assert self.calc.sum(-5, 3) == -2
    
    def test_suma_con_decimales(self):
        """Prueba caso límite: números decimales"""
        assert self.calc.sum(2.5, 3.7) == 6.2
    
    # ============ PRUEBAS PARA RESTA ============
    def test_resta_correcta(self):
        """Prueba caso correcto: 10 - 5 = 5"""
        assert self.calc.subtract(10, 5) == 5
    
    def test_resta_con_negativos(self):
        """Prueba caso límite: números negativos"""
        assert self.calc.subtract(-5, -3) == -2
    
    def test_resta_con_decimales(self):
        """Prueba caso límite: números decimales"""
        assert self.calc.subtract(10.5, 3.2) == 7.3
    
    # ============ PRUEBAS PARA MULTIPLICACIÓN ============
    def test_multiplicacion_correcta(self):
        """Prueba caso correcto: 3 * 4 = 12"""
        assert self.calc.multiply(3, 4) == 12
    
    def test_multiplicacion_con_cero(self):
        """Prueba caso límite: multiplicación por cero"""
        assert self.calc.multiply(5, 0) == 0
    
    def test_multiplicacion_con_negativos(self):
        """Prueba caso límite: números negativos"""
        assert self.calc.multiply(-3, 4) == -12
    
    # ============ PRUEBAS PARA DIVISIÓN ============
    def test_division_correcta(self):
        """Prueba caso correcto: 10 / 2 = 5"""
        assert self.calc.divide(10, 2) == 5
    
    def test_division_con_decimales(self):
        """Prueba caso límite: división con decimales"""
        assert self.calc.divide(10, 3) == pytest.approx(3.3333333333333335)
    
    def test_division_por_cero(self):
        """Prueba caso error: división por cero debe lanzar ValueError"""
        with pytest.raises(ValueError, match="No se puede dividir por cero"):
            self.calc.divide(10, 0)
    
    # ============ PRUEBAS PARA PERÍMETRO DEL RECTÁNGULO ============
    def test_perimetro_rectangulo_correcto(self):
        """Prueba caso correcto: largo=5, ancho=3 -> perímetro=16"""
        assert self.calc.perimetro_rectangulo(5, 3) == 16
    
    def test_perimetro_rectangulo_cuadrado(self):
        """Prueba caso límite: cuadrado (largo=ancho)"""
        assert self.calc.perimetro_rectangulo(4, 4) == 16
    
    def test_perimetro_rectangulo_decimales(self):
        """Prueba caso límite: números decimales"""
        assert self.calc.perimetro_rectangulo(5.5, 3.2) == 17.4
    
    def test_perimetro_rectangulo_largo_cero(self):
        """Prueba caso error: largo = 0 debe lanzar ValueError"""
        with pytest.raises(ValueError, match="Largo y ancho deben ser mayores que cero"):
            self.calc.perimetro_rectangulo(0, 3)
    
    def test_perimetro_rectangulo_ancho_cero(self):
        """Prueba caso error: ancho = 0 debe lanzar ValueError"""
        with pytest.raises(ValueError, match="Largo y ancho deben ser mayores que cero"):
            self.calc.perimetro_rectangulo(5, 0)
    
    def test_perimetro_rectangulo_valores_negativos(self):
        """Prueba caso error: valores negativos deben lanzar ValueError"""
        with pytest.raises(ValueError, match="Largo y ancho deben ser mayores que cero"):
            self.calc.perimetro_rectangulo(-5, 3)
    
    def test_perimetro_rectangulo_tipo_invalido(self):
        """Prueba caso error: tipo de dato inválido debe lanzar TypeError"""
        with pytest.raises(TypeError, match="Largo y ancho deben ser números"):
            self.calc.perimetro_rectangulo("5", 3)
    
    def test_perimetro_rectangulo_valores_grandes(self):
        """Prueba caso límite: valores muy grandes"""
        resultado = self.calc.perimetro_rectangulo(1000000, 2000000)
        assert resultado == 6000000