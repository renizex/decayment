from data import classes, weapons, edens, drop, locations, game_flags
import random
import copy

def game_over(ui):
    ui.display("ты проиграл, увы")

def heal(ui, player, name, quality):
    amount = 15 if quality == 1 else 40
    old_hp = player.hp
    player.hp += amount
    max_hp = classes[player.perk]["attributes"]["hp"]
    if player.hp > max_hp:
        player.hp = max_hp
    actual_heal = player.hp - old_hp
    ui.display(f"\nты использовал {name} и подлечился на {actual_heal} хп")
    ui.display(f"твое здоровье равняется {player.hp} хп")
    if actual_heal < amount and player.hp == 100:
        ui.display("(эффект ограничен максимальным запасом здоровья)")

def heal_limbs(ui, player, quality):
    if quality == 1:
        ui.display("ты вылечил все переломы")
        game_flags["broken_leg"] = False
        game_flags["broken_arm"] = False

def get_leg_broken(player, ui, dmg):
    if player.perk in ["арбитр", "дрифтер"]:
        return
    if dmg > 20:
        final_value = min(dmg / 200, 0.5)
        result = check_event(final_value)
    else:
        result = False
    if result and not game_flags["broken_leg"]:
        ui.display("\nты сломал себе ногу. теперь каждое твое действие будет тратить в два раза больше времени")
        game_flags["broken_leg"] = True

def get_arm_broken(player, ui, dmg):
    if dmg > 20:
        final_value = min(dmg / 200, 0.6)
        result = check_event(final_value)
    else:
        result = False
    if result and not game_flags["broken_arm"]:
        ui.display("\nты сломал себе руку. теперь каждый твой удар будет иметь в два раза меньше урона")
        player.dmg //= 2
        game_flags["broken_arm"] = True

def get_random_effect(category, place):
    events_list = locations_events[category][place]["events"]
    if isinstance(events_list, list):
        weights_list = [evnt.weight for evnt in events_list]
        chosen_effect = random.choices(events_list, weights=weights_list, k=1)[0]
        return chosen_effect
    return None

