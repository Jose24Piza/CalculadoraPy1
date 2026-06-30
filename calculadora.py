class Calculator:
    def sum(self, a, b):
        """Suma dos números.
        
        Args:
            a (float): Primer número
            b (float): Segundo número
            
        Returns:
            float: Resultado de la suma
        """
        return a + b
    
    def subtract(self, a, b):
        """Resta dos números.
        
        Args:
            a (float): Minuendo
            b (float): Sustraendo
            
        Returns:
            float: Resultado de la resta
        """
        return a - b
    
    def multiply(self, a, b):
        """Multiplica dos números.
        
        Args:
            a (float): Primer factor
            b (float): Segundo factor
            
        Returns:
            float: Resultado de la multiplicación
        """
        return a * b
    
    def divide(self, a, b):
        """Divide dos números.
        
        Args:
            a (float): Dividendo
            b (float): Divisor
            
        Returns:
            float: Resultado de la división
            
        Raises:
            ValueError: Si el divisor es cero
        """
        if b == 0:
            raise ValueError("No se puede dividir por cero")
        return a / b
    
    def perimetro_rectangulo(self, largo, ancho):
        """Calcula el perímetro de un rectángulo.
        
        Fórmula: P = 2 * (largo + ancho)
        
        Args:
            largo (float): Longitud del rectángulo (debe ser > 0)
            ancho (float): Anchura del rectángulo (debe ser > 0)
            
        Returns:
            float: Perímetro del rectángulo
            
        Raises:
            ValueError: Si largo o ancho son menores o iguales a cero
            TypeError: Si largo o ancho no son números
        """
        # Validar que sean números
        if not isinstance(largo, (int, float)) or not isinstance(ancho, (int, float)):
            raise TypeError("Largo y ancho deben ser números")
        
        # Validar que sean positivos
        if largo <= 0 or ancho <= 0:
            raise ValueError("Largo y ancho deben ser mayores que cero")
        
        # Calcular perímetro
        return 2 * (largo + ancho)