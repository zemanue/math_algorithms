"""
API Flask para estrategias de cálculo mental.
Expone endpoints REST para que el frontend React consuma la lógica de Python.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from suma_algoritmos import compensacion_base10_suma

app = Flask(__name__)

# Habilitar CORS para permitir peticiones desde React y HTML local
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "null"  # Para archivos HTML abiertos directamente
        ],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificar que la API está funcionando.

    Returns:
        JSON con status y mensaje
    """
    return jsonify({
        "status": "ok",
        "message": "API de estrategias de cálculo mental funcionando"
    }), 200


@app.route('/api/suma/compensacion_base10/<operacion>', methods=['GET'])
def compensacion_suma_endpoint(operacion):
    """
    Calcula la compensación en base 10 para una suma.

    URL Pattern:
        /api/suma/compensacion_base10/38+42?nivel=auto

    Path Parameters:
        operacion (str): Expresión de suma en formato "a+b" (ej: "38+42")

    Query Parameters:
        nivel (str, opcional): "auto" | "decena" | "centena" |
                              "unidad_de_millar"
                              Default: "auto"

    Ejemplos:
        GET /api/suma/compensacion_base10/290+603
        GET /api/suma/compensacion_base10/79+25?nivel=decena
        GET /api/suma/compensacion_base10/1887+1455?nivel=centena

    Response (JSON):
        {
            "operacion_original": "290 + 603",
            "estrategia": "compensacion_base10",
            "pasos": [
                {
                    "nivel": "centena",
                    "ajuste": {
                        "de": 290,
                        "a": 300,
                        "cantidad": 10
                    },
                    "compensacion": {
                        "de": 603,
                        "a": 593,
                        "cantidad": -10
                    },
                    "nueva_operacion": "300 + 593",
                    "comentario": "Ajustamos 290 a 300..."
                }
            ],
            "resultado_final": 893
        }

    Returns:
        JSON con el resultado de la compensación
    """
    try:
        # Parsear la operación "a+b"
        if '+' not in operacion:
            return jsonify({
                "error": "Formato inválido",
                "message": "La operación debe tener formato 'a+b' (ej: 38+42)"
            }), 400

        partes = operacion.split('+')
        if len(partes) != 2:
            return jsonify({
                "error": "Formato inválido",
                "message": "La operación debe tener exactamente dos sumandos"
            }), 400

        # Convertir a enteros
        try:
            a = int(partes[0].strip())
            b = int(partes[1].strip())
        except ValueError:
            return jsonify({
                "error": "Formato inválido",
                "message": "Los sumandos deben ser números enteros válidos"
            }), 400

        # Obtener nivel del query parameter (default: "auto")
        nivel = request.args.get('nivel', 'auto')

        # Validar nivel
        niveles_validos = ['auto', 'decena', 'centena', 'unidad_de_millar']
        if nivel not in niveles_validos:
            return jsonify({
                "error": "Nivel inválido",
                "message":
                    f"El nivel debe ser uno de: {', '.join(niveles_validos)}"
            }), 400

        # Ejecutar la función de compensación
        resultado = compensacion_base10_suma(a, b, nivel)

        return jsonify(resultado), 200

    except ValueError as e:
        return jsonify({
            "error": "Error de validación",
            "message": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "message": str(e)
        }), 500


@app.route('/api/suma/compensacion_base10/ejemplos', methods=['GET'])
def obtener_ejemplos():
    """
    Devuelve ejemplos precalculados de compensación.

    Returns:
        JSON con varios ejemplos de compensación
    """
    ejemplos = [
        {
            "nombre": "Decena superior",
            "operacion": "79 + 25",
            "resultado": compensacion_base10_suma(79, 25)
        },
        {
            "nombre": "Decena inferior",
            "operacion": "21 + 26",
            "resultado": compensacion_base10_suma(21, 26)
        },
        {
            "nombre": "Prioridad múltiplo de 10",
            "operacion": "70 + 83",
            "resultado": compensacion_base10_suma(70, 83)
        },
        {
            "nombre": "Ajuste pequeño gana",
            "operacion": "199 + 220",
            "resultado": compensacion_base10_suma(199, 220)
        },
        {
            "nombre": "Sin compensación necesaria",
            "operacion": "30 + 17",
            "resultado": compensacion_base10_suma(30, 17)
        }
    ]
    
    return jsonify({
        "total": len(ejemplos),
        "ejemplos": ejemplos
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Manejador para rutas no encontradas."""
    return jsonify({
        "error": "Endpoint no encontrado",
        "message": "La ruta solicitada no existe"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Manejador para errores internos."""
    return jsonify({
        "error": "Error interno del servidor",
        "message": str(error)
    }), 500


if __name__ == '__main__':
    print("🚀 Iniciando API Flask...")
    print("📍 Endpoints disponibles:")
    print("   - GET  http://localhost:5000/api/health")
    print("   - GET  http://localhost:5000/api/suma/"
          "compensacion_base10/290+603")
    print("   - GET  http://localhost:5000/api/suma/"
          "compensacion_base10/79+25?nivel=decena")
    print("   - GET  http://localhost:5000/api/suma/"
          "compensacion_base10/ejemplos")
    print("\n💡 Presiona Ctrl+C para detener el servidor\n")

    # Modo debug para desarrollo (auto-reload)
    app.run(debug=True, host='0.0.0.0', port=5000)
