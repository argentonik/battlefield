import random
from constant import *
from statistics import geometric_mean
from typing import List
from abc import ABC, abstractmethod

from loggers import SquadLog, ArmyLog, WoundedUnit

random.seed(SEED)

class Unit(ABC):
    def __init__(self):
        self.health: int = 100

    @abstractmethod
    def is_alive(self) -> bool:
        pass

    @abstractmethod
    def get_attack_success_probability(self) -> float:
        pass

    @abstractmethod
    def take_damage(self) -> float:
        return 0

    @abstractmethod
    def get_damage(self, damage: float):
        return 0


class Soldier(Unit):
    def __init__(self):
        Unit.__init__(self)
        self.experience: int = 0

    def is_alive(self) -> bool:
        return self.health > 0

    def get_attack_success_probability(self) -> float:
        res = 0.5 * (1 + self.health/100) * random.randint(
                50, 100) / 100
        return res

    def take_damage(self) -> float:
        damage = 5 + random.randint(0, self.experience)
        self.experience += 1
        return damage

    def get_damage(self, damage: float):
        self.health -= random.uniform(damage - 5, damage + 5)



class Vehicle(Unit):
    def __init__(self):
        Unit.__init__(self)
        self.health = 100
        self.operators: List[Soldier] = []

        self.__init_operators()

    def __init_operators(self):
        for i in range(random.randint(MIN_OPERATORS_PER_VEHICLE,
                       MAX_OPERATORS_PER_VEHICLE)):
            self.operators.append(Soldier())

    def __is_some_operator_alive(self) -> bool:
        for operator in self.operators:
            if operator.is_alive():
                return True
        return False

    def __get_operators_attack_success_probability_list(self) -> List[float]:
        attack_success_probability_list: [float] = []
        for operator in self.operators:
            attack_success_probability_list.append(
                operator.get_attack_success_probability())
        return attack_success_probability_list

    def __get_sum_operators_experience(self) -> int:
        total: int = 0
        for operator in self.operators:
            total += operator.experience
        return total

    def is_alive(self) -> bool:
        return self.health > 0 and self.__is_some_operator_alive()

    def get_attack_success_probability(self) -> float:
        res = 0.5 * (1 + self.health / 100) * geometric_mean(
            self.__get_operators_attack_success_probability_list())
        return res

    def take_damage(self) -> float:
        return 10 + float(self.__get_sum_operators_experience()) / 5

    def get_damage(self, damage: float):
        index_of_hurted_operator = random.randint(0, len(self.operators) - 1)
        self.health -= damage * random.uniform(0.1, 0.3)
        self.operators[index_of_hurted_operator].health -= damage * 0.8
        if not self.operators[index_of_hurted_operator].is_alive():
            self.operators.remove(self.operators[index_of_hurted_operator])
        for i, operator in enumerate(self.operators[:]):
            if i == index_of_hurted_operator:
                break
            operator.health -= damage * 0.1
            if not operator.is_alive():
                self.operators.remove(operator)


