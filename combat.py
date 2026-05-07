import random, copy

def check_event(chance):
    return random.random() < chance

def miss_chance(is_player=True):
    chance = 0.1 if is_player else 0.2
    return check_event(chance)

def crit_chance(is_player=True):
    chance = 0.2 if is_player else 0.1
    return check_event(chance)

def escape():
    chance = 0.5
    return check_event(chance)

def get_parry(ui, player, enemy):
    ui.display(f"ты попробовал спарировать удар {enemy.name}")
    parry_rate = round(player.parry_rate * 100 - enemy.dmg)
    if parry_rate > 0:
        player.parry_rate += 0.005
        ui.display(f"\nты успешно спарировал {enemy.name}")
        ui.display("враг пропустит один ход")
        return True
    else:
        chance = 0.2
        if not check_event(chance):
            player.parry_rate += 0.01
            ui.display(f"\nты не смог спарировать {enemy.name}")
            return False
        player.parry_rate += 0.005
        ui.display(f"\nты успешно спарировал {enemy.name}")
        ui.display("враг пропустит один ход")
        return True

def start_battle(ui, player, quality):
    enemy_list = []
    for faction in enemies:
        for e in enemies[faction]:
            if e.quality == quality:
                enemy_list.append(e)
    if not enemy_list:
        for faction in enemies:
            for e in enemies[faction]:
                if e.quality == 1:
                    enemy_list.append(e)
    if enemy_list:
        chosen_enemy = random.choice(enemy_list)
        chosen_enemy.dmg += chosen_enemy.weapon.dmg
        result = battle(ui, player, copy.copy(chosen_enemy))
        if result == "won":
            get_random_loot(ui, player, quality+1)
        elif result == "escaped":
            return
        elif result == "death":
            game_over(ui)
        else:
            return

def battle(ui, player, enemy):
    ui.display(f"\nна тебя напал {enemy.name}")
    while player.hp > 0 and enemy.hp > 0:
        result = player_turn(ui, player, enemy)
        if result == "escaped":
            return "escaped"
        if result:
            return "won"
        ui.pause()
        if not can_move():
            ui.display("враг пропускает ход из за сломанной ноги")
            continue
        if enemy.hp > 0:
            if enemy_turn(ui, player, enemy):
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
            if game_flags["bleeding"]:
                ui.display("ты истекаешь кровью и твое хп уменьшилось на 5")
                player.hp -= 5
            if miss_chance():
                ui.display("ты попытался нанести удар, но промахнулся")
                return False
            multiplier = 1.5 if crit_chance() else 1.0
            final_damage = max(1, round(player.dmg * multiplier * enemy.resist))
            enemy.hp -= final_damage
            msg = f"ты кританул и нанес {final_damage} урона" if crit_chance() else f"ты нанес {final_damage} урона"
            ui.display(msg)
            if enemy.hp <= 0:
                enemy.hp = 0
                ui.display("\nты победил")
                return True
            ui.display(f"\n{enemy.name}: {enemy.hp} хп")
            return False
        elif choice in ["5", "0", "сбежать", "убежать", "бежать"]:
            if escape():
                ui.display("\nты успешно сбежал в ужасе")
                return "escaped"
            ui.display("ты не смог сбежать в ужасе")
            return False
        elif choice in ["6", "парировать", "пари"]:
            if get_parry(ui, player, enemy):
                enemy_flags["skip_turn"] = True
        else:
            ui.pause("неизвестная команда")

def enemy_turn(ui, player, enemy):
    if enemy_flags["bleeding"]:
        ui.display("враг истекает кровью и теряет 5 хп")
        enemy.hp -= 5
    if enemy_flags["skip_turn"]:
        enemy_flags["skip_turn"] = False
        return False
    if miss_chance(is_player=False):
        ui.display("враг попытался нанести удар но промахнулся")
        return False
    multiplier = 1.5 if crit_chance(is_player=False) else 1.0
    final_damage = max(1, round(enemy.dmg * multiplier * player.resist))
    player.hp -= final_damage
    msg = f"по тебе кританули и нанесли {final_damage} урона" if crit_chance(is_player=False) else f"тебе нанесли {final_damage} урона"
    ui.display(msg)
    if player.hp <= 0:
        player.hp = 0
        ui.display("\nты проиграл")
        return True
    get_injured(player, enemy, ui, final_damage, enemy.weapon.category)
    ui.display(f"\nу тебя осталось {player.hp} хп")
    return False

def get_injured(player, enemy, ui, dmg, damage_type, is_enemy=False):
    if damage_type == "blunt" and dmg > 30:
        chance = min(dmg / 400, 0.15)
        if not check_event(chance):
            return
        result = random.choices(["leg", "arm"], weights=[35, 65], k=1)[0]
        if not is_enemy:
            if result == "leg" and not game_flags["broken_leg"]:
                ui.display("\nу тебя сломана нога. теперь каждое твое действие будет тратить в два раза больше времени")
                game_flags["broken_leg"] = True
            elif result == "arm" and not game_flags["broken_arm"]:
                ui.display("\nу тебя сломана рука. теперь каждый твой удар будет иметь в два раза меньше урона")
                player.dmg //= 2
                game_flags["broken_arm"] = True
        else:
            if result == "leg" and not enemy_flags["broken_leg"]:
                ui.display("\nты сломал врагу ногу. теперь ты сможешь ходить два раза подряд")
                enemy_flags["broken_leg"] = True
            elif result == "arm" and not enemy_flags["broken_arm"]:
                ui.display("\nты сломал врагу руку. теперь его урон будет снижен вдвое")
                enemy.dmg //= 2
                enemy_flags["broken_arm"] = True
    elif damage_type == "bladed" and dmg > 20:
        chance = min(dmg / 300, 0.20)
        if not check_event(chance):
            return
        if not is_enemy:
            if not game_flags["bleeding"]:
                ui.display("у тебя открылось кровотечение. ты будешь терять 5 хп каждый ход, пока не вылечишься")
                game_flags["bleeding"] = True
        else:
            if not enemy_flags["bleeding"]:
                ui.display("у врага открылось кровотечение. он будет терять 5 хп каждый ход")
                enemy_flags["bleeding"] = True

