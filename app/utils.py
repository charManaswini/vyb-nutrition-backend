def safe_get_weight(entry, fallback=50):
    """
    Converts raw weight into a human-readable household quantity.
    Returns integer grams and also stores a 'friendly_quantity' string.
    """
    weight = entry.get("weight_in_grams", fallback)

    if not isinstance(weight, (int, float)):
        try:
            weight = int(weight)
        except:
            weight = fallback

    # Friendly quantity mapping based on real units
    if weight <= 5:
        unit = "teaspoon"
        approx_qty = round(weight / 5, 1)
    elif weight <= 15:
        unit = "tablespoon"
        approx_qty = round(weight / 15, 1)
    elif weight <= 100:
        unit = "katori (150ml)"
        approx_qty = round(weight / 150, 2)
    elif weight <= 250:
        unit = "glass (250ml)"
        approx_qty = round(weight / 250, 2)
    else:
        unit = "grams"
        approx_qty = weight

    entry["friendly_quantity"] = f"{approx_qty} {unit}{'s' if approx_qty > 1 else ''} (≈ {weight}g)"
    return weight
