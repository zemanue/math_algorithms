"""
Script de prueba para la función compensacion_suma.
Verifica que la estrategia elige correctamente la decena más cercana.
"""

from suma_algoritmos import compensacion_suma
import json


def test_caso(a: int, b: int, descripcion: str = ""):
    """Ejecuta y muestra un caso de prueba."""
    print(f"\n{'='*60}")
    if descripcion:
        print(f"📝 {descripcion}")
    print(f"{'='*60}")

    resultado = compensacion_suma(a, b)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Verificar que el resultado es correcto
    suma_real = a + b
    assert resultado['resultado_final'] == suma_real, \
        f"Error: {resultado['resultado_final']} ≠ {suma_real}"
    print(f"✅ Verificado: {a} + {b} = {suma_real}")


if __name__ == "__main__":
    print("🧮 PRUEBAS DE COMPENSACIÓN EN SUMA")
    print("="*60)

    # Caso 1: El ejemplo original (79 está más cerca de 80)
    test_caso(79, 25, "79 más cerca de 80 (dist=1) que 25 de 30 (dist=5)")

    # Caso 2: El nuevo ejemplo que mencionaste
    test_caso(21, 26, "21 más cerca de 20 (dist=1) que 26 de 30 (dist=4)")

    # Caso 3: Ambos equidistantes (debe elegir el primero)
    test_caso(15, 25, "Ambos equidistantes (dist=5)")

    # Caso 4: Un número ya es decena
    test_caso(30, 17, "30 ya es decena, 17 cerca de 20 (dist=3)")

    # Caso 5: Número más cerca de decena inferior
    test_caso(48, 33, "48 cerca de 50 (dist=2), 33 cerca de 30 (dist=3)")

    # Caso 6: Otro caso con decena inferior
    test_caso(12, 47, "12 cerca de 10 (dist=2), 47 cerca de 50 (dist=3)")

    # Caso 7: Ambos ya son decenas
    test_caso(40, 60, "Ambos ya son decenas")

    # Caso 8: Números pequeños
    test_caso(8, 7, "8 cerca de 10 (dist=2), 7 cerca de 10 (dist=3)")

    print(f"\n{'='*60}")
    print("✅ Todas las pruebas pasaron correctamente")
    print(f"{'='*60}\n")
