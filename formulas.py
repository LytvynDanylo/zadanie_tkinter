import random

def celsius_to_fahrenheit(value):
    return value * 1.8 + 32


def generate_temperatures(count=60, seed=None):
    rng = random.Random(seed)
    return [round(rng.uniform(-20.0, 40.0), 1) for _ in range(count)]


def meters_to_miles(meters):
    return meters / 1609.344


def generate_distances(count=60, seed=None):
    rng = random.Random(seed)
    return [round(rng.uniform(100.0, 100000.0), 1) for _ in range(count)]


def array_operations(values):
    return {
        "sorted": sorted(values),
        "average": sum(values) / len(values),
        "minimum": min(values),
        "maximum": max(values),
    }
