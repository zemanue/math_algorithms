import json
from typing import Optional


def _calcular_peso_ajuste(ajuste: int) -> float:
    """
    Calcula un peso que determina la facilidad de cálculo mental.

    Estrategia: Los ajustes múltiplos de 10 son más fáciles de calcular
    mentalmente, por lo que reciben un bonus (peso reducido).

    Ejemplos:
    - ajuste = 30 (múltiplo de 10) → peso = 15 (30 * 0.5)
    - ajuste = 17 (no múltiplo)    → peso = 17 (sin bonus)

    Args:
        ajuste: Valor del ajuste a evaluar

    Returns:
        Peso del ajuste (menor peso = más fácil de calcular)
    """
    peso = abs(ajuste)

    # BONUS: Si el ajuste es múltiplo de 10 (10, 20, 30, 100...),
    # aplicamos un 50% de descuento en el peso porque es más fácil
    # de calcular mentalmente (ej: +30 es más fácil que +17)
    if ajuste != 0 and ajuste % 10 == 0:
        peso *= 0.5  # Bonus del 50%

    return peso


def _calcular_ajuste_optimo(
        valor: int, divisor: int) -> int:
    """
    Calcula el mejor ajuste (superior o inferior) para un valor dado.

    Args:
        valor: Número a ajustar
        divisor: Múltiplo objetivo (10, 100, etc.)

    Returns:
        - ajuste óptimo (positivo o negativo)
    """
    resto = valor % divisor
    dist_inferior = resto
    dist_superior = divisor - resto

    # Elegir el múltiplo más cercano
    if dist_inferior < dist_superior:
        return -dist_inferior
    else:
        return dist_superior


def _aplicar_compensacion(a: int, b: int, divisor: int) -> Optional[dict]:
    """
    Aplica compensación para un nivel específico (decena, centena, etc.).

    Estrategia: ajustar el operando más cercano a un múltiplo del divisor
    y compensar el ajuste en el otro operando para mantener la suma igual.

    Args:
        a, b: Operandos actuales
        divisor: 10 (decenas), 100 (centenas), 1000 (millares), etc.

    Returns:
        Dict con el paso de compensación, o None si no se requiere
    """
    # Mapeo automático de divisor a nombre de nivel
    nivel_nombre = {
        10: "decena",
        100: "centena",
        1000: "unidad_de_millar"
    }.get(divisor, f"multiplo_de_{divisor}")

    resto_a = a % divisor
    resto_b = b % divisor

    # Si al menos uno ya es múltiplo, no se requiere compensación
    if resto_a == 0 or resto_b == 0:
        return None

    # Calcular mejor ajuste para cada operando (al múltiplo más cercano)
    ajuste_a = _calcular_ajuste_optimo(a, divisor)
    ajuste_b = _calcular_ajuste_optimo(b, divisor)

    # =======================================================================
    # SELECCIÓN INTELIGENTE DEL AJUSTE
    # =======================================================================
    # No siempre el ajuste más pequeño es el más fácil mentalmente.
    # Ejemplo: 70 + 83
    #   - Ajustar 70→100 requiere +30 (múltiplo de 10, fácil)
    #   - Ajustar 83→100 requiere +17 (más pequeño, pero más difícil)
    #
    # Solución: Calculamos un "peso" que considera:
    #   1. La magnitud del ajuste (menor es mejor)
    #   2. Si es múltiplo de 10 (bonus del 50%)
    #
    # Ejemplos de pesos:
    #   - ajuste +30 (×10) → peso 15 (30 * 0.5)
    #   - ajuste +17       → peso 17 (sin bonus)
    #   - ajuste +1        → peso 1  (muy pequeño, gana siempre)
    #   - ajuste +400 (×10)→ peso 200 (grande, pierde ante +41)
    # =======================================================================

    peso_a = _calcular_peso_ajuste(ajuste_a)
    peso_b = _calcular_peso_ajuste(ajuste_b)

    # Elegir el ajuste con MENOR PESO (más fácil de calcular)
    if peso_a <= peso_b:
        # Ajustar 'a', compensar 'b'
        principal_orig = a
        principal_ajustado = a + ajuste_a
        ajuste_principal = ajuste_a

        compensado_orig = b
        compensado_ajustado = b - ajuste_a
        ajuste_compensado = -ajuste_a

        nuevo_a, nuevo_b = principal_ajustado, compensado_ajustado
    else:
        # Ajustar 'b', compensar 'a'
        principal_orig = b
        principal_ajustado = b + ajuste_b
        ajuste_principal = ajuste_b

        compensado_orig = a
        compensado_ajustado = a - ajuste_b
        ajuste_compensado = -ajuste_b

        nuevo_a, nuevo_b = compensado_ajustado, principal_ajustado

    # Generar comentario explicativo
    verbo_principal = "sumamos" if ajuste_principal > 0 else "restamos"
    verbo_compensado = "restamos" if ajuste_principal > 0 else "sumamos"
    valor_abs = abs(ajuste_principal)

    comentario = (
        f"Ajustamos {principal_orig} a {principal_ajustado} "
        f"({verbo_principal} {valor_abs}) y compensamos el otro sumando "
        f"de {compensado_orig} a {compensado_ajustado} "
        f"({verbo_compensado} {valor_abs})."
    )

    return {
        "nivel": nivel_nombre,
        "transformacion": {
            "operando_principal": {
                "original": principal_orig,
                "ajustado": principal_ajustado,
                "ajuste": ajuste_principal,
            },
            "operando_compensado": {
                "original": compensado_orig,
                "ajustado": compensado_ajustado,
                "ajuste": ajuste_compensado,
            }
        },
        "nueva_operacion": f"{nuevo_a} + {nuevo_b}",
        "comentario": comentario,
        "nuevos_valores": (nuevo_a, nuevo_b)
    }


