from typing import List

from constant import StatusOfAttack, UnitType


class WoundedUnit:
    def __init__(self):
        self.name: str = ""
        self.type: UnitType = None
        self.health: float = None


class SquadLog:
    def __init__(self):
        self.attacking: str = ""
        self.defending: str = ""
        self.status: StatusOfAttack = None
        self.damage: int = None
        self.all_dead: bool = False
        self.army_win: bool = False
        self.wounded_units: List[WoundedUnit] = []
        self.dead_units: List[WoundedUnit] = []


class ArmyLog:
    def __init__(self):
        self.attacking: str = ""
        self.defending: str = ""
        self.squad_logs: List[SquadLog] = []

