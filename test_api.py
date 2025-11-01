"""
Script de prueba para la API Flask.
Ejecuta requests a los diferentes endpoints.
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"


def print_section(title):
    """Imprime un separador visual."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_health():
    """Prueba el endpoint de health check."""
    print_section("1. Health Check")

    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_compensacion_suma(a, b, nivel="auto"):
    """Prueba el endpoint de compensación de suma."""
    operacion_str = f"{a}+{b}"
    nivel_param = f"?nivel={nivel}" if nivel != "auto" else ""
    url = f"{BASE_URL}/suma/compensacion_base10/{operacion_str}{nivel_param}"

    print_section(f"➕ Compensación: {a} + {b} (nivel: {nivel})")
    print(f"🔗 URL: {url}\n")

    response = requests.get(url)

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Operación: {data['operacion_original']}")
        print(f"🎯 Estrategia: {data['estrategia']}")

        if data['pasos']:
            paso = data['pasos'][0]
            print(f"\n🔧 Nivel: {paso['nivel']}")
            print("🛠️  Transformación:")
            print(f"   - Operando principal: {paso['transformacion']['operando_principal']['original']} "
                  f"→ {paso['transformacion']['operando_principal']['ajustado']} "
                  f"(ajuste: {paso['transformacion']['operando_principal']['ajuste']})")
            print(f"   - Operando compensado: {paso['transformacion']['operando_compensado']['original']} "
                  f"→ {paso['transformacion']['operando_compensado']['ajustado']} "
                  f"(ajuste: {paso['transformacion']['operando_compensado']['ajuste']})")
            print(f"📝 Nueva operación: {paso['nueva_operacion']}")
            print(f"💬 Explicación: {paso['comentario']}")
        else:
            print("\n⚠️  No se requiere compensación")

        print(f"\n✅ Resultado final: {data['resultado_final']}")
    else:
        print(f"❌ Error: {response.json()}")


def test_ejemplos():
    """Prueba el endpoint de ejemplos."""
    print_section("📚 Ejemplos precalculados")

    response = requests.get(f"{BASE_URL}/suma/compensacion_base10/ejemplos")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal de ejemplos: {data['total']}\n")

        for ejemplo in data['ejemplos']:
            print(f"  • {ejemplo['nombre']}: {ejemplo['operacion']}")


def test_error_handling():
    """Prueba el manejo de errores."""
    print_section("🚨 Prueba de manejo de errores")

    # Test 1: Formato inválido (sin +)
    print("\n1. Formato sin '+' :")
    response = requests.get(f"{BASE_URL}/suma/compensacion_base10/38")
    print(f"   Status: {response.status_code}")
    print(f"   Error: {response.json()['message']}")

    # Test 2: Parámetros no numéricos
    print("\n2. Parámetros no numéricos:")
    response = requests.get(f"{BASE_URL}/suma/compensacion_base10/abc+123")
    print(f"   Status: {response.status_code}")
    print(f"   Error: {response.json()['message']}")

    # Test 3: Nivel inválido
    print("\n3. Nivel inválido:")
    response = requests.get(
        f"{BASE_URL}/suma/compensacion_base10/10+20?nivel=invalido"
    )
    print(f"   Status: {response.status_code}")
    print(f"   Error: {response.json()['message']}")


if __name__ == "__main__":
    print("\n🧪 PRUEBAS DE LA API FLASK")
    print("=" * 70)

    try:
        # Health check
        test_health()

        # Pruebas de compensación
        test_compensacion_suma(290, 603)
        test_compensacion_suma(79, 25)
        test_compensacion_suma(70, 83)
        test_compensacion_suma(199, 220)
        test_compensacion_suma(30, 17)  # Sin compensación

        # Ejemplos
        test_ejemplos()

        # Manejo de errores
        test_error_handling()

        print("\n" + "=" * 70)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("=" * 70 + "\n")

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se puede conectar a la API")
        print("   Asegúrate de que el servidor Flask esté corriendo:")
        print("   python api.py\n")
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}\n")
