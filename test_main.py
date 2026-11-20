import unittest

from main import (
    array_operations,
    celsius_to_fahrenheit,
    generate_forces,
    generate_temperatures,
    pressure_from_force,
)


class ApplicationTests(unittest.TestCase):
    def test_formula(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(0), 32)
        self.assertAlmostEqual(celsius_to_fahrenheit(100), 212)

    def test_array_operations(self):
        values = [3, 1, 2]
        operations = array_operations(values)
        self.assertEqual(operations["sorted"], [1, 2, 3])
        self.assertEqual(operations["minimum"], 1)
        self.assertEqual(operations["maximum"], 3)
        self.assertEqual(operations["average"], 2)

    def test_random_array_has_at_least_50_values(self):
        values = generate_temperatures()
        self.assertGreaterEqual(len(values), 50)

    def test_random_forces_have_at_least_50_values(self):
        forces = generate_forces()
        self.assertGreaterEqual(len(forces), 50)
        self.assertTrue(all(10 <= force <= 1000 for force in forces))

    def test_pressure_formula(self):
        self.assertAlmostEqual(pressure_from_force(100, 0.01), 10000)
        with self.assertRaises(ValueError):
            pressure_from_force(100, 0)


if __name__ == "__main__":
    unittest.main()
