class NutritionCalculator:
    def __init__(self, nutrition_df):
        self.nutrition_df = nutrition_df

    def get_nutrition_per_100g(self, ingredient_name):
        row = self.nutrition_df[self.nutrition_df["food_name"] == ingredient_name]
        if not row.empty:
            return {
                "calories": float(row["energy_kcal"].values[0]),
                "protein": float(row["protein_g"].values[0]),
                "carbs": float(row["carb_g"].values[0]),
                "fat": float(row["fat_g"].values[0])
            }
        else:
            return None

    def estimate_total_nutrition(self, matched_ingredients_with_quantities):
        total = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        for item in matched_ingredients_with_quantities:
            nutrition = self.get_nutrition_per_100g(item["matched_ingredient"])
            if nutrition:
                multiplier = item.get("weight_in_grams", 0) / 100
                total["calories"] += nutrition["calories"] * multiplier
                total["protein"] += nutrition["protein"] * multiplier
                total["carbs"] += nutrition["carbs"] * multiplier
                total["fat"] += nutrition["fat"] * multiplier
        return total
