from math import floor, ceil

def apply_rounding(value: float, rule: str) -> int:
    if rule == "floor":
        return floor(value)
    if rule == "ceil":
        return ceil(value)
    return round(value)
