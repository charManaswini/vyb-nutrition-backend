def safe_get_weight(entry, fallback=50):
    try:
        return int(entry.get("weight_in_grams", fallback))
    except:
        return fallback
