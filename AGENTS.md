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
- Each strategy lives in its own Python module (e.g., `strategies/compensation.py`).
- Common interfaces and base classes should live in `strategies/base.py`.
- Example scripts for testing should go in `examples/`.
- Output examples (JSON) may be stored in `samples/` for reference.
- Keep functions **pure** — no print statements in core logic.

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

## 🛠️ Future Enhancements
- Extend compensation to hundreds, thousands, etc.  
- Add new strategies (e.g., decomposition, rounding, doubling/halving).  
- Implement subtraction and multiplication reasoning.  
- Integrate with a lightweight **API layer** (FastAPI) for interactive use.  
- Add a simple **frontend visualization** later on.

---

## 🧩 Example Agent Prompt
> “Create a new strategy class for subtraction using the ‘compensation’ method.  
> Follow the same JSON structure as in `compensation.py` and document each reasoning step clearly.”

---

## 🧭 Summary
This project bridges **mathematical pedagogy** and **software engineering**.  
Agents should assist by producing **transparent, well-explained, extensible** code that combines educational insight with clean architecture.
