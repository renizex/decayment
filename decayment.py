import random
import copy

classes = {
    "арбитр": {
        "weapon": {"name": "арматура", "descr": "хорошо ломать ноги другим, когда не могут тебе.", "dmg": "5"},
        "armor": {"name": "классическое пальто", "descr": "sanguis absentia.", "resist": "10"},
        "attributes": {"+30 к хп, +30% к ближнему урону, иммунитет к переломам ноги, плохая стрельба."}
    },
    "дрифтер": {
        "weapon": {"name": "скрытый клинок", "descr": "уж точно не отсылка на ассасина.", "dmg": "10"},
        "armor": {"name": "теневой плащ", "descr": "0% защиты, 100% скрытности и скорости.", "resist": "0"},
        "attributes": {"+30% к ближнему урону, иммунитет к переломам ноги, ужасная, но возможная стрельба, -10 к хп."}
    },
    "иммолятор": {
        "weapon": {"name": "топор", "descr": "хорошо рубит дрова. впрочем, и врагов тоже.", "dmg": "10"},
        "armor": {"name": "утепленная накидка", "descr": "слабо защищает, но не сковывает движения.", "resist": "5"},
        "attributes": {"+25% к ближнему урону, иммунитет к горению, неплохая стрельба."}
    },
    "берсеркер": {
        "weapon": {"name": "копье", "descr": "ничего необычного. позволяет держать дистанцию для контроля врагов.", "dmg": "5"},
        "armor": {"name": "куртка рейдера", "descr": "забытый трофей из жестокого прошлого.", "resist": "5"},
        "attributes": {"+40% к ближнему урону, +15% защиты, иммунитет к переломам ноги, нельзя оглушить, не может стрелять."}
    },
    "артиллерист": {
        "weapon": {"name": "сковородка", "descr": "я жарил на ней яичницу, друзья.", "dmg": "0"},
        "armor": {"name": "куртка с капюшоном", "descr": "кому нужна защита, когда есть сковородка?(и пистолет).", "resist": "0"},
        "attributes": {"отличная стрельба и перезарядка, -15% к ближнему урону, -15% к защите."}
    }
}

weapons = {
    "нож": {"descr": "самый обычный нож", "dmg": 0},
    "сковородка": {"descr": "я жарил на ней яичницу, друзья.", "dmg": 0},
    "арматура": {"descr": "хорошо ломать ноги другим, когда не могут тебе.", "dmg": 5},
    "скрытый клинок": {"descr": "уж точно не отсылка на ассасина.", "dmg": 10},
    "топор": {"descr": "хорошо рубит дрова. впрочем, и врагов тоже.", "dmg": 10},
    "копье": {"descr": "ничего необычного. позволяет держать дистанцию для контроля врагов.", "dmg": 5},
    "бейсбольная бита": {"descr": "хороша для дробления черепов.", "dmg": 15},
    "кувалда": {"descr": "тяжелая и смертоносная", "dmg": 20},
    "военный топор": {"descr": "хорош для каши из топора. или мяса.", "dmg": 25},
    "тактическое копье": {"descr": "улучшенная версия копья.", "dmg": 30},
    "дециматор": {"descr": "что получится, если обьединить дробовик и кувалду? (взрывной урон)", "dmg": 40},
    "коса жнеца": {"descr": "«рви и кромсай, пока не иссякнут.»", "dmg": 50}
}

edens = {
    1: (30, 50),
    2: (50, 100),
    3: (100, 200)
}

drop = {
        1: {"самодельный бинт": 2, "самодельный жгут": 2, "легкая аптечка": 2, "ничего": 1},
        2: {"самодельный бинт": 2, "самодельный жгут": 2, "легкая аптечка": 3, "бейсбольная бита": 2, "ничего": 1},
        3: {"легкая аптечка": 2, "бинт": 1, "жгут": 1, "меч": 1, "ничего": 1},
        4: {"качественная аптечка": 1, "легкая аптечка": 2,  "бинт": 2, "жгут": 2, "флеш граната": 1, "военный топор": 1},
        5: {"качественная аптечка": 1, "чертеж автомата": 1, "чертеж косы жнеца": 1, "импакт граната": 1, "граната": 1, "тактическое копье": 1},
        6: {"качественная аптечка": 1, "чертеж автомата": 1, "чертеж косы жнеца": 1, "динамит": 1, "фиолетовый шприц": 1, "синий шприц": 2,}
}


