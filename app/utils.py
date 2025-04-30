def safe_get_weight(entry, fallback=50):
    weight = entry.get("weight_in_grams", fallback)

    if not isinstance(weight, (int, float)):
        try:
            weight = int(weight)
        except:
            weight = fallback

    # conversion
    if weight <= 10:
        unit = "teaspoon"
        approx_qty = round(weight / 5, 1)
    elif weight <= 50:
        unit = "tablespoon"
        approx_qty = round(weight / 15, 1)
    elif weight <= 180:
        unit = "cup"
        approx_qty = round(weight / 60, 1)
    else:
        unit = "grams"
        approx_qty = weight

    entry["friendly_quantity"] = f"{approx_qty} {unit}{'s' if approx_qty > 1 else ''} (≈ {weight}g)"
    return weight
