from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

# Load your Gemini API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

def fetch_recipe_ingredients(dish_name):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You're a nutrition assistant. "
                    "Given an Indian dish name, reply only in pure JSON array "
                    "of 5 key ingredients with estimated weight in grams, like:\n"
                    "[{\"name\": \"Ingredient\", \"weight_in_grams\": 100}, ...]"
                )
            ),
            contents=f"What are the 5 main ingredients of {dish_name} with estimated weights in grams?"
        )

        raw = response.text.strip()

        # Extract and parse only the JSON part
        json_start = raw.find("[")
        json_end = raw.rfind("]") + 1
        json_str = raw[json_start:json_end]

        ingredients = json.loads(json_str)
        return ingredients if isinstance(ingredients, list) else []

    except Exception as e:
        print("[Gemini Error]", str(e))
        return []
