from fuzzywuzzy import process

class IngredientMapper:
    def __init__(self, nutrition_df):
        self.nutrition_df = nutrition_df
        self.ingredient_names = nutrition_df["food_name"].dropna().unique().tolist()

    def match(self, raw_ingredient):
        match, score = process.extractOne(raw_ingredient, self.ingredient_names)
        return {
            "input": raw_ingredient,
            "matched_ingredient": match,
            "confidence_score": score
        }

    def bulk_match(self, ingredient_list):
        return [self.match(item) for item in ingredient_list]
