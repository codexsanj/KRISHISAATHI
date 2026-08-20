# KrishiSaathi — Frontend-Backend API Contract

This document specifies the exact contract between the React frontend and the FastAPI backend for the KrishiSaathi Smart Crop Advisory System.

---

## 1. Authentication

### `POST /api/auth/register`
- **Page:** `RegisterPage` (`src/pages/auth/RegisterPage.jsx`)
- **Component:** `RegisterPage`
- **Current Data Source:** Client state / `register()` in `AppProvider`
- **Request Schema:**
  ```json
  {
    "identifier": "string (+91 9876543210 or user@example.com)",
    "password": "string"
  }
  ```
- **Response Schema:**
  ```json
  {
    "access_token": "string",
    "token_type": "bearer",
    "farmer": {
      "id": "string",
      "name": "string",
      "phone": "string",
      "email": "string"
    }
  }
  ```
- **Loading State:** Button loading spinner (`isLoading={true}`)
- **Error State:** Error banner under inputs (`"Invalid credentials or user already exists"`)

### `POST /api/auth/login`
- **Page:** `LoginPage` (`src/pages/auth/LoginPage.jsx`)
- **Component:** `LoginPage`
- **Current Data Source:** Client state / `login()` in `AppProvider`
- **Request Schema:**
  ```json
  {
    "identifier": "string (+91 9876543210 or user@example.com)",
    "password": "string"
  }
  ```
- **Response Schema:**
  ```json
  {
    "access_token": "string",
    "token_type": "bearer",
    "farmer": {
      "id": "string",
      "name": "string",
      "phone": "string",
      "email": "string"
    },
    "farm": {
      "id": "string",
      "name": "string",
      "crop": "string",
      "area": "string",
      "location": "string",
      "soil": "string",
      "waterSource": "string",
      "status": "string"
    }
  }
  ```
- **Loading State:** Button loading spinner
- **Error State:** Error message banner

### `GET /api/auth/me`
- **Page:** Global / `AppProvider`
- **Headers:** `Authorization: Bearer <token>`
- **Response Schema:**
  ```json
  {
    "isAuthenticated": true,
    "onboardingComplete": true,
    "farmer": { "id": "string", "name": "string", "phone": "string", "email": "string" },
    "farm": { "id": "string", "name": "string", "crop": "string", "area": "string", "location": "string", "soil": "string", "waterSource": "string", "status": "string" }
  }
  ```
- **Loading State:** Global initial auth check
- **Error State:** Fallback to unauthenticated state

---

## 2. Onboarding & Farmer Profile

### `POST /api/farmer/onboard`
- **Page:** `OnboardingPage` (`src/pages/onboarding/OnboardingPage.jsx`)
- **Component:** `OnboardingPage`
- **Current Data Source:** Local component state -> `completeOnboarding()`
- **Request Schema:**
  ```json
  {
    "farmer": {
      "name": "string",
      "phone": "string"
    },
    "farm": {
      "name": "string",
      "area": "string",
      "crop": "string",
      "soil": "string",
      "waterSource": "string",
      "location": "string"
    }
  }
  ```
- **Response Schema:**
  ```json
  {
    "success": true,
    "farmer": { "id": "string", "name": "string", "phone": "string" },
    "farm": { "id": "string", "name": "string", "crop": "string", "area": "string", "location": "string", "soil": "string", "waterSource": "string", "status": "string" }
  }
  ```
- **Loading State:** Step 6 submit button loading state
- **Error State:** Error notification banner

---

## 3. Home Dashboard (`HomePage`)

### `GET /api/advisory/today`
- **Page:** `HomePage` (`src/pages/HomePage.jsx`)
- **Component:** `PriorityActionCard`
- **Current Data Source:** `DEMO_PRIORITY_ACTION` in `demoData.js`
- **Response Schema:**
  ```json
  {
    "iconLabel": "string (e.g. Pest risk)",
    "title": "string",
    "dueLabel": "string (e.g. Due by 4 PM)",
    "what": "string",
    "when": "string",
    "why": "string",
    "ctaLabel": "string"
  }
  ```

### `GET /api/analytics/dashboard`
- **Page:** `HomePage`
- **Component:** `FarmSnapshotCard` grid
- **Current Data Source:** `DEMO_FARM_SNAPSHOT` in `demoData.js`
- **Response Schema:**
  ```json
  {
    "weather": { "value": "32°C", "label": "Partly cloudy", "detail": "Rain likely tomorrow" },
    "irrigation": { "value": "Due", "label": "North field", "detail": "Rain expected tomorrow" },
    "cropHealth": { "value": "Healthy", "label": "2 of 3 fields", "detail": "No major issues" },
    "market": { "value": "Wheat", "label": "+4.2%", "detail": "Nearby mandi prices" }
  }
  ```

### `GET /api/alerts`
- **Page:** `HomePage`
- **Component:** `WeatherCard`, `RiskCard`
- **Current Data Source:** `DEMO_ALERTS` in `demoData.js`
- **Response Schema:**
  ```json
  [
    { "id": "1", "type": "weather", "title": "Rain advisory", "description": "Light showers expected..." },
    { "id": "2", "type": "pest", "title": "Pest activity rising", "description": "Regional cotton pest risk..." }
  ]
  ```

---

## 4. Saathi AI & What-If Simulation

### `POST /api/chat`
- **Page:** `SaathiPage` (`src/pages/SaathiPage.jsx`) / `SaathiChat`
- **Component:** `SaathiChat` (`src/components/saathi/SaathiChat.jsx`)
- **Current Data Source:** `getSaathiMockResponse()` in `demoData.js`
- **Request Schema:**
  ```json
  {
    "message": "string (e.g. 'Should I irrigate today?')",
    "farm_id": "optional string",
    "history": "array of previous messages"
  }
  ```