def heal(ui, player, name, quality):
    amount = 15 if quality == 1 else 40
    old_hp = player.hp
    player.hp += amount
    if player.hp > 100:
        player.hp = 100
    actual_heal = player.hp - old_hp
    ui.display(f"\nты использовал {name} и подлечился на {actual_heal} хп")
    ui.display(f"твое здоровье равняется {player.hp} хп")
    if actual_heal < amount and player.hp == 100:
        ui.display("(эффект ограничен максимальным запасом здоровья)")


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
}

class Enemy:
    def __init__(self, name, hp, dmg, quality):
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.quality = quality

enemies = {
    "скавенджеры": [
        Enemy("скавенджер с ножом", 60, 15, 1),
        Enemy("скавенджер со сковородкой", 60, 15, 1),
        Enemy("скавенджер с арматурой", 80, 15, 2),
        Enemy("скавенджер с копьем", 70, 15, 2),
        Enemy("скавенджер с кувалдой", 150, 10, 5),
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
    def __init__(self, description, effect, weight, quality = 0):
        self.description = description
        self.effect = effect
        self.weight = weight
        self.quality = quality

    def apply(self, ui, player):
        self.effect(ui, player, self.quality)

def get_random_effect(category, place):
    events_list = category_events[category][place]
    weights_list = [evnt.weight for evnt in events_list]
    chosen_effect = random.choices(events_list, weights = weights_list, k = 1)[0]
    return chosen_effect

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

def get_injured(ui, player, quality):
    variants = ["упал", "порезался", "ударился"]
    result = random.choice(variants)
    damage = quality * 10
    player.hp -= quality * 10
    ui.display(f"\nты {result} и получил {damage} урона")
    ui.pause(f"твое хп равно {player.hp}")

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
        battle(ui, player, copy.copy(chosen_enemy))

def battle(ui, player, enemy):
    ui.display(f"\nна тебя напал {enemy.name}")
    while True:
        while True:
            ui.display("\nтвой ход")
            ui.display("ты можешь посмотреть статистику врага, зайти в инвентарь, атаковать и попробовать сбежать")
            ui.display("напиши статистика, инвентарь, атака и бежать соответственно")
            choice = ui.get_input("> ").lower().strip()
            if choice in ["1", "статистика", "стат"]:
                ui.display(f"\nздоровье: {enemy.hp}")
                ui.pause(f"урон: {enemy.dmg}")
                continue
            elif choice in ["2", "инвентарь", "инвент", "инв"]:
                time, result = inventory_main(ui, player, in_combat = True)
                if result:
                    break
                else:
                    continue
            elif choice in ["", "3", "атаковать", "атака"]:
                enemy_death = player_turn(ui, player, enemy)
                if enemy_death:
                    return
                else:
                    break
            elif choice in ["4", "сбежать", "убежать", "бежать"]:
                result = escape(ui)
                if result:
                    return
                break
            else:
                ui.pause("неизвестная команда")
        player_death = enemy_turn(ui, player, enemy)
        if player_death:
            ui.display("хахаха лох")
            return
        else:
            continue

def player_turn(ui, player, enemy):
    # while True:
        # ui.display("тебе доступно на выбор (пока что) только ударить")
        # choice = ui.get_input("> ").lower().strip()
        # if choice in ["", "1", "ударить"]:
        is_crit = crit_chance()
        if is_crit:
            enemy.hp -= 2 * player.dmg
            ui.display(f"ты кританул и нанес {2 * player.dmg} урона")
        else:
            enemy.hp -= player.dmg
            ui.display(f"ты нанес {player.dmg} урона")
        if enemy.hp <= 0:
            enemy.hp = 0
            ui.display("\nты победил")
            return True
        ui.display(f"\nу {enemy.name} осталось {enemy.hp} здоровья")
        return False
        # else:
            # ui.pause("неизвестная команда")

def enemy_turn(ui, player, enemy):
    is_crit = crit_chance(is_player = False)
    if is_crit:
        player.hp -= 2 * enemy.dmg
        ui.display(f"по тебе кританули и нанесли {2 * enemy.dmg} урона")
    else:
        player.hp -= enemy.dmg
        ui.display(f"тебе нанесли {enemy.dmg} урона")
    if player.hp <= 0:
        player.hp = 0
        ui.display("\nты проиграл")
        return True
    ui.display(f"\nу тебя осталось {player.hp} хп")
    return False

def crit_chance(is_player = True):
    if is_player:
        result = 0.2
    else:
        result = 0.1
    if random.random() < result:
        return True
    else:
        return False

def escape(ui):
    if random.random() < 0.5:
        ui.display("ты успешно сбежал в ужасе")
        return True
    else:
        ui.display("ты не смог сбежать в ужасе")
        return False

def not_ready(ui, *_):
    ui.display("\nувы, данная функция пока что не готова")
    ui.pause()

def nothing(ui, *_):
    ui.display("\nувы, ты ничего не нашел")
    ui.pause()

category_events = {
    "bad_places": {
        "мусор": [
            Event("нашел очень мало припасов", get_random_loot, 5, 2),
            Event("нашел мало эденов", get_random_eden, 3, 1),
            Event("небольшое нападение", not_ready, 1, 1)
        ],
        "коробки": [
            Event("нашел каплю припасов", get_random_loot, 4, 1),
            Event("нашел мало эденов", get_random_eden, 3, 1),
            Event("ранение", get_injured, 3, 1)
        ]
    },
    "normal_places": {
        "башня": [
            Event("нашел немного припасов", get_random_loot, 3, 4),
            Event("нашел мало припасов", get_random_loot, 2, 3),
            Event("нашел немного эденов", get_random_eden, 1, 2),
            Event("ранение", get_injured, 1, 3),
            Event("встреча с патрулем", not_ready, 1)
        ],
        "пещера": [
            Event("нашел немного эденов", get_random_eden, 2, 2),
            Event("нашел мало припасов", get_random_loot, 3, 3),
            Event("нашел очень мало припасов", get_random_loot, 1, 2),
            Event("нападение", not_ready, 1)
        ],
        "холм": [
            Event("нашел мало припасов", get_random_loot, 3, 3),
            Event("нашел каплю припасов", get_random_loot, 2, 1),
            Event("нашел немного эденов", get_random_eden, 2, 2),
            Event("ранение", get_injured, 2, 3)
        ]
    },
    "nice_places": {
        "бункер": [
            Event("нашел неплохо припасов", get_random_loot, 3, 6),
            Event("нашел много эденов", get_random_eden, 3, 3),
            Event("нашел немного припасов", get_random_loot, 3, 3),
            Event("встреча с рейдерами", not_ready, 1)
        ],
        "аванпост": [
            Event("нашел средне припасов", get_random_loot, 3, 5),
            Event("нашел немного припасов", get_random_loot, 3, 4),
            Event("нашел средне эденов", get_random_eden, 3, 2),
            Event("встреча со скиннером", not_ready, 1)

        ],
        "место крушения": [
            Event("нашел средне припасов", get_random_loot, 3, 5),
            Event("нашел средне эденов", get_random_eden, 2, 2),
            Event("ранение", get_injured, 2, 5),
        ]
    },
    "good_places": {
        "лаборатория": [
            Event("nothing(yet)", not_ready, 1),
        ],
        "замок рейдеров": [
            Event("nothing(yet)", not_ready, 1),
        ],
        "база скавов": [
            Event("nothing(yet)", not_ready, 1)
        ]
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
        if item in self.weapons:
            current_equipped_weapon = set(self.equipment.keys()) & set(weapons.keys())
            if current_equipped_weapon:
                old_weapon = list(current_equipped_weapon)[0]
                player.dmg -= weapons[old_weapon]["dmg"]
                self.weapons[old_weapon] = self.equipment.pop(old_weapon)

                self.equipment[item] = self.weapons.pop(item)
                player.dmg += weapons[item]["dmg"]
                return "changed", old_weapon

            self.equipment[item] = self.weapons.pop(item)
            player.dmg += weapons[item]["dmg"]
            return "equipped", None

        elif item in self.inventory:
            self.equipment[item] = self.inventory.pop(item)
            return "equipped", None

        return "not_found", None

    def unequip(self, player, item):
        if item in self.equipment:
            if item in weapons:
                player.dmg -= weapons[item]["dmg"]
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
        self.dmg = 20
        self.resist = 100
        self.balance = 500

        self.inventory_manager = Inventory()

    def get_stats(self):
        return self.hp, self.dmg, self.resist

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
        ui.display(f"каждый товар стоит 100 эденов. для списка товаров или руководства")
        ui.display(f"когда будешь готов, напиши название класса или предмета, который хочешь купить, чтобы узнать подробнее и выход чтобы выйти")
        command = ui.get_input("> ").lower().strip()
        found = False
        for class_name in classes:
            weapon_name = classes[class_name]['weapon']['name']
            armor_name = classes[class_name]['armor']['name']
            if command == weapon_name:
                found = True
                purchase(player, ui, weapon_name)
                break
            elif command == armor_name:
                found = True
                purchase(player, ui, armor_name)
                break
        if found:
            continue
        if command in classes:
            ui.display(f"\n{classes[command]['weapon']['name']} - {classes[command]['weapon']['descr']}")
            ui.display(f"{classes[command]['armor']['name']} - {classes[command]['armor']['descr']}")
            ui.display(f"выбирай, что ты будешь делать. пиши купить оружие/броню или выход")
            result = ui.get_input("> ").lower().strip()
            if result in ["купить оружие", f"{classes[command]['weapon']['name']}"]:
                purchase(player, ui, classes[command]['weapon']['name'])
            elif result in ["купить броню", f"{classes[command]['armor']['name']}"]:
                purchase(player, ui, classes[command]['armor']['name'])
            elif result in ["", "выход", "выйти"]:
                pass
            else:
                ui.pause("\nтакой команды не существует")
            continue
        elif command in ["", "выход", "выйти"]:
            return
        else:
            ui.pause("\nтакой команды не существует")

def loot(player, ui, time):
    while time > 0:
        display_time = time_left(time, 0)
        ui.display(f"\nты вылез из своей базы на вылазку. у тебя осталось времени: {display_time}")
        ui.display("ты можешь выбрать желаемый временной обьем вылазки.")
        ui.display("напиши числовое значение того, сколько хочешь выделить, либо Enter чтобы выйти")
        size = ui.get_input("> ").lower().strip()
        if size.isdigit():
            size = int(size)
            while True:
                if size not in range(30, 121):
                    ui.display("\nдиапазон должен быть от 30 до 120")
                    ui.display("введи новое значение")
                    value = (ui.get_input("> "))
                    if value.isdigit():
                        size = int(value)
                elif time - size < 0:
                    ui.display(f"\nтебе не хватает {-(time - size)} секунд. у тебя сейчас {time} секунд")
                    ui.display("введи новое значение")
                    value = (ui.get_input("> "))
                    if value.isdigit():
                        size = int(value)
                else:
                    ui.display(f"\nты выбрал вылазку на {size} секунд")
                    time -= size
                    proceed_loot(player, ui, size)
                    break
        elif size in ["", "выход", "выйти", "назад"]:
            return time
        else:
            ui.pause("\nнеизвестная команда")
    else:
        ui.pause("\nу тебя недостаточно времени")
        return time

def proceed_loot(player, ui, time):
    time = int(time)
    category = None
    names = None
    time_categories = {
        (30, 50): ("bad_places", 2),
        (50, 80): ("normal_places", 3),
        (80, 100): ("nice_places", 3),
        (100, 121): ("good_places", 3)
    }
    for (low, high), (category, count) in time_categories.items():
        if low <= time < high:
            names = list(places[category].keys())
            if count == 2:
                ui.display(f"тебе на выбор доступны две локации: {names[0]} и {names[1]}")
            else:
                ui.display(f"тебе на выбор доступно три локации: {names[0]}, {names[1]} и {names[2]}")
            break
    ui.display("выбери локацию")
    name = ui.get_input().lower().strip()
    if names:
        while name not in names:
            ui.display("\nтакой локации на выбор у тебя нет")
            name = ui.get_input().lower().strip()
    event = get_random_effect(category, name)
    event.apply(ui, player)

def inventory_main(ui, player, time = None, in_combat = False):
    while time is None or time > 0:
        items_list = ", ".join(player.inventory_manager.inventory.keys())
        weapons_list = ", ".join(player.inventory_manager.weapons.keys())
        equipment_list = ", ".join(player.inventory_manager.equipment.keys())

        if time is not None:
            remaining_time = time_left(time, 0)
            ui.display(f"\nу тебя осталось времени: {remaining_time}")
        ui.display(f"\nвот твои расходники: {items_list if items_list else 'пусто'}")
        ui.display(f"вот твой арсенал: {weapons_list if weapons_list else 'пусто'}")
        ui.display(f"вот то, что у тебя экипировано: {equipment_list if equipment_list else 'пусто'}")
        ui.display("\nнапиши название какого либо предмета для взаимодействия с ним, снять чтобы снять убрать или нажми Enter чтобы продолжить")
        command = ui.get_input("> ").lower().strip()
        if command in ["выход", "выйти", "назад", ""]:
            if in_combat:
                return time, False
            return time
        elif command in items:
            if command in player.inventory_manager.inventory.keys():
                item = items[command]
                item.apply(ui, player)
                if time is not None:
                    time -= 5
                if in_combat:
                    return time, True
            else:
                ui.pause("\nу тебя нет такого предмета")
        elif command in weapons:
            result, old_weapon = player.inventory_manager.equip(player, command)
            if result == "equipped":
                ui.display(f"\nты экипировал {command}")
                if time is not None:
                    time -= 5
                if in_combat:
                    return time, True
            elif result == "changed":
                ui.display(f"\nты поменял {old_weapon} на {command}")
                if time is not None:
                    time -= 5
                if in_combat:
                    return time, True
            else:
                ui.pause("\nтакого оружия у тебя нет")
        elif command in ["снять", "убрать"]:
            cross = set(weapons) & set(player.inventory_manager.equipment.keys())
            if cross:
                weapon = list(cross)[0]
                result = player.inventory_manager.unequip(player, weapon)
                if result == "unequipped":
                    ui.display(f"\nты успешно снял {weapon}")
                    if time is not None:
                        time -= 5
                    if in_combat:
                        return time, True
                else:
                    ui.pause("\nне удалось снять предмет")
            else:
                ui.pause("\nу тебя не экипировано оружие")
        else:
            ui.pause("\nтакой команды не существует")
    else:
        ui.pause("\nу тебя недостаточно времени")
        return time, True

def purchase(player, ui, item):
    if player.balance >= 100:
        ui.pause(f"\nты купил {item}")
        player.balance -= 100
        player.inventory_manager.add_item(item)
    else:
        ui.pause(f"\nу тебя недостаточно рублей")

def time_left(time, lost_time):
    time -= lost_time
    minutes = time // 60
    seconds = time % 60
    result = f"{minutes}:{seconds:02d}"
    return result

def menu(player, ui):
    time = random.randint(90, 150)
    lost_time = 0
    while time > 0:
        display_time = time_left(time, lost_time)
        ui.display(f"\nу тебя осталось времени: {display_time}")
        ui.display("тебе доступно пять опций: просмотр статистики, взаимодействие с инвентарем, поход в магазин, поход на вылазку, выход")
        ui.display("для выбора пиши статистика, инвентарь, магазин, вылазка и выход соответственно")
        choice = ui.get_input("> ").lower().strip()
        if choice in ["1", "статистика", "стат"]:
            hp, dmg, res = player.get_stats()
            ui.display(f"\nздоровье: {hp}")
            ui.display(f"урон: {dmg}")
            ui.display(f"защита: {res}")
            ui.pause()
        elif choice in ["2", "магазин"]:
            shop(player, ui)
        elif choice in ["3", "инвентарь", "инвент", "инв"]:
            inventory_main(ui, player)
        elif choice in ["4", "вылазка"]:
            time = loot(player, ui, time)
        elif choice in ["5","выход", "выйти"]:
            break
        else:
            ui.pause("\nтакой команды не существует")

def main():
    ui = UI()
    player_name = name_create(ui)
    player_perk = perk_choose(ui)

    player = Player(player_name, player_perk)

    menu(player, ui)

# начало кода
print("version 0.00")
print("из новостей: я добавляю нумеровочный ввод для практически всех функций, так что игрок сможет просто вводить цифру выбора по номеру от 1 и так далее, дабы упростить ввод")

main()
