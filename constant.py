import json
from enum import Enum

with open('conf.json') as data_file:
    conf = json.load(data_file)

for k, v in conf.items():
    exec("%s=%s" % (k, v))


class Strategy(Enum):
    RANDOM = 0
    WEAKEST = 1
    STRONGEST = 2


class StatusOfAttack(Enum):
    WIN = 0
    LOSE = 1
    RECHARGED = 2


class UnitType(Enum):
    SOLDIER = 0
    VEHICLE = 1