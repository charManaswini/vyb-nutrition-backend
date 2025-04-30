from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def classify_food_type(dish_name, food_cat_df):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="Classify Indian dish into one of: 'Wet Sabzi', 'Dry Sabzi', 'Dal', 'Non-Veg Curry'."
            ),
            contents=f"Dish: {dish_name}. What type of Indian dish is this?"
        )
        result = response.text.strip().title()

        # Validate against categories
        valid = ["Wet Sabzi", "Dry Sabzi", "Dal", "Non-Veg Curry"]
        return result if result in valid else "Unknown"

    except Exception as e:
        print("[Gemini Food Type Error]", str(e))
        return "Unknown"
