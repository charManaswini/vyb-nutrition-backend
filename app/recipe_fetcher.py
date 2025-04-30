from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def fetch_recipe_ingredients(dish_name):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a nutrition assistant. "
                    "Given an Indian dish, return only a JSON array of 5 ingredients with both raw weight in grams "
                    "and estimated household quantity (e.g., '2 tablespoons', '1 cup chopped').\n"
                    "Format: [{\"name\": \"Ingredient\", \"weight_in_grams\": 100, \"household_quantity\": \"2 tablespoons\"}, ...]"
                )
            ),
            contents=f"What are the 5 main ingredients of {dish_name} with estimated weights and household measurements?"
        )

        raw = response.text.strip()
        json_start = raw.find("[")
        json_end = raw.rfind("]") + 1
        json_str = raw[json_start:json_end]

        ingredients = json.loads(json_str)
        return ingredients if isinstance(ingredients, list) else []

    except Exception as e:
        print("[Gemini Ingredient Error]", str(e))
        return []
