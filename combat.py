import random, copy
from items import inventory_main
from actions import escape

def start_battle(ui, player, quality):
    enemies = player.enemies.values()
    enemy_list = [
        e for faction in enemies
        for e in faction if e.quality == quality
    ]
    if not enemy_list:
        enemy_list = [
            e for faction in enemies
            for e in faction if e.quality == 1
        ]
    if enemy_list:
        chosen_enemy = random.choice(enemy_list)
        chosen_enemy.dmg += chosen_enemy.weapon.dmg
        result = battle(ui, player, copy.deepcopy(chosen_enemy))
        return result
    return None

def battle(ui, player, enemy):
    ui.display(f"\nна тебя напал {enemy.name}")
    while player.hp > 0 and enemy.hp > 0:
        result = player_turn(ui, player, enemy)
        if result == "escaped":
            return "escaped"
        if result:
            return "won"
        ui.pause()
        if not enemy.can_move:
            ui.display("враг пропускает ход")
            continue
        if enemy.hp > 0:
            if enemy.attack(player, ui):
                return "death"
    return "error"

def player_turn(ui, player, enemy):
    while True:
        ui.display("\nтвой ход")
        ui.display("ты можешь посмотреть статистику врага, зайти в инвентарь, атаковать, парировать и попробовать сбежать")
        ui.display("напиши статистика, инвентарь, атака, парировать и бежать соответственно (можно цифрами)")
        choice = ui.get_input("> ").lower().strip()
        if choice in ["1", "статистика", "стат"]:
            ui.display(f"\nздоровье: {enemy.hp} хп")
            ui.pause(f"урон: {enemy.dmg}")
            continue
        elif choice in ["2", "инвентарь", "инвент", "инв"]:
            time, result = inventory_main(ui, player, in_combat=True)
            if result:
                return False
            else:
                continue
        elif choice in ["", "3", "атаковать", "атака"]:
            result = player.attack(enemy, ui)
            if result:
                return "won"
            else:
                return False
        elif choice in ["5", "0", "сбежать", "убежать", "бежать"]:
            if escape():
                ui.display("\nты успешно сбежал в ужасе")
                return "escaped"
            ui.display("ты не смог сбежать в ужасе")
            return False
        elif choice in ["6", "парировать", "пари"]:
            if player.get_parry(ui, enemy):
                enemy.is_skip_turn = True
        else:
            ui.pause("неизвестная команда")
