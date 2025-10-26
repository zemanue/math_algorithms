

import json


def compensacion_suma(a: int, b: int):
    """
    Aplica la estrategia de compensación a la suma a + b.
    Devuelve un diccionario con todos los pasos del razonamiento.

    La función elige el número más cercano a una decena (superior o inferior)
    y compensa el ajuste en el otro sumando para mantener la suma constante.
    """
    pasos = []
    original = (a, b)
    nivel = "decena"

    # 1️⃣ Calcular distancias a las decenas más cercanas (superior e inferior)
    resto_a = a % 10
    resto_b = b % 10

    # Si al menos uno ya es múltiplo de 10, no hay que ajustar nada.
    # El objetivo de la compensación es conseguir que UNO sea múltiplo de 10.
    if resto_a == 0 or resto_b == 0:
        resultado = a + b
        return {
            "operacion_original": f"{a} + {b}",
            "operandos": [a, b],
            "estrategia": "compensacion",
            "pasos": [],
            "resultado_final": resultado
        }

    # Para cada número, calculamos distancia a decena superior e inferior
    # y elegimos la más cercana

    # Para 'a':
    dist_a_superior = 10 - resto_a
    dist_a_inferior = resto_a

    if dist_a_inferior < dist_a_superior:
        # Más cerca de la decena inferior
        dist_a = dist_a_inferior
        ajuste_a = -dist_a_inferior  # Ajuste negativo (restar)
        decena_a = a - dist_a_inferior
    else:
        # Más cerca de la decena superior
        dist_a = dist_a_superior
        ajuste_a = dist_a_superior  # Ajuste positivo (sumar)
        decena_a = a + dist_a_superior

    # Para 'b':
    dist_b_superior = 10 - resto_b
    dist_b_inferior = resto_b

    if dist_b_inferior < dist_b_superior:
        # Más cerca de la decena inferior
        dist_b = dist_b_inferior
        ajuste_b = -dist_b_inferior  # Ajuste negativo (restar)
        decena_b = b - dist_b_inferior
    else:
        # Más cerca de la decena superior
        dist_b = dist_b_superior
        ajuste_b = dist_b_superior  # Ajuste positivo (sumar)
        decena_b = b + dist_b_superior

    # 2️⃣ Elegimos el número con menor distancia a su decena más cercana
    if dist_a <= dist_b:
        # Ajustamos 'a' a su decena más cercana
        num_a_ajustar = a
        ajuste = ajuste_a
        decena_objetivo = decena_a
        nuevo_a = decena_a
        nuevo_b = b - ajuste_a  # Compensamos en el otro número

        direccion = "sumamos" if ajuste_a > 0 else "restamos"
        otra_direccion = "sumamos" if direccion == "restamos" else "restamos"
        valor_abs = abs(ajuste_a)
        comentario = (
            f"Ajustamos {num_a_ajustar} a {decena_objetivo} "
            f"({direccion} {valor_abs})"
            f" y compensamos el otro sumando de {b} a {nuevo_b} "
            f"({otra_direccion} {valor_abs})."
        )

    else:
        # Ajustamos 'b' a su decena más cercana
        num_a_ajustar = b
        ajuste = ajuste_b
        decena_objetivo = decena_b
        nuevo_a = a - ajuste_b  # Compensamos en el otro número
        nuevo_b = decena_b

        direccion = "sumamos" if ajuste_b > 0 else "restamos"
        otra_direccion = "sumamos" if direccion == "restamos" else "restamos"
        valor_abs = abs(ajuste_b)
        comentario = (
            f"Ajustamos {num_a_ajustar} a {decena_objetivo} "
            f"({direccion} {valor_abs})"
            f" y compensamos el otro sumando de {a} a {nuevo_a} "
            f"({otra_direccion} {valor_abs})."
        )

    pasos.append({
        "nivel": nivel,
        "ajuste": abs(ajuste),
        "direccion_ajuste": "superior" if ajuste > 0 else "inferior",
        "operando_a_ajustar": num_a_ajustar,
        "decena_objetivo": decena_objetivo,
        "otro_operando": nuevo_b if num_a_ajustar == a else nuevo_a,
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
    print(json.dumps(compensacion_suma(17, 78), indent=2, ensure_ascii=False))
