from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS

from .ingredient_mapper import IngredientMapper
from .nutrition_calculator import NutritionCalculator
from .recipe_fetcher import fetch_recipe_ingredients
from .food_type_classifier import classify_food_type
from .unit_converter import convert_to_grams
from .utils import safe_get_weight

app = Flask(__name__)
CORS(app)

# Load CSVs
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
nutrition_df = pd.read_csv(os.path.join(DATA_DIR, 'nutrition_source.csv'))
unit_df = pd.read_csv(os.path.join(DATA_DIR, 'unit_of_measurements.csv'))
food_cat_df = pd.read_csv(os.path.join(DATA_DIR, 'food_categories.csv'))

# Clean column names (important)
nutrition_df.columns = nutrition_df.columns.str.strip().str.lower()
unit_df.columns = unit_df.columns.str.strip().str.lower()
food_cat_df.columns = food_cat_df.columns.str.strip().str.lower()

# Setup helpers
ingredient_mapper = IngredientMapper(nutrition_df)
nutrition_calculator = NutritionCalculator(nutrition_df)

@app.route("/")
def home():
    return "VYB Nutrition API is running!"

@app.route("/api/nutrition", methods=["POST"])
def estimate_nutrition():
    try:
        dish_name = request.json.get("dish")
        if not dish_name:
            return jsonify({"error": "No dish provided"}), 400

        # Step 1: Fetch ingredients for the dish
        raw_ingredients = fetch_recipe_ingredients(dish_name)
        if not raw_ingredients:
            return jsonify({"error": f"No recipe found for '{dish_name}'"}), 404

        # Step 2: Fuzzy match and attach quantity
        matched = []
        for item in raw_ingredients:
            match = ingredient_mapper.match(item["name"])
            match["weight_in_grams"] = safe_get_weight(item)
            matched.append(match)

        # Step 3: Nutrition per ingredient
        total_nutrition = nutrition_calculator.estimate_total_nutrition(matched)

        # Step 4: Serving scaling
        cooked_weight = sum(item["weight_in_grams"] for item in matched)
        food_type = classify_food_type(dish_name, food_cat_df)
        std_serving_weight = convert_to_grams("1 katori", unit_df, food_type)
        scale = std_serving_weight / cooked_weight if cooked_weight else 1
        scaled = {k: round(v * scale, 2) for k, v in total_nutrition.items()}

        return jsonify({
            "estimated_nutrition_per_200ml_katori": scaled,
            "dish_type": food_type,
            "ingredients_used": [
                {
                    "original": i["input"],
                    "ingredient": i["matched_ingredient"],
                    "match_confidence": i["confidence_score"],
                    "quantity": i.get("friendly_quantity", f'{i["weight_in_grams"]}g')
                } for i in matched
            ]
        })

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
