

def compensacion_suma(a: int, b: int):
    """
    Aplica la estrategia de compensación a la suma a + b.
    Devuelve un diccionario con todos los pasos del razonamiento.
    """
    pasos = []
    original = (a, b)
    nivel = "decena"

    # 1️⃣ Encontrar el número más cercano a una decena
    # Decenas: si se dividen entre 10, el resto es 0
    # Objetivo: calcular la diferencia al múltiplo de 10 superior
    resto_a = a % 10
    resto_b = b % 10

    # Si ya son múltiplos de 10, no hay que ajustar nada.
    if resto_a == 0 and resto_b == 0:
        resultado = a + b
        return {
            "operacion_original": f"{a} + {b}",
            "estrategia": "compensacion",
            "pasos": [],
            "resultado_final": resultado
        }

    # Seguimos: elegimos el número que esté más cerca del múltiplo de 10
    dif_a = 10 - resto_a if resto_a != 0 else 0
    dif_b = 10 - resto_b if resto_b != 0 else 0

    if dif_a <= dif_b:
        # Ajustamos 'a'
        num_a_ajustar = a
        ajuste = dif_a
        nuevo_a = a + ajuste
        nuevo_b = b - ajuste
    else:
        # Ajustamos 'b'
        num_a_ajustar = b
        ajuste = dif_b
        nuevo_a = a - ajuste
        nuevo_b = b + ajuste

    comentario = (
        f"Ajustamos {num_a_ajustar} al múltiplo de 10 más cercano (+{ajuste}) "
        f"y restamos {ajuste} al otro número."
    )

    pasos.append({
        "nivel": nivel,
        "ajuste": ajuste,
        "numero_a_ajustar": num_a_ajustar,
        "nuevo_numero": nuevo_a if dif_a <= dif_b else nuevo_b,
        "otro_numero": nuevo_b if dif_a <= dif_b else nuevo_a,
        "nueva_operacion": f"{nuevo_a} + {nuevo_b}",
        "comentario": comentario
    })

    resultado_final = nuevo_a + nuevo_b

    return {
        "operacion_original": f"{original[0]} + {original[1]}",
        "estrategia": "compensacion",
        "pasos": pasos,
        "resultado_final": resultado_final
    }


# Ejemplo de uso
if __name__ == "__main__":
    print(compensacion_suma(79, 25))
