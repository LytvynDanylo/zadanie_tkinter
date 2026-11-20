import random

def celsius_to_fahrenheit(value):
    return value * 1.8 + 32


def generate_temperatures(count=60, seed=None):
    rng = random.Random(seed)
    return [round(rng.uniform(-20.0, 40.0), 1) for _ in range(count)]


def pressure_from_force(force, area):
    if area <= 0:
        raise ValueError("Musi byt vacsia ako nula")
    return force / area


def generate_forces(count=60, seed=None):
    rng = random.Random(seed)
    return [round(rng.uniform(10.0, 1000.0), 1) for _ in range(count)]


def array_operations(values):
    return {
        "sorted": sorted(values),
        "average": sum(values) / len(values),
        "minimum": min(values),
        "maximum": max(values),
    }
