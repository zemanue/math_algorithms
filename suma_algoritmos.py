
import json


def compensacion_suma(a: int, b: int, nivel: str = "auto") -> dict:
    """
    Aplica la estrategia de compensación a la suma a + b.
    Devuelve un diccionario con todos los pasos del razonamiento.

    La función elige el número más cercano a un múltiplo de 10 o 100
    (decena o centena) y compensa el ajuste en el otro sumando
    para mantener la suma constante.

    Args:
        a: Primer operando
        b: Segundo operando
        nivel: "decena", "centena" o "auto" (detecta automáticamente)

    Returns:
        Diccionario con la estructura completa de la compensación
    """
    pasos = []
    original = (a, b)

    # Determinar el nivel de compensación automáticamente
    if nivel == "auto":
        # Si algún número tiene 3+ dígitos, intentar centena
        if a >= 100 or b >= 100:
            nivel = "centena"
        else:
            nivel = "decena"

    # Configurar el divisor según el nivel
    divisor = 10 if nivel == "decena" else 100

    # 1️⃣ Calcular restos
    resto_a = a % divisor
    resto_b = b % divisor

    # Si al menos uno ya es múltiplo del divisor, no hay que ajustar nada.
    # El objetivo de la compensación es conseguir que UNO sea múltiplo.
    if resto_a == 0 or resto_b == 0:
        resultado = a + b
        return {
            "operacion_original": f"{a} + {b}",
            "operandos": [a, b],
            "estrategia": "compensacion",
            "pasos": [],
            "resultado_final": resultado
        }

    # 2️⃣ Para cada número, calculamos distancia al múltiplo
    # superior e inferior y elegimos la más cercana

    # Para 'a':
    dist_a_superior = divisor - resto_a
    dist_a_inferior = resto_a

    if dist_a_inferior < dist_a_superior:
        # Más cerca del múltiplo inferior
        dist_a = dist_a_inferior
        ajuste_a = -dist_a_inferior  # Ajuste negativo (restar)
        multiplo_a = a - dist_a_inferior
        direccion_a = "inferior"
    else:
        # Más cerca del múltiplo superior
        dist_a = dist_a_superior
        ajuste_a = dist_a_superior  # Ajuste positivo (sumar)
        multiplo_a = a + dist_a_superior
        direccion_a = "superior"

    # Para 'b':
    dist_b_superior = divisor - resto_b
    dist_b_inferior = resto_b

    if dist_b_inferior < dist_b_superior:
        # Más cerca del múltiplo inferior
        dist_b = dist_b_inferior
        ajuste_b = -dist_b_inferior  # Ajuste negativo (restar)
        multiplo_b = b - dist_b_inferior
        direccion_b = "inferior"
    else:
        # Más cerca del múltiplo superior
        dist_b = dist_b_superior
        ajuste_b = dist_b_superior  # Ajuste positivo (sumar)
        multiplo_b = b + dist_b_superior
        direccion_b = "superior"

    # 3️⃣ Elegimos el número con menor distancia a su múltiplo más cercano
    if dist_a <= dist_b:
        # Ajustamos 'a' a su múltiplo más cercano
        operando_principal_orig = a
        operando_principal_ajustado = multiplo_a
        ajuste_principal = ajuste_a
        direccion_principal = direccion_a

        operando_compensado_orig = b
        operando_compensado_ajustado = b - ajuste_a  # Compensación inversa
        ajuste_compensado = -ajuste_a
        direccion_compensada = "inferior" if ajuste_a > 0 else "superior"

        nuevo_a = operando_principal_ajustado
        nuevo_b = operando_compensado_ajustado

    else:
        # Ajustamos 'b' a su múltiplo más cercano
        operando_principal_orig = b
        operando_principal_ajustado = multiplo_b
        ajuste_principal = ajuste_b
        direccion_principal = direccion_b

        operando_compensado_orig = a
        operando_compensado_ajustado = a - ajuste_b  # Compensación inversa
        ajuste_compensado = -ajuste_b
        direccion_compensada = "inferior" if ajuste_b > 0 else "superior"

        nuevo_a = operando_compensado_ajustado
        nuevo_b = operando_principal_ajustado

    # 4️⃣ Construir comentario
    verbo_principal = "sumamos" if ajuste_principal > 0 else "restamos"
    verbo_compensado = "restamos" if ajuste_principal > 0 else "sumamos"
    valor_abs = abs(ajuste_principal)

    comentario = (
        f"Ajustamos {operando_principal_orig} a "
        f"{operando_principal_ajustado} ({verbo_principal} {valor_abs}) "
        f"y compensamos el otro sumando de {operando_compensado_orig} a "
        f"{operando_compensado_ajustado} ({verbo_compensado} {valor_abs})."
    )

    # 5️⃣ Construir el paso con la estructura
    pasos.append({
        "nivel": nivel,
        "transformacion": {
            "operando_principal": {
                "original": operando_principal_orig,
                "ajustado": operando_principal_ajustado,
                "ajuste": ajuste_principal,
                "direccion": direccion_principal
            },
            "operando_compensado": {
                "original": operando_compensado_orig,
                "ajustado": operando_compensado_ajustado,
                "ajuste": ajuste_compensado,
                "direccion": direccion_compensada
            }
        },
        "nueva_operacion": f"{nuevo_a} + {nuevo_b}",
        "comentario": comentario
    })

    resultado_final = nuevo_a + nuevo_b

    return {
        "operacion_original": f"{original[0]} + {original[1]}",
        "operandos": [original[0], original[1]],
        "estrategia": "compensacion",
        "pasos": pasos,
        "resultado_final": resultado_final
    }


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 70)
    print("EJEMPLOS DE COMPENSACIÓN EN SUMA (VERSIÓN SIMPLE)")
    print("=" * 70)

    # Ejemplo 1: Decena superior
    print("\n1️⃣ Decena superior: 79 + 25")
    print(json.dumps(compensacion_suma(79, 25), indent=2, ensure_ascii=False))

    # Ejemplo 2: Decena inferior
    print("\n2️⃣ Decena inferior: 21 + 26")
    print(json.dumps(compensacion_suma(21, 26), indent=2, ensure_ascii=False))

    # Ejemplo 3: Centena (un solo paso)
    print("\n3️⃣ Centena: 198 + 145")
    resultado = compensacion_suma(198, 145)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Ejemplo 4: Sin compensación necesaria
    print("\n4️⃣ Sin compensación: 30 + 17")
    print(json.dumps(compensacion_suma(30, 17), indent=2, ensure_ascii=False))

    # Ejemplo 5: Forzar nivel decena
    print("\n5️⃣ Forzar decena en 198 + 145:")
    print(json.dumps(compensacion_suma(198, 145, nivel="decena"),
                     indent=2, ensure_ascii=False))
