def convert_to_grams(quantity_str, unit_df, food_type="Wet Sabzi"):
    """
    Convert common unit (e.g., katori) into grams using food category mapping.
    """
    # Normalize column names (even if misspelled)
    unit_df.columns = unit_df.columns.str.strip().str.lower()
    
    # Fix potential column mismatches
    # Try fuzzy column correction if needed
    if "measuing units" in unit_df.columns:
        unit_df.rename(columns={"measuing units": "measuring_unit"}, inplace=True)
    if "weight cat" in unit_df.columns:
        unit_df.rename(columns={"weight cat": "weight"}, inplace=True)
    if "food category name" not in unit_df.columns:
        return 180  # fallback
    
    # Filter based on category and unit
    filtered = unit_df[unit_df["food category name"].str.lower() == food_type.lower()]
    row = filtered[filtered["measuring_unit"].str.lower() == "katori"]

    if not row.empty:
        weight_str = row["weight"].values[0]
        if isinstance(weight_str, str) and weight_str.endswith("g"):
            weight_str = weight_str.replace("g", "").strip()
        try:
            return int(weight_str)
        except:
            return 180
    return 180