def compensacion_base10_suma(a: int, b: int, nivel: str = "auto") -> dict:
    """
    Aplica la estrategia de compensación en base 10 a la suma a + b.

    Estrategia mental: transforma la suma en una equivalente más fácil
    ajustando un operando a un múltiplo redondo de base 10 (10, 100, 1000)
    y compensando el cambio en el otro operando.

    Ejemplo: 79 + 25 → 80 + 24 = 104
            (ajusto +1)  (compenso -1)
    ajustando un operando a un múltiplo redondo (10, 100, etc.) y
    compensando el cambio en el otro operando.

    Ejemplo: 79 + 25 → 80 + 24 = 104
            (ajusto +1)  (compenso -1)

    Args:
        a: Primer operando
        b: Segundo operando
        nivel: "decena", "centena", "unidad_de_millar" o "auto" (por defecto)
                - "auto": detecta automáticamente de forma progresiva:
                    1. Si algún operando es múltiplo de 100 Y suma >= 1000
                        → usa unidades de millar
                    2. Si algún operando es múltiplo de 10 Y suma >= 100
                        → usa centenas
                    3. En caso contrario → usa decenas
                - "decena": fuerza compensación a múltiplos de 10
                - "centena": fuerza compensación a múltiplos de 100
                - "unidad_de_millar": fuerza compensación a múltiplos de 1000

    Returns:
        Dict con la operación original, estrategia usada, pasos detallados
        y resultado final
    """
    pasos = []
    original = (a, b)

    # Determinar divisor según nivel especificado
    if nivel == "auto":
        # Auto-detección inteligente: escalar progresivamente según mérito
        suma_total = a + b

        # NIVEL 1: ¿Merece compensar a UNIDADES DE MILLAR?
        # Condición: algún operando es múltiplo de 100 Y suma >= 1000
        if (a % 100 == 0 or b % 100 == 0) and suma_total >= 1000:
            divisor = 1000

        # NIVEL 2: ¿Merece compensar a CENTENAS?
        # Condición: algún operando es múltiplo de 10 Y suma >= 100
        elif (a % 10 == 0 or b % 10 == 0) and suma_total >= 100:
            divisor = 100

        # NIVEL 3: DECENAS (por defecto)
        # Siempre se intenta si los niveles superiores no aplican
        else:
            divisor = 10

    elif nivel == "decena":
        divisor = 10
    elif nivel == "centena":
        divisor = 100
    elif nivel == "unidad_de_millar":
        divisor = 1000
    else:
        raise ValueError(
            f"Nivel '{nivel}' no válido. "
            f"Use 'auto', 'decena', 'centena' o 'unidad_de_millar'."
        )

    # Aplicar compensación con el divisor seleccionado
    paso = _aplicar_compensacion(a, b, divisor)

    if paso:
        # Extraer nuevos valores y limpiar campo auxiliar
        nuevos_valores = paso.pop("nuevos_valores")
        pasos.append(paso)
        resultado_final = nuevos_valores[0] + nuevos_valores[1]
    else:
        # No se requiere compensación (uno ya es múltiplo)
        resultado_final = a + b

    return {
        "operacion_original": f"{original[0]} + {original[1]}",
        "operandos": [original[0], original[1]],
        "estrategia": "compensacion_base10",
        "pasos": pasos,
        "resultado_final": resultado_final
    }


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 70)
    print("EJEMPLOS DE COMPENSACIÓN BASE 10 EN SUMA")
    print("=" * 70)

    # Ejemplo 1: Decena superior
    print("\n1️⃣ Decena superior: 79 + 25")
    resultado = compensacion_base10_suma(79, 25)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Ejemplo 2: Decena inferior
    print("\n2️⃣ Decena inferior: 21 + 26")
    resultado = compensacion_base10_suma(21, 26)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Ejemplo 3: Sin compensación necesaria
    print("\n3️⃣ Sin compensación: 30 + 17")
    resultado = compensacion_base10_suma(30, 17)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Ejemplo 4: CASO INTERESANTE - Prioridad a múltiplo de 10
    print("\n4️⃣ Prioridad múltiplo de 10: 70 + 83")
    print("   (Ajuste +30 gana sobre +17 por ser múltiplo de 10)")
    resultado = compensacion_base10_suma(70, 83)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Ejemplo 5: CASO INTERESANTE - Ajuste pequeño gana
    print("\n5️⃣ Ajuste pequeño gana: 199 + 220")
    print("   (Ajuste +1 gana sobre -20 por ser mucho menor)")
    resultado = compensacion_base10_suma(199, 220)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Ejemplo 6: CASO INTERESANTE - Ajuste pequeño gana sobre grande
    print("\n6️⃣ Ajuste pequeño vs grande: 1600 + 7041")
    print("   (Ajuste +41 gana sobre +400 aunque 400 sea múltiplo)")
    resultado = compensacion_base10_suma(1600, 7041)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Ejemplo 7: Múltiplo de 10, pero suma < 100 → NO compensa
    print("\n7️⃣ No merece compensar: 20 + 27")
    resultado = compensacion_base10_suma(20, 27)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Ejemplo 8: Múltiplo de 100, suma >= 1000 → compensa a millar
    print("\n8️⃣ Auto-detección millar: 1900 + 1442")
    resultado = compensacion_base10_suma(1900, 1442)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Ejemplo 9: Progresivo - primera aplicación a decena
    print("\n9️⃣ Progresivo (paso 1): 1887 + 1455")
    resultado = compensacion_base10_suma(1887, 1455)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
