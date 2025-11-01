# 🧮 Math Algorithms

Backend Python para modelar estrategias de cálculo mental con fines educativos.

## 🎯 Objetivo

Generar **procesos de razonamiento paso a paso** para operaciones aritméticas básicas, no solo resultados numéricos. Ideal para aplicaciones educativas que enseñan matemáticas mentales.

## ✨ Características

- **Compensación en base 10**: Ajusta números a múltiplos redondos (10, 100, 1000)
- **API REST Flask**: Endpoints listos para consumir desde frontend
- **Estructura semántica**: JSON optimizado para educación
- **Tests automatizados**: Suite completa de pruebas

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar API
python api.py

# Probar en navegador
http://localhost:5000/api/suma/compensacion_base10/79+25
```

## 📊 Ejemplo

**Input:** `79 + 25`

**Output:**
```json
{
  "operacion_original": "79 + 25",
  "pasos": [{
    "nivel": "decena",
    "ajuste": { "de": 79, "a": 80, "cantidad": 1 },
    "compensacion": { "de": 25, "a": 24, "cantidad": -1 },
    "nueva_operacion": "80 + 24"
  }],
  "resultado_final": 104
}
```

**Razonamiento:**
```
79 + 25  →  ajusto 79 a 80 (+1)
         →  compenso 25 a 24 (-1)
         →  80 + 24 = 104
```

## 📁 Estructura

```
├── suma_algoritmos.py          # Lógica de estrategias
├── api.py                      # API REST Flask
├── test_api.py                 # Tests
├── ejemplo_acceso_semantico.html  # Demo visual
└── API_README.md               # Documentación de la API
```

## 🧪 Tests

```bash
python test_api.py
```

## 📚 Documentación

- **[API_README.md](API_README.md)** - Documentación completa de endpoints
- **[AGENTS.md](AGENTS.md)** - Guía para agentes de IA

## 🎓 Uso Educativo

```javascript
// Ejemplo para app educativa
const paso = resultado.pasos[0];

// Acceso semántico intuitivo
paso.ajuste.de          // 79 (número original)
paso.ajuste.a           // 80 (número ajustado)
paso.ajuste.cantidad    // +1 (cambio aplicado)
```

## 🚧 Roadmap

- [x] Compensación en base 10
- [x] Auto-detección de nivel (decena/centena/millar)
- [x] API REST
- [ ] Frontend React
- [ ] Más estrategias (descomposición, redondeo)
- [ ] Sistema de ejercicios interactivos

## 📄 Licencia

MIT
