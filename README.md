# 🌱 KrishiSaathi Backend Service

FastAPI Backend & Agricultural Decision Intelligence Engine for KrishiSaathi.

## 🚀 Quickstart (Local Development)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Seed Database
```bash
python scripts/seed_database.py
```

### 3. Run FastAPI Backend Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
The API documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### 4. Run Pytest Test Suite
```bash
pytest tests/
```

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

---

## 🌾 Intelligence Subsystems & Fallback Policy

| Subsystem | Primary Engine | Local Fallback Provider |
|---|---|---|
| **Weather Adapter** | IMD / AgMet Data Source | Local AgMet Development Provider |
| **Market Intelligence** | Agmarknet / e-NAM API | Mandi Market Trend Provider |
| **Irrigation Advisory** | Deterministic Decision Engine | Soil Water Capacity Rule Engine |
| **Crop Recommendation** | Scikit-learn / XGBoost + SHAP | ICAR Agro-Climatic Matrix |
| **Disease Detection** | PyTorch ResNet-18 Leaf Classifier | OpenCV / Rule-based Diagnostic Fallback |
| **Pest Outbreak Risk** | XGBoost Pest Model | Temperature-Humidity Risk Matrix |
| **Natural Language What-If** | Scenario Parser & Farm State Cloner | Transient Memory State Engine |
| **Saathi Chat Assistant** | Gemini 1.5 Flash + FAISS RAG | Grounded Local Advisory Engine |
