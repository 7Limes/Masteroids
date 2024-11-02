def wrap(x: float, lower: float, upper: float) -> float:
    return lower + (x - lower) % (upper - lower)