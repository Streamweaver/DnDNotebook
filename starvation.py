# These are some simple functions to simulation the results of starvation rules under
import numpy as np


class NoFoodException(Exception):
    pass


class Forager:

    def __init__(self, wis_mod, con_mod, lbs_food_per_day, survival_bonus):
        """

        :param wis_mod: int of wisdom modifier
        :param con_mod: int of con modifier
        :param lbs_food_per_day: float of pounds of food needed per day.
        :param survival_bonus: int of survival bonus
        """
        self.wis_mod = wis_mod
        self.con_mod = con_mod
        self.food_per_day = float(lbs_food_per_day)
        self.survival_bonus = survival_bonus
        self.exhaustion_level = 0
        self.food = 0.0
        self.fed = True
        self.days_without_food = 0.0
        self.is_alive = True

    def is_starving(self):
        """
        Returns true if the character has gone without food for more than con_modifier + 3 days, min 1.
        :return: boolean if character is starving.
        """
        max_days = max([1, self.con_mod + 3])
        return self.days_without_food > max_days

    def eat(self):
        if self.food >= self.food_per_day:
            self.fed = True
            self.food -= self.food_per_day
            self.days_without_food = 0
        elif self.food >= float(self.food_per_day) * 0.5:
            self.fed = True
            self.food -= float(self.food_per_day) * 0.5
            self.days_without_food += 0.5
        else:
            self.fed = False
            self.days_without_food += 1

    def sleep(self):
        if self.fed:
            self.exhaustion_level = max(self.exhaustion_level - 1, 0)
        else:
            self.exhaustion_level += 1
        self.fed = False
        if self.is_starving():
            self.exhaustion_level += 1

    def forage(self, dc):
        pass

    def _check(self, bonus, dc, disadvantage):
        check = np.random.randint(1, 21)
        if disadvantage:
            check = max([check, np.random.randint(1, 21)])
        return check + bonus >= dc

    def con_check(self, dc):
        return self._check(self.con_mod, dc, self.exhaustion_level > 0)

    def wis_check(self, dc):
        return self._check(self.wis_mod, dc, self.exhaustion_level > 0)

    def survival_check(self, dc):
        return self._check(self.survival_bonus, dc, self.exhaustion_level > 0)


class Landscape:

    def __init__(self, dc):
        self.dc = dc
        self.people = []

    def add_person(self, person):
        self.people.append(person)

    def handle_day(self):
        # forage for food
        # eat food
        # check for starvation
        # rest
        pass