class Squad(Unit):
    def __init__(self, opponents, strategy: Strategy, name="name",
                 army_name="army_name"):
        self.name = name
        self.army_name = army_name
        self.opponents: Army = opponents
        self.strategy = strategy
        self.units: List[Unit] = []
        self.current_opponent: Squad = None
        self.__init_units()

    def __init_units(self):
        for i in range(random.randint(MIN_UNITS_PER_SQUAD,
                                      MAX_UNITS_PER_SQUAD)):
            self.units.append(Soldier() if i % 2 == 0 else Vehicle())

    def __choose_opponent(self):
        if self.strategy == Strategy.RANDOM:
            self.current_opponent = self.opponents.squads[
            random.randint(0, len(self.opponents.squads) - 1)]
        elif self.strategy == Strategy.STRONGEST:
            self.current_opponent = self.__get_strongest_opponent()
        elif self.strategy == Strategy.WEAKEST:
            self.current_opponent = self.__get_weakest_opponent()

    def __get_strongest_opponent(self):
        strongest: Squad = self.opponents.squads[0]
        for unit in self.opponents.squads[1:]:
            if unit.take_damage() > strongest.take_damage():
                strongest = unit
        return strongest

    def __get_weakest_opponent(self):
        weakest: Squad = self.opponents.squads[0]
        for unit in self.opponents.squads[1:]:
            if unit.take_damage() < weakest.take_damage():
                strongest = unit
        return weakest

    def __get_wounded_units_to_log(self) -> List[WoundedUnit]:
        units: List[WoundedUnit] = []
        for i, unit in enumerate(self.current_opponent.units):
            wounded_unit = WoundedUnit()
            wounded_unit.name = i + 1
            wounded_unit.type = UnitType.SOLDIER if type(unit) is Soldier \
                else UnitType.VEHICLE
            wounded_unit.health = unit.health
            units.append(wounded_unit)
        return units

    def count_of_soldier(self):
        count = 0
        for unit in self.units:
            if type(unit) is Soldier:
                count += 1
        return count

    def count_of_vehicle(self):
        return len(self.units) - self.count_of_soldier()

    def is_alive(self) -> bool:
        for unit in self.units:
            if unit.is_alive():
                return True
        return False

    def get_attack_success_probability(self) -> float:
        all_attacks = []
        try:
            for unit in self.units:
                attack_probability = unit.get_attack_success_probability()
                all_attacks.append(unit.get_attack_success_probability())
            res = geometric_mean(all_attacks)
        except ValueError:
            res = 0
        return res

    def take_damage(self) -> float:
        damage = 0
        for unit in self.units:
            damage += unit.take_damage()
        return damage

    def get_damage(self, damage: float) -> List[WoundedUnit]:
        damage_for_each = damage / len(self.units)
        dead_units: List[WoundedUnit] = []
        for i, unit in enumerate(self.units[:]):
            unit.get_damage(damage_for_each)
            if not unit.is_alive():
                dead_unit = WoundedUnit()
                dead_unit.name = i + 1
                dead_unit.type = UnitType.SOLDIER if type(unit) is Soldier \
                    else UnitType.VEHICLE
                dead_units.append(dead_unit)
                self.units.remove(unit)
        return dead_units

    def attack(self) -> SquadLog:
        if not self.opponents.is_alive():
            return
        self.__choose_opponent()

        log = SquadLog()
        log.attacking = self.name
        log.defending = self.current_opponent.name

        if not self.get_attack_success_probability() > \
               self.current_opponent.get_attack_success_probability():
            log.status = StatusOfAttack.LOSE
            return log

        damage = self.take_damage() / len(self.units)
        log.dead_units = self.current_opponent.get_damage(damage)
        if not self.current_opponent.is_alive():
            log.all_dead = True
            self.opponents.squads.remove(self.current_opponent)
        if not self.opponents.is_alive():
            log.army_win = True
        log.damage = damage
        log.wounded_units = self.__get_wounded_units_to_log()

        log.status = StatusOfAttack.WIN
        return log


class Army:
    def __init__(self, name: str = 'A'):
        self.name = name
        self.squads: List[Squad] = []
        self.opponent: Army = None

    def init_squads(self, strategy: Strategy = Strategy.RANDOM):
        for i in range(random.randint(MIN_SQUADS_NUMBER, MAX_SQUADS_NUMBER)):
            self.squads.append(Squad(self.opponent, strategy, name=str(i + 1),
                                     army_name=self.name))

    def is_alive(self) -> bool:
        for squad in self.squads:
            if squad.is_alive():
                return True
        return False

    def attack(self) -> ArmyLog:
        log = ArmyLog()
        log.attacking = self.name
        log.defending = self.opponent.name
        for squad in self.squads:
            log.squad_logs.append(squad.attack())
        return log

