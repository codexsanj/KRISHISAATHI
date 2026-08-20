# 🌱 KrishiSaathi

## Smart Crop Advisory System for Small and Marginal Farmers

> **Data → Intelligence → Decision → Action**

KrishiSaathi is an AI-powered, farmer-first agricultural decision-support platform designed to help small and marginal farmers make timely, personalized and informed farming decisions.

Instead of simply displaying agricultural information, KrishiSaathi combines:

**Farm + Soil + Crop + Weather + Market + Crop Health**

to generate actionable recommendations that answer three simple questions:

> **What should I do?**  
> **When should I do it?**  
> **Why should I do it?**

---

## 🏆 Smart India Hackathon 2026

| | |
|---|---|
| **Problem Statement** | SIH260491 |
| **Title** | Smart Crop Advisory System for Small and Marginal Farmers |
| **Organisation** | Government of Punjab |
| **Theme** | Agriculture, FoodTech & Rural Development |
| **Category** | Software |
| **Competition** | Smart India Hackathon 2026 |

---

# 📌 Architecture & Decision Flow

```text
FARMER
  │
  ▼
REACT FRONTEND (PWA Ready + Mobile First)
  │ (REST APIs)
  ▼
FASTAPI BACKEND MONOLITH
  ├── Auth & JWT Security (RBAC)
  ├── Relational DB Memory (PostgreSQL / SQLAlchemy)
  ├── Saathi Intelligence Router
  │     ├── Natural Language What-If Simulation Engine (Transient In-Memory State Cloner)
  │     ├── Deterministic Irrigation Decision Engine
  │     ├── PyTorch / OpenCV Leaf Disease Scanner (Auto Expert Escalation)
  │     ├── XGBoost Pest Risk Outbreak Predictor
  │     ├── Agmarknet / e-NAM Market Intelligence Adapter
  │     └── Grounded ICAR / KCC FAISS RAG Retrieval Engine
  └── Fallback Intelligence Providers (100% Offline Demo Reliability)
```

---

# ⚡ Quickstart Guide (Local Development)

### 1. Run FastAPI Backend

```bash
cd backend
pip install -r requirements.txt
python scripts/seed_database.py
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger API documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### 2. Run React Frontend

```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

### 3. Run Backend Test Suite

```bash
cd backend
pytest tests/
```

### 4. Run Docker Architecture

```bash
docker-compose up --build
```

---

# 🔮 Core Differentiators

- **Saathi AI Companion**: Answers questions with structured **WHAT**, **WHEN**, **WHY** guidance.
- **Natural Language What-If Engine**: Simulates multi-variable scenarios (e.g. *"What if rainfall decreases by 20%, irrigation is reduced by 15%, and fertilizer cost increases by 10%?"*) without modifying the real farm database.
- **Explainable AI (SHAP)**: Provides clear explanations for crop and irrigation recommendations.
- **Demo Reliability Mode**: Built-in fallback providers for Weather, Market, LLM, and CV models guarantee flawless demo performance even when offline.