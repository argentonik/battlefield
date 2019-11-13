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

    def test_is_alive(self):
        self.assertTrue(self.vehicle.is_alive())

    def test_is_not_alive_when_it_health_equal_null(self):
        self.vehicle.health = 0
        self.assertFalse(self.vehicle.is_alive())

    def test_is_not_alive_when_operators_died(self):
        self.vehicle.operators = []
        self.assertFalse(self.vehicle.is_alive())

    def test_get_take_damage_return_correct_value(self):
        self.assertGreaterEqual(self.vehicle.take_damage(), 0)
        self.assertLessEqual(self.vehicle.take_damage(), 100)

    def test_get_attack_success_probability_return_correct_value(self):
        self.assertGreaterEqual(self.vehicle.get_attack_success_probability(), 0)
        self.assertLessEqual(self.vehicle.get_attack_success_probability(), 1)

if __name__ == '__main__':
    unittest.main()
