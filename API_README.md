# 🧮 Math Algorithms API

API REST en Flask para estrategias de cálculo mental educativo.

## 🚀 Inicio Rápido

```bash
pip install -r requirements.txt
python api.py
```

Servidor: `http://localhost:5000`

## 📡 Endpoints

### `GET /api/health`
Health check.

### `GET /api/suma/compensacion_base10/<operacion>`

Calcula compensación en base 10.

**Ejemplos:**
```
/api/suma/compensacion_base10/79+25
/api/suma/compensacion_base10/290+603?nivel=centena
```

**Response:**
```json
{
  "operacion_original": "79 + 25",
  "estrategia": "compensacion_base10",
  "pasos": [{
    "nivel": "decena",
    "ajuste": { "de": 79, "a": 80, "cantidad": 1 },
    "compensacion": { "de": 25, "a": 24, "cantidad": -1 },
    "nueva_operacion": "80 + 24",
    "comentario": "..."
  }],
  "resultado_final": 104
}
```

### `GET /api/suma/compensacion_base10/ejemplos`
Ejemplos precalculados.

## 🧪 Uso

**JavaScript:**
```javascript
const res = await fetch('http://localhost:5000/api/suma/compensacion_base10/79+25');
const data = await res.json();
console.log(data.pasos[0].ajuste); // { de: 79, a: 80, cantidad: 1 }
```

**Python:**
```python
import requests
r = requests.get('http://localhost:5000/api/suma/compensacion_base10/79+25')
print(r.json()['pasos'][0]['ajuste'])
```

## 📝 Tests
```bash
python test_api.py
```