def get_random_loot(ui, player, quality):
    repeats = max(1, quality // 2)
    if quality % 2 != 0:
        if random.random() > 0.5:
            repeats += 1
    item_list = list(drop[quality].keys())
    weights_list = list(drop[quality].values())
    for _ in range(repeats):
        while True:
            chosen_item = random.choices(item_list, weights = weights_list, k = 1)[0]
            if chosen_item == "ничего":
                ui.display("\nувы, ты ничего не получил")
                break
            elif chosen_item in player.inventory_manager.weapons:
                ui.display(f"\nоп, {chosen_item} у тебя в инвентаре уже есть, рероллим")
            else:
                ui.display(f"\nты получил {chosen_item}")
                get_item(player, chosen_item, 1)
                break
    ui.pause()

def get_random_eden(ui, player, quality):
    eden_list = list(edens[quality])
    get_edens = random.randint(eden_list[0], eden_list[1])
    get_item(player, "eden", get_edens)
    ui.pause(f"\nты получил {get_edens} эденов")

def get_damage(ui, player, quality):
    variants = ["упал", "порезался", "ударился"]
    result = random.choice(variants)
    damage = quality * 10
    player.health -= quality * 10
    ui.display(f"\nты {result} и получил {damage} урона")
    ui.pause(f"твое хп равно {player.health}")

def get_item(player, item, quantity):
    if item == "eden":
        player.balance += quantity
    else:
        player.inventory_manager.add_item(item, quantity)

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
        result = battle(ui, player, copy.copy(chosen_enemy))
        if result == "won":
            get_random_loot(ui, player, quality + 1)
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
        if enemy.hp > 0:
            if enemy_turn(ui, player, enemy):
                return "death"
    return "error"

def player_turn(ui, player, enemy):
    while True:
        ui.display("\nтвой ход")
        ui.display("ты можешь посмотреть статистику врага, зайти в инвентарь, атаковать и попробовать сбежать")
        ui.display("напиши статистика, инвентарь, атака и бежать соответственно (можно цифрами)")
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
            is_miss = miss_chance()
            if is_miss:
                ui.display("ты попытался нанести удар, но промахнулся")
                return False
            is_crit = crit_chance()
            multiplier = 1.5 if is_crit else 1.0
            final_damage = max(1, round(player.dmg * multiplier * enemy.resist))
            enemy.hp -= final_damage
            msg = f"ты кританул и нанес {final_damage} урона" if is_crit else f"ты нанес {final_damage} урона"
            ui.display(msg)
            if enemy.hp <= 0:
                enemy.hp = 0
                ui.display("\nты победил")
                return True
            ui.display(f"\n{enemy.name}: {enemy.hp} хп")
            return False
        elif choice in ["4", "0", "сбежать", "убежать", "бежать"]:
            result = escape()
            if result:
                ui.display("ты успешно сбежал в ужасе")
                return "escaped"
            ui.display("ты не смог сбежать в ужасе")
            return False
        else:
            ui.pause("неизвестная команда")

def enemy_turn(ui, player, enemy):
    is_miss = miss_chance(is_player=False)
    if is_miss:
        ui.display("враг попытался нанести удар но промахнулся")
        return False
    is_crit = crit_chance(is_player=False)
    multiplier = 1.5 if is_crit else 1.0
    final_damage = max(1, round(enemy.dmg * multiplier * player.resist))
    player.hp -= final_damage
    msg = f"по тебе кританули и нанесли {final_damage} урона" if is_crit else f"тебе нанесли {final_damage} урона"
    ui.display(msg)
    if player.hp <= 0:
        player.hp = 0
        ui.display("\nты проиграл")
        return True
    ui.display(f"\nу тебя осталось {player.hp} хп")
    return False

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

def not_ready(ui, *_):
    ui.display("\nувы, данная функция пока что не готова")
    ui.pause()

def nothing(ui, *_):
    ui.display("\nувы, ты ничего не нашел")
    ui.pause()

def enter_location(ui, player, quality):
    if quality not in locations:
        ui.pause("ты как сюда попал вообще")
        return
    text = locations[quality]
    ui.display(text["desc"])
    ui.display(text["options"])
    while True:
        ui.display("что ты сделаешь?")
        choice = ui.get_input("> ")
        match choice:
            case "1":
                ui.display(text["try_enter"])
                return
            case "2":
                ui.display(text["scout_around"])
                return
            case "3":
                ui.display("ты ушел в ужасе")
                return
            case _:
                ui.pause("неизвестная команда")

class Items:
    def __init__(self, name, effect, quality):
        self.name = name
        self.effect = effect
        self.quality = quality

    def apply(self, ui, player):
        self.effect(ui, player, self.name, self.quality)
        player.inventory_manager.remove_item(self.name, 1)

items = {
    "легкая аптечка": Items("легкая аптечка", heal, 1),
    "качественная аптечка": Items("качественная аптечка", heal, 2),
    "самодельный бинт": Items("самодельный бинт", heal_limbs, 1)
}

class Enemy:
    def __init__(self, name, hp, dmg, resist, quality):
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.resist = resist
        self.quality = quality

enemies = {
    "скавенджеры": [
        Enemy("скавенджер с ножом", 60, 15, 1.0, 1),
        Enemy("скавенджер со сковородкой", 60, 15, 1.0, 1),
        Enemy("скавенджер с арматурой", 80, 15, 0.95,2),
        Enemy("скавенджер с копьем", 70, 15, 0.95,2),
        Enemy("скавенджер с кувалдой", 150, 20, 0.9, 5)
    ],
    "рейдеры": [
        Enemy("рейдер щитовик", 80, 20, 0.9, 3),
        Enemy("рейдер с топорищем", 100, 30, 0.85, 5),
        Enemy("рейдер охотник", 120, 35, 1.0, 6)
    ],
    "рейкгоны": [
        Enemy("скиннер", 200, 20, 0.9, 6)
    ]
}

class UI:
    @staticmethod
    def display(text):
        print(text)

    @staticmethod
    def get_input(prompt = "> "):
        return input(prompt)

    def pause(self, message = None):
        if message:
            self.display(message)
        self.display("нажми Enter чтобы продолжить")
        self.get_input()

class Event:
    def __init__(self, effect, weight, quality = 0):
        self.effect = effect
        self.weight = weight
        self.quality = quality

    def apply(self, ui, player):
        self.effect(ui, player, self.quality)

locations_events = {
    "bad_places": {
        "мусор": {
            "cost": 40,
            "events": [Event(get_random_loot, 5, 2), Event(get_random_eden, 3, 1), Event(start_battle, 1, 1)]
        },
        "коробки": {
            "cost": 30,
            "events": [Event(get_random_loot, 4, 1), Event(get_random_eden, 3, 1), Event(get_damage, 3, 1)]
        },
    },
    "normal_places": {
        "башня": {
            "cost": 70,
            "events": [Event(get_random_loot, 3, 4), Event(get_random_loot, 2, 3), Event(get_random_eden, 1, 2), Event(get_damage, 1, 3), Event(start_battle, 2, 2)]
        },
        "пещера": {
            "cost": 60,
            "events": [Event(get_random_eden, 2, 2), Event(get_random_loot, 3, 3), Event(get_random_loot, 1, 2), Event(start_battle, 1, 1)]
        },
        "холм": {
            "cost": 50,
            "events": [Event(get_random_loot, 3, 3), Event(get_random_loot, 2, 1), Event(get_random_eden, 2, 2), Event(get_damage, 2, 3)]
        }
    },
    "nice_places": {
        "бункер": {
            "cost": 100,
            "events": [Event(get_random_loot, 3, 6), Event(get_random_eden, 3, 3), Event(get_random_loot, 3, 3), Event(start_battle, 2, 3)]
        },
        "аванпост": {
            "cost": 90,
            "events": [Event(get_random_loot, 3, 5), Event(get_random_loot, 3, 4), Event(get_random_eden, 3, 2), Event(start_battle, 2, 2)]
        },
        "крушение": {
            "cost": 80,
            "events": [Event(get_random_loot, 3, 5), Event(get_random_eden, 2, 2), Event(get_damage, 2, 4)]
        }
    },
    "good_places": {
        "лаборатория": {
            "cost": 20,
            "events": [Event(enter_location, 1, 30)]
        },
        "замок рейдеров": {
            "cost": 40,
            "events": [Event(enter_location, 1, 20)]
        },
        "база скавов": {
            "cost": 30,
            "events": [Event(enter_location, 1, 10)]
        }
    }
}

class Location:
    def __init__(self, name, risk, actions = None):
        self.name = name
        self.risk = risk
        self.actions = actions

places = {
    "good_places": {
        "лаборатория": Location("лаборатория", "15", ""),
        "замок рейдеров": Location("замок рейдеров", "10", ""),
        "база скавов": Location("база скавов", "8", "")
    },
    "nice_places": {
        "бункер": Location("бункер", "5", ""),
        "аванпост": Location("аванпост", "5", ""),
        "место крушения": Location("место крушения", "5", "")
    },
    "normal_places": {
        "башня": Location("башня", "4", ""),
        "холм": Location("холм", "3", ""),
        "пещера":Location("пещера", "2", "")
    },
    "bad_places": {
        "коробки": Location("коробки", "1", ""),
        "мусор": Location("мусор", "2", "")
    }
}

class Inventory:
    def __init__(self):
        self.inventory = {}
        self.equipment = {}
        self.weapons = {}

    def add_item(self, item, quantity = 1):
        if item in weapons:
            self.weapons[item] = weapons[item].copy()
        else:
            self.inventory[item] = self.inventory.get(item, 0) + quantity

    def remove_item(self, item_name, quantity = 1):
        if self.inventory.get(item_name, 0) - quantity >= 0:
            self.inventory[item_name] -= quantity
            if self.inventory[item_name] == 0:
                del self.inventory[item_name]
            return "removed"
        return "not_found"

    def equip(self, player, item):
        if item in self.equipment:
            return "already_equipped", None

        if item in self.weapons:
            current_equipped_weapon = set(self.equipment.keys()) & set(weapons.keys())
            if current_equipped_weapon:
                old_weapon = list(current_equipped_weapon)[0]
                player.damage -= weapons[old_weapon]["dmg"]
                self.weapons[old_weapon] = self.equipment.pop(old_weapon)

                self.equipment[item] = self.weapons.pop(item)
                player.damage += weapons[item]["dmg"]
                return "changed", old_weapon

            self.equipment[item] = self.weapons.pop(item)
            player.damage += weapons[item]["dmg"]
            return "equipped", None

        elif item in self.inventory:
            self.equipment[item] = self.inventory.pop(item)
            return "equipped", None
        return "not_found", None

    def unequip(self, player, item):
        if item in self.equipment:
            if item in weapons:
                player.damage -= weapons[item]["dmg"]
                self.weapons[item] = self.equipment.pop(item)
            else:
                self.inventory[item] = self.equipment.pop(item)
            return "unequipped"
        return "not_found"

class Player:
    def __init__(self, name, perk):
        self.name = name
        self.perk = perk

        self.hp = 100
        self.dmg = 25
        self.resist = 1.0
        self.balance = 500

        self.inventory_manager = Inventory()

def name_create(ui):
    while True:
        ui.display("\nназови же имя того, кому суждено страдать")
        name = ui.get_input("> ").strip()
        while name == "" or len(name) < 3:
            ui.display("\nтакое имя создать нельзя")
            name = ui.get_input("> ").strip()
        while True:
            ui.display(f"\nотлично, имя твое - {name}. нажми Enter, если хочешь продолжить и нет, если хочешь сменить имя")
            command = ui.get_input("> ").strip().lower()
            if command == "":
                return name
            elif command == "нет":
                break
            else:
                ui.pause("\nтакой команды не существует.")

def perk_choose(ui):
    while True:
        ui.display("\nвыбери свой перк. тебе на выбор доступно: арбитр, дрифтер, иммолятор, берсеркер, артиллерист")
        perk = ui.get_input("> ").lower().strip()
        if perk in ["арбитр", "дрифтер", "иммолятор", "берсеркер", "артиллерист"]:
            while True:
                ui.display(f"\nтвой перк - {perk}. нажми Enter чтобы продолжить или нет, чтобы сменить его")
                command = ui.get_input("> ").lower().strip()
                if command in ["нет", "сменить", "изменить"]:
                    break
                elif command == "":
                    return perk
                else:
                    ui.pause("\nтакой команды не существует")
        else:
            ui.pause("\nтакого перка не существует")

def shop(player, ui):
    while True:
        ui.display(f"\nты находишься в магазине. твой баланс в эденах - {player.balance}")
        ui.display(f"когда будешь готов, напиши название предмета, который хочешь купить, чтобы узнать подробнее и выход чтобы выйти")
        ui.display("(ты можешь вывести весь список оружий на выбор написав список)")
        command = ui.get_input("> ").lower().strip()
        if command in weapons:
            ui.display(f"\n{weapons[command]['name']} - {weapons[command]['descr']}")
            ui.display(f"цена: {weapons[command]['price']} эденов")
            ui.display(f"выбирай, что ты будешь делать. пиши купить или выход")
            result = ui.get_input("> ").lower().strip()
            if result in ["1",  "купить", weapons[command]['name']]:
                can_buy = True
                if weapons[command]["is_schematic"]:
                    schematic = "чертеж " + weapons[command]['name']
                    if schematic not in player.inventory_manager.inventory:
                        ui.pause("\nу тебя нет чертежа этого предмета")
                        can_buy = False
                if can_buy:
                    price = weapons[command]["price"]
                    if player.balance < price:
                        ui.pause("\nу тебя не хватает денег")
                        continue
                    ui.display(f"\nты купил {weapons[command]['name']}")
                    purchase(player, command)
            elif result in ["0", "", "выход", "выйти"]:
                continue
            else:
                ui.pause("\nтакой команды не существует")
            continue
        elif command in ["2", "список"]:
            ui.display("у тебя на выбор есть:\n")
            for i in weapons.values():
                ui.display(f"{i['name']} - {i['price']} эденов")
            ui.pause()
        elif command in ["0", "", "выход", "выйти"]:
            return
        else:
            ui.pause("\nтакой команды не существует")

def purchase(player, item):
    price = weapons[item]["price"]
    player.balance -= price
    player.inventory_manager.add_item(item)

def loot(player, ui, time):
    while time > 0:
        display_time = time_left(time)
        ui.display(f"\nты вылез из своей базы на вылазку. у тебя осталось времени: {display_time}")
        ui.display("ты можешь выбрать желаемый временный обьем, а так же можешь вызвать список для того, чтобы увидеть все доступные локации")
        ui.display("напиши число сколько хочешь выделить, название локации, список, либо Enter чтобы выйти")
        choice = ui.get_input("> ").lower().strip()
        if choice == "":
            return time
        if choice.isdigit():
            value = int(choice)
            while True:
                if time - value < 0:
                    ui.display(f"\nтебе не хватает {-(time - value)} секунд. у тебя сейчас {time} секунд")
                    ui.display("введи новое значение")
                    value = ui.get_input("> ")
                    if value.isdigit():
                        value = int(value)
                else:
                    time_categories = []
                    high_place = None
                    low_place = None
                    ui.display(f"\nты выбрал вылазку на {value} секунд")
                    for category in locations_events:
                        for place in locations_events[category]:
                            time_categories.append([place, locations_events[category][place]["cost"]])
                    sorted_list = sorted(time_categories, key=lambda x: x[1])
                    previous = None
                    for cell in sorted_list:
                        if cell[1] > value:
                            high_place = cell
                            low_place = previous
                            break
                        previous = cell
                    if high_place:
                        if low_place:
                            ui.display(f"ты можешь пойти в {low_place[0]} ({low_place[1]} сек)")
                            ui.display(f"если добавишь {high_place[1] - value} сек, сможешь пойти в {high_place[0]}")
                        else:
                            ui.display("тебе не хватает вообще ни на какую локацию. миниум - 30 сек")
                    else:
                        last_place = sorted_list[-1]
                        ui.display(f"ты выделил слишком много времени для одной локации. максимум - {last_place[0]}, {last_place[1]} сек")
                    break
        elif choice == "список":
            ui.display("список доступных локаций:")
            for category in locations_events:
                for name, data in locations_events[category].items():
                    ui.display(f"{name} - {data['cost']} сек")
        elif not choice.isdigit():
            found_category = None
            found_name = None
            for category in locations_events:
                for name in locations_events[category]:
                    if choice == name:
                        found_category = category
                        found_name = name
                        break
                if found_name:
                    break
            if found_name and found_category:
                value = locations_events[found_category][found_name]["cost"]
                time = spend_time(time, value)
                event = get_random_effect(found_category, found_name)
                event.apply(ui, player)
            else:
                ui.display("такой локации не существует")
        else:
            ui.pause("\nнеизвестная команда")
    else:
        ui.pause("\nу тебя недостаточно времени")
        return time

def inventory_main(ui, player, time = None, in_combat = False):
    while time is None or time > 0:
        items_list = ", ".join(player.inventory_manager.inventory.keys())
        weapons_list = ", ".join(player.inventory_manager.weapons.keys())
        equipment_list = ", ".join(player.inventory_manager.equipment.keys())

        if time is not None:
            remaining_time = time_left(time)
            ui.display(f"\nу тебя осталось времени: {remaining_time}")
        ui.display(f"\nвот твои расходники: {items_list if items_list else 'пусто'}")
        ui.display(f"вот твой арсенал: {weapons_list if weapons_list else 'пусто'}")
        ui.display(f"вот то, что у тебя экипировано: {equipment_list if equipment_list else 'пусто'}")
        ui.display("\nнапиши название какого либо предмета для взаимодействия с ним, снять чтобы снять убрать или нажми Enter чтобы продолжить")
        command = ui.get_input("> ").lower().strip()
        if command in ["0", "выход", "выйти", "назад", ""]:
            if in_combat:
                return time, False
            return time
        elif command in items:
            if command in player.inventory_manager.inventory.keys():
                item = items[command]
                item.apply(ui, player)
                if time is not None:
                    spend_time(time, 5)
                if in_combat:
                    return time, True
            else:
                ui.display("у тебя нет такого предмета")
        elif command in weapons:
            result, old_weapon = player.inventory_manager.equip(player, command)
            if result == "equipped":
                ui.display(f"ты экипировал {command}")
                if time is not None:
                    spend_time(time, 5)
                if in_combat:
                    return time, True
            elif result == "changed":
                ui.display(f"ты поменял {old_weapon} на {command}")
                if time is not None:
                    spend_time(time, 5)
                if in_combat:
                    return time, True
            elif result == "already_equipped":
                ui.display("уже экипировано")
            else:
                ui.pause("такого оружия у тебя нет")
        elif command in ["снять", "убрать"]:
            cross = set(weapons) & set(player.inventory_manager.equipment.keys())
            if cross:
                weapon = list(cross)[0]
                result = player.inventory_manager.unequip(player, weapon)
                if result == "unequipped":
                    ui.display(f"ты успешно снял {weapon}")
                    if time is not None:
                        spend_time(time, 5)
                    if in_combat:
                        return time, True
                else:
                    ui.pause("не удалось снять предмет")
            else:
                ui.pause("у тебя не экипировано оружие")
        else:
            ui.pause("такой команды не существует")
    else:
        ui.pause("у тебя недостаточно времени")
        return time, True

def time_left(time):
    minutes = time // 60
    seconds = time % 60
    result = f"{minutes}:{seconds:02d}"
    return result

def spend_time(time, amount):
    multiplier = 1.0
    if game_flags["broken_leg"]:
        multiplier = 2.0
    time -= amount * multiplier
    return time

def statistic(player, ui):
    current_dmg = player.dmg // 2 if game_flags["broken_arm"] else player.dmg
    ui.display(f"\nтвой перк: {player.perk}")
    ui.display(f"здоровье: {player.hp}")
    ui.display(f"урон: {current_dmg}")
    ui.display(f"защита: {round((1 - player.resist) * 100)}%")
    if game_flags["broken_leg"]:
        ui.display("\nу тебя сломана нога")
        ui.display("ты будешь тратить в два раза больше времени на действие")
        ui.display("это пройдет с началом следующей волны, либо ты можешь излечить ее сам с помощью шины")
    if game_flags["broken_arm"]:
        ui.display("\nу тебя сломана рука")
        ui.display("ты будешь наносить в два раза меньше урона по врагам")
        ui.display("(здесь показан текущий урон)")
        ui.display("это пройдет с началом следующей волны, либо ты можешь излечить ее сам с помощью шины")
    ui.pause()

def menu(time, player, ui):
    while time > 0:
        display_time = time_left(time)
        ui.display(f"\nу тебя осталось времени: {display_time}")
        ui.display("тебе доступно пять опций: просмотр статистики, взаимодействие с инвентарем, поход в магазин, поход на вылазку, выход")
        ui.display("для выбора пиши статистика, инвентарь, магазин, вылазка и выход соответственно")
        choice = ui.get_input("> ").lower().strip()
        if choice in ["1", "статистика", "стат"]:
            statistic(player, ui)
        elif choice in ["2", "инвентарь", "инвент", "инв"]:
            inventory_main(ui, player)
        elif choice in ["3", "магазин", "магаз", "маг"]:
            shop(player, ui)
        elif choice in ["4", "вылазка", "вылаз", "выл"]:
            time = loot(player, ui, time)
        elif choice in ["5", "0", "выход", "выйти"]:
            break
        else:
            ui.pause("\nтакой команды не существует")

def main():
    ui = UI()
    time = random.randint(90, 150)
    player_name = name_create(ui)
    player_perk = perk_choose(ui)
    player = Player(player_name, player_perk)

    attr = classes[player.perk]["attributes"]
    player.hp = attr["hp"]
    player.dmg = round(player.dmg * attr["dmg"])
    player.resist = round(player.resist * attr["resist"])
    menu(time, player, ui)

# начало кода
print("я добавил взаимодействие через цифры и сокращения. поиграйся если интересно и лень писать полные названия для взаимодействия.")
print("version 0.00")

main()
