# 🤖 AGENTS.md – Math Strategies Backend

## 🧠 Project Overview
This project is a **Python backend** that models and explains **mental math strategies** for basic arithmetic operations (addition, subtraction, multiplication, and division).  
Its purpose is **didactic**: to generate step-by-step reasoning processes (not just numeric results) that can later be displayed or visualized in an educational app.

The core idea:
```
79 + 25 → adjust 79 to 80 → compensate 25 to 24 → 80 + 24 = 104
```

The backend produces **structured JSON outputs** containing:
- The original operation  
- The chosen strategy (e.g., “compensation”)  
- A list of reasoning steps (each with level, adjustment, new operation, and explanation)  
- The final result  

---

## ⚙️ Agent Goals
When assisting in this repository, your goals are:
1. **Preserve clarity and educational intent** in the code and comments.  
2. **Encourage clean, modular design** — strategies should be easy to extend and plug in (e.g., Compensation, Decomposition, Rounding).  
3. **Favor explainability over optimization** — explicit steps and readable code are preferred to clever tricks.  
4. **Promote testability** — all strategy logic should be pure and deterministic.  
5. **Maintain consistent structure** for JSON outputs to simplify frontend integration.

---

## 🧩 Code Structure Guidelines
- Strategy logic in `suma_algoritmos.py` (currently: compensation)
- API endpoints in `api.py` (Flask REST)
- Tests in `test_api.py`
- Keep functions **pure** — no print statements in core logic
- Future: separate strategies into individual modules

---

## 🧱 Style & Conventions
- Follow **PEP 8** for naming and formatting.
- Use **type hints** throughout (e.g., `def compensate(a: int, b: int) -> dict:`).
- Write **docstrings** explaining both the math reasoning and code behavior.
- Prefer clear variable names (`adjustment`, `rounded_value`, `compensated_value`) over short ones.
- Comments should clarify the **math thinking process**, not just the code flow.

---

## 🧪 Testing
- Each strategy should include unit tests verifying:
  - Correct final results  
  - Correct structure of the step breakdown  
  - Logical consistency of the compensation process
- Use `pytest` for testing.
- Avoid hardcoding expected JSON strings — test key-value correctness.

---

## 🛠️ Current Status
- ✅ Compensation strategy with intelligent selection (weight-based ("peso"))
- ✅ Flask REST API with GET endpoints
- ✅ Auto-detection: decena/centena/unidad_de_millar
- ✅ Semantic JSON structure (`ajuste` / `compensacion`)
- 🔄 Frontend React (in progress)
- 📚 Future: decomposition, rounding, doubling/halving strategies

---

## 🧩 Example Agent Prompt
> "Add a new strategy for decomposition: break down numbers into place values.  
> Follow the same semantic JSON structure with `ajuste` and `compensacion` fields."

---

## 🧭 Summary
This project bridges **mathematical pedagogy** and **software engineering**.  
Agents should assist by producing **transparent, well-explained, extensible** code that combines educational insight with clean architecture.
