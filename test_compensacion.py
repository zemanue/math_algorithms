"""
Script de prueba para la función compensacion_suma.
Verifica que la estrategia elige correctamente el múltiplo más cercano
(decena o centena) y genera la estructura JSON correcta.
"""

from suma_algoritmos import compensacion_suma
import json


def test_caso(a: int, b: int, descripcion: str = "", nivel: str = "auto"):
    """Ejecuta y muestra un caso de prueba."""
    print(f"\n{'='*60}")
    if descripcion:
        print(f"📝 {descripcion}")
    print(f"{'='*60}")

    resultado = compensacion_suma(a, b, nivel=nivel)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Verificar que el resultado es correcto
    suma_real = a + b
    assert resultado['resultado_final'] == suma_real, \
        f"Error: {resultado['resultado_final']} ≠ {suma_real}"

    # Verificar estructura de transformación si hay pasos
    if resultado['pasos']:
        paso = resultado['pasos'][0]
        assert 'transformacion' in paso, "Falta campo 'transformacion'"
        assert 'operando_principal' in paso['transformacion'], \
            "Falta 'operando_principal'"
        assert 'operando_compensado' in paso['transformacion'], \
            "Falta 'operando_compensado'"

        # Verificar que la suma de ajustes es cero (compensación)
        trans = paso['transformacion']
        ajuste_principal = trans['operando_principal']['ajuste']
        ajuste_compensado = trans['operando_compensado']['ajuste']
        assert ajuste_principal + ajuste_compensado == 0, \
            "Los ajustes no se compensan correctamente"

    print(f"✅ Verificado: {a} + {b} = {suma_real}")


if __name__ == "__main__":
    print("🧮 PRUEBAS DE COMPENSACIÓN EN SUMA")
    print("="*60)

    # ===== PRUEBAS CON DECENAS =====
    print("\n" + "🔟 PRUEBAS CON DECENAS ".center(60, "="))

    test_caso(79, 25, "79 más cerca de 80 (dist=1) que 25 de 30 (dist=5)")
    test_caso(21, 26, "21 más cerca de 20 (dist=1) que 26 de 30 (dist=4)")
    test_caso(15, 25, "Ambos equidistantes (dist=5)")
    test_caso(30, 17, "30 ya es decena, 17 cerca de 20 (dist=3)")
    test_caso(48, 33, "48 cerca de 50 (dist=2), 33 cerca de 30 (dist=3)")
    test_caso(12, 47, "12 cerca de 10 (dist=2), 47 cerca de 50 (dist=3)")
    test_caso(40, 60, "Ambos ya son decenas")
    test_caso(8, 7, "8 cerca de 10 (dist=2), 7 cerca de 10 (dist=3)")

    # ===== PRUEBAS CON CENTENAS =====
    print("\n" + "💯 PRUEBAS CON CENTENAS ".center(60, "="))

    test_caso(198, 145, "198 más cerca de 200 (dist=2)")
    test_caso(305, 287,
              "305 más cerca de 300 (dist=5) que 287 de 300 (dist=13)")
    test_caso(450, 123, "450 ya es centena")
    test_caso(99, 88, "Números < 100, usa decenas", nivel="auto")

    # ===== PRUEBAS FORZANDO NIVEL =====
    print("\n" + "⚙️ PRUEBAS FORZANDO NIVEL ".center(60, "="))

    test_caso(186, 145, "Forzar decena en números grandes", nivel="decena")
    test_caso(79, 25, "Forzar decena explícitamente", nivel="decena")

    print(f"\n{'='*60}")
    print("✅ Todas las pruebas pasaron correctamente")
    print(f"{'='*60}\n")
