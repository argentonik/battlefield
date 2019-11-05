from typing import List

from loggers import ArmyLog
from model import Army, StatusOfAttack, UnitType

def print_line():
    print("--------------------------------------------------------------")


def print_init_stats(army: Army):
    print_line()
    print_line()
    print("ЧИСЛО ОТРЯДОВ В АРМИИ", army.name, "-", len(army.squads), "\n")
    for i, squad in enumerate(army.squads):
        print("В ОТРЯДЕ", i + 1, "-", len(squad.units), "ЮНИТОВ. СОЛДАТОВ -",
              squad.count_of_soldier(), "ТЕХНИКИ -", squad.count_of_vehicle())

def print_battle_log(battle_logs: List[ArmyLog]):
    for army_log in battle_logs:
        if len(army_log.squad_logs) == 0:
            break
        print("АРМИЯ", army_log.attacking, "АТАКУЕТ АРМИЮ", army_log.defending)
        for squad_log in army_log.squad_logs:
            print()
            if squad_log == None:
                break
            print("Отряд", squad_log.attacking, "напал на отряд",
                  squad_log.defending)
            if squad_log.status == StatusOfAttack.WIN:
                print("★★★ Атака удалась ★★★")
                print("Юниты отряда", squad_log.defending, "получили по",
                      round(squad_log.damage, 1), "урона.")
                if squad_log.all_dead:
                    print("ОТРЯД", squad_log.defending, "УБИТ")
                    if squad_log.army_win:
                        print("АРМИЯ", army_log.attacking, "ПОБЕДИЛА")
                        print_line()
                    break
                print("Текущее здоровье юнитов отряда", squad_log.defending,
                      ":")
                for unit in squad_log.wounded_units:
                    print("\t-", "солдат" if unit.type == UnitType.SOLDIER else
                    "танк", unit.name, ":", round(unit.health, 1))
                for unit in squad_log.dead_units:
                    print("\t-", "солдат" if unit.type == UnitType.SOLDIER else
                    "танк", unit.name, ": убит")
            else:
                print("✘✘✘ Атака не удалась ✘✘✘")
        print_line()

def print_battle_log_from_json(battle_logs: List[ArmyLog]):
    for army_log in battle_logs:
        if len(army_log['squad_logs']) == 0:
            break
        print("АРМИЯ", army_log['attacking'], "АТАКУЕТ АРМИЮ",
              army_log['defending'])
        for squad_log in army_log['squad_logs']:
            print()
            if squad_log == None:
                break
            print("Отряд", squad_log['attacking'], "напал на отряд",
                  squad_log['defending'])

            if squad_log['status']['value'] == 0:
                print("★★★ Атака удалась ★★★")
                print("Юниты отряда", squad_log['defending'], "получили по",
                      round(squad_log['damage'], 1), "урона.")
                if squad_log['all_dead']:
                    print("ОТРЯД", squad_log['defending'], "УБИТ")
                    if squad_log['army_win']:
                        print("АРМИЯ", army_log['attacking'], "ПОБЕДИЛА")
                        print_line()
                    break
                print("Текущее здоровье юнитов отряда", squad_log['defending'],
                      ":")
                for unit in squad_log['wounded_units']:
                    print("\t-", "солдат" if unit['type'] ==
                                             UnitType.SOLDIER else
                    "танк", unit['name'], ":", round(unit['health'], 1))
                for unit in squad_log['dead_units']:
                    print("\t-", "солдат" if unit['type'] ==
                                             UnitType.SOLDIER else
                    "танк", unit['name'], ": убит")
            else:
                print("✘✘✘ Атака не удалась ✘✘✘")
        print_line()