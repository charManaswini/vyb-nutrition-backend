# 🍲 VYB Nutrition Backend API

## 🔍 Problem Statement
Build a system that estimates the nutritional value per standard serving of a given home-cooked Indian dish.

## 🧠 What This Does
- Fetches estimated recipe ingredients using Gemini AI
- Maps ingredients to a nutrition dataset (IFCT-2017)
- Converts quantities using household measurements
- Calculates nutrition per 100g → scales to 1 standard serving (e.g., 1 katori = 180g)
- Classifies dish type (e.g., Wet Sabzi, Dal) or logs 'Unknown' if ambiguous

## ✅ Files and Responsibilities
- `api.py` — Main entry API (Flask app)
- `ingredient_mapper.py` — Handles fuzzy ingredient mapping
- `recipe_fetcher.py` — Uses Gemini LLM to fetch core ingredients with quantities
- `nutrition_calculator.py` — Calculates nutrition using sum-product logic
- `unit_converter.py` — Maps household units to grams (e.g., 1 tablespoon ≈ 15g)
- `food_type_classifier.py` — Classifies dish type via keyword-based logic
- `utils.py` — Utility methods for fallback handling

## ⚠️ Edge Case Handling
- Logs `"Unknown"` if classification or ingredient matching fails
- Avoids crashes with safe fallbacks and default assumptions
- All failures handled silently with warnings — as required in assignment

## 🌐 Deployment
- ✅ Hosted on Render: [https://vyb-nutrition-backend.onrender.com](https://vyb-nutrition-backend.onrender.com)
- Endpoint: `POST /api/nutrition`
- Example Payload:
```json
{ "dish": "Paneer Butter Masala" }
```

## 🧪 Test Dishes Supported
- Paneer Butter Masala
- Rajma
- Dal Tadka
- Chole
- Vegetable Fry

## 📦 Requirements
```
flask
pandas
fuzzywuzzy
python-Levenshtein
google-generativeai
python-dotenv
flask-cors
```

---

> 👩‍💻 Built with ❤️ and AI to assist every Indian home.