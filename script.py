import json

from encoder import ObjectEncoder
from model import *
from print_scripts import print_init_stats, print_line, print_battle_log, \
    print_battle_log_from_json

print("Играть или посмотреть лог прошлой игры? (p - играть, другое - лог)")
answer = input()
if answer == 'p':
    arm1 = Army(name='A')
    arm2 = Army(name='B')
    arm1.opponent = arm2
    arm2.opponent = arm1
    arm1.init_squads(Strategy.RANDOM)
    arm2.init_squads(Strategy.RANDOM)
    print_init_stats(arm1)
    print_init_stats(arm2)

    logs: List[ArmyLog] = []
    while arm1.is_alive() and arm2.is_alive():
        logs.append(arm1.attack())
        logs.append(arm2.attack())

    print_line()
    print_line()
    print_battle_log(logs)

    with open('game-log.json', 'w', encoding="utf-8") as f:
        json.dump(logs, f, cls=ObjectEncoder, ensure_ascii=False, indent=2,
                  sort_keys=True)
else:
    with open('game-log.json') as data_file:
        logs = json.load(data_file)

    print_battle_log_from_json(logs)



