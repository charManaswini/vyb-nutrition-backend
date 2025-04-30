def classify_food_type(dish_name, food_cat_df):
    """
    Mock classifier using keyword matching.
    """
    dish_lower = dish_name.lower()

    if "gravy" in dish_lower or "masala" in dish_lower:
        return "Wet Sabzi"
    elif "fry" in dish_lower or "bhaji" in dish_lower:
        return "Dry Sabzi"
    elif "dal" in dish_lower:
        return "Dal"
    elif "chicken" in dish_lower or "mutton" in dish_lower:
        return "Non-Veg Curry"

    return "Unknown"