- **Response Schema:**
  ```json
  {
    "answer": "string",
    "structured": {
      "what": "string",
      "when": "string",
      "why": "string"
    },
    "confidence": 0.92,
    "sources": ["string"],
    "requires_expert": false,
    "is_what_if": false,
    "simulation": null
  }
  ```

### `POST /api/simulation`
- **Page:** `SaathiPage` / `FarmPage`
- **Component:** `SaathiChat` / `WhatIfSimulator`
- **Request Schema:**
  ```json
  {
    "query": "string (e.g. 'What if rainfall decreases by 20%, irrigation is reduced by 15%, and fertilizer cost increases by 10%?')",
    "farm_id": "optional string"
  }
  ```
- **Response Schema:**
  ```json
  {
    "parsed_params": {
      "rainfall_change_pct": -20.0,
      "irrigation_change_pct": -15.0,
      "fertilizer_cost_change_pct": 10.0,
      "crop_change": null
    },
    "current_state": {
      "crop": "Wheat",
      "yield_q_per_acre": 18.5,
      "water_req_mm": 450,
      "pest_risk": "Low",
      "input_cost_inr": 12000,
      "revenue_inr": 41625,
      "profit_inr": 29625
    },
    "simulated_state": {
      "crop": "Wheat",
      "yield_q_per_acre": 16.2,
      "water_req_mm": 382.5,
      "pest_risk": "Moderate",
      "input_cost_inr": 13200,
      "revenue_inr": 36450,
      "profit_inr": 23250
    },
    "deltas": {
      "yield_change_pct": -12.4,
      "water_change_pct": -15.0,
      "profit_change_pct": -21.5
    },
    "explanation": "What: Yield drops by 12.4% with ₹6,375 lower profit. When: Review before reducing irrigation. Why: Rainfall drop combined with reduced irrigation creates severe crop moisture stress during grain filling stage.",
    "structured": {
      "what": "Yield decreases to 16.2 q/acre (-12.4%) and profit drops by ₹6,375 (-21.5%).",
      "when": "Re-evaluate water management before skipping planned irrigation schedules.",
      "why": "Rainfall deficit (-20%) coupled with irrigation cut (-15%) limits soil moisture availability, reducing yield potential despite cost changes."
    }
  }
  ```

---

## 5. Crop Health, Disease & Pests

### `POST /api/health/disease-detect`
- **Page:** `HealthPage` (`src/pages/HealthPage.jsx`)
- **Component:** `AIRecommendationCard` / File Upload Modal
- **Request:** `multipart/form-data` with `file: File`, `crop: string`
- **Response Schema:**
  ```json
  {
    "prediction": "Cotton Leaf Blight",
    "confidence": 0.94,
    "severity": "Moderate",
    "what": "Spray copper oxychloride (3g/L of water) on affected leaves.",
    "when": "Apply within 24-48 hours during early morning hours.",
    "why": "Fungal infection detected with 94% confidence. Early intervention prevents field-wide spread.",
    "requires_expert": false,
    "bbox": null
  }
  ```

### `GET /api/pest/risk`
- **Page:** `HealthPage`
- **Component:** `RiskCard`
- **Response Schema:**
  ```json
  {
    "risk_level": "Moderate",
    "pest_type": "Pink Bollworm / Aphids",
    "probability": 0.65,
    "title": "Pest activity rising",
    "description": "Regional cotton pest risk is moderate this week due to warm humid weather."
  }
  ```

---

## 6. Market Intelligence

### `GET /api/market/current`
- **Page:** `MarketPage` (`src/pages/MarketPage.jsx`)
- **Component:** `MarketCard`
- **Response Schema:**
  ```json
  [
    {
      "crop": "Cotton",
      "mandi": "Bengaluru Local Mandi",
      "price_per_quintal": 6420,
      "date": "2026-08-20",
      "trend_pct": 3.2,
      "trend_direction": "up"
    }
  ]
  ```

### `GET /api/market/trends`
- **Page:** `MarketPage`
- **Component:** `StatCard`
- **Response Schema:**
  ```json
  {
    "crop": "Wheat",
    "recommendation": "Sell this week",
    "best_window": "Next 5-7 days",
    "price_trend": "+4.2% over last 14 days",
    "forecast": "Prices expected to peak this Friday before new arrivals hit mandis."
  }
  ```

---

## 7. Expert Escalation

### `POST /api/expert/cases`
- **Page:** `HealthPage` / `SaathiPage`
- **Request Schema:**
  ```json
  {
    "farmer_id": "string",
    "field_id": "optional string",
    "issue_description": "string",
    "image_url": "optional string",
    "confidence": 0.42
  }
  ```
- **Response Schema:**
  ```json
  {
    "case_id": "exp-1029",
    "status": "Escalated",
    "assigned_to": "KVK Agricultural Expert",
    "message": "Your query has been escalated to an expert. Expected response within 4 hours."
  }
  ```

---

## Fallback & Reliability Policy
If any backend service, model, or external API (Gemini, IMD weather, e-NAM market) is unavailable:
1. The backend returns a status flag `"is_fallback": true` along with `"data_source": "Cached Weather Adapter"` or `"Local Heuristic Rules Engine"`.
2. The response NEVER fails or returns 500 errors.
3. The frontend displays the fallback data with a clear label: *"Development/Cached fallback data — source: Local Agmet Engine"*.
