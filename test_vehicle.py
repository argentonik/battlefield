import unittest

from model import Vehicle


class CalcTest(unittest.TestCase):
    MIN_OPERATORS_PER_VEHICLE = 1
    MAX_OPERATORS_PER_VEHICLE = 3

    def setUp(self):
        self.vehicle = Vehicle()

    def test_initial_properties(self):
        self.assertTrue(hasattr(self.vehicle, 'health'))
        self.assertTrue(hasattr(self.vehicle, 'operators'))

    def test_initial_health(self):
        self.assertEqual(self.vehicle.health, 100)

    def test_initial_operators(self):
        self.assertTrue(len(self.vehicle.operators) >= self.MIN_OPERATORS_PER_VEHICLE)
        self.assertTrue(len(self.vehicle.operators) <= self.MAX_OPERATORS_PER_VEHICLE)






if __name__ == '__main__':
    unittest.main()