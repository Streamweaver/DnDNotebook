import unittest
from starvation import Forager

class TestForager(unittest.TestCase):

    def setUp(self):
        self.person = Forager(0, 0, 1, 0)

    def test_is_starving(self):
        self.assertFalse(self.person.is_starving())
        self.person.days_without_food = 4
        self.assertTrue(self.person.is_starving())

    def test_eat(self):
        # Starts Fed and zero days w/o food.
        self.assertTrue(self.person.fed)
        self.assertEqual(self.person.days_without_food, 0)
        # Eat with no food
        self.person.eat()
        self.assertFalse(self.person.fed)
        self.assertEqual(self.person.days_without_food, 1)
        # Add a day and a half of food.
        self.person.food = 1.5
        self.person.eat()
        self.assertTrue(self.person.fed)
        self.assertEqual(self.person.days_without_food, 0)
        # Eat with half rations.
        self.person.eat()
        self.assertTrue(self.person.fed)
        self.assertEqual(self.person.days_without_food, 0.5)
        # Eat again
        self.person.eat()
        self.assertFalse(self.person.fed)
        self.assertEqual(self.person.days_without_food, 1.5)

    def test_sleep(self):
        self.assertEqual(self.person.exhaustion_level, 0)
        self.assertTrue(self.person.fed)
        self.person.sleep()
        self.assertEqual(self.person.exhaustion_level, 0)
        self.assertFalse(self.person.fed)
        self.person.sleep()
