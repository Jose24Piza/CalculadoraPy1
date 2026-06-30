from calculadora import Calculator

def main():
    calc = Calculator()
    
    print("=== CALCULADORA AVANZADA ===")
    print("Operaciones disponibles:")
    print("  +  : Suma")
    print("  -  : Resta")
    print("  *  : Multiplicación")
    print("  /  : División")
    print("  p  : Perímetro de rectángulo")
    
    try:
        operacion = input("\nSeleccione la operación (+, -, *, /, p): ").strip()
        
        if operacion == 'p':
            # Operación para perímetro del rectángulo
            largo = float(input("Ingrese el largo del rectángulo: "))
            ancho = float(input("Ingrese el ancho del rectángulo: "))
            resultado = calc.perimetro_rectangulo(largo, ancho)
            print(f"\n📐 Perímetro del rectángulo ({largo} x {ancho}) = {resultado}")
        else:
            # Operaciones aritméticas tradicionales
            num1 = float(input("Ingrese el primer número: "))
            num2 = float(input("Ingrese el segundo número: "))
            
            if operacion == '+':
                resultado = calc.sum(num1, num2)
            elif operacion == '-':
                resultado = calc.subtract(num1, num2)
            elif operacion == '*':
                resultado = calc.multiply(num1, num2)
            elif operacion == '/':
                resultado = calc.divide(num1, num2)
            else:
                print("❌ Operación no válida")
                return
            
            print(f"\n✅ Resultado: {num1} {operacion} {num2} = {resultado}")
    
    except ValueError as e:
        print(f"❌ Error de valor: {e}")
    except TypeError as e:
        print(f"❌ Error de tipo: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
    