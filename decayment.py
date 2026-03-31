import random

class Event:
    def __init__(self, description, effect, weight, item, quantity):
        self.description = description
        self.effect = effect
        self.weight = weight
        self.item = item
        self.quantity = quantity

    def apply(self, player):
        self.effect(player)

    @staticmethod
    def get_random_effect(category, place):
        events_list = category_events[category][place]
        weights_list = [evnt.weight for evnt in events_list]
        chosen_event = random.choices(events_list, weights = weights_list, k=1)[0]
        return chosen_event

def get_damage(player, quantity):
    player.hp -= quantity

def get_item(player, item, quantity):
    if item == "eden":
        player.balance += quantity
    else:
        player.inventory.add_item(item, quantity)

category_events = {
    "bad_places": {
        "коробки": [
            Event("нашел очень мало припасов", get_item, 5, ),
            Event("нашел очень мало патронов", get_item, 4),
            Event("нашел очень мало эденов (10-30)", lambda p: get_item(p, "eden", random.randint(10, 30)), 3, ),
            Event("ничего не нашел", "nothing", 2, ),
            Event("небольшое нападение во время лута", "nothing", 1)
            ],
        "мусор": [
            Event("нашел немного припасов", "get_item()",4),
            Event("нашел немного патронов", "get_item()",3),
            Event("нападение во время лута", "get_item()",2),
            Event("ранение (порез)", "get_damage", 1)
            ]
    },
    "normal_places": {
        "башня": [
            Event("nothing(yet)", "nothing(yet)",1),
        ],
        "холм": [
            Event("nothing(yet)", "nothing(yet)", 1),
        ],
        "пещера": [
            Event("nothing(yet)", "nothing(yet)", 1),
        ]
    },
    "nice_places":{
        "бункер П.": [
            Event("nothing(yet)", "nothing(yet)", 1),
        ],
        "аванпост": [
            Event("nothing(yet)", "nothing(yet)", 1),
        ],
        "место крушения": [
            Event("nothing(yet)", "nothing(yet)", 1),
        ]
    },
    "good_places": {
        "лаборатория": [
            Event("nothing(yet)", "nothing(yet)", 1),
        ],
        "замок рейдеров": [
            Event("nothing(yet)", "nothing(yet)", 1),
        ],
        "база скавов": [
            Event("nothing(yet)", "nothing(yet)", 1)
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
        "бункер П.": Location("бункер П.", "5", ""),
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

class UI:
    @staticmethod
    def display(text):
        print(text)

    @staticmethod
    def get_input(prompt="> "):
        return input(prompt)

    def pause(self, message = None):
        if message:
            self.display(message)
        self.display("нажми Enter чтобы продолжить")
        self.get_input()

class Inventory:
    def __init__(self):
        self.inventory = {}
        self.equipment = {}

    def add_item(self, item_name, quantity = 1):
        self.inventory[item_name] = self.inventory.get(item_name, 0) + quantity

    def remove_item(self, item_name, quantity = 1):
        if self.inventory.get(item_name, 0) - quantity >= 0:
            self.inventory[item_name] -= quantity
            if self.inventory[item_name] == 0:
                del self.inventory[item_name]
            return "removed"
        return "not_found"

    def equip(self, item_name):
        if item_name in self.inventory:
            self.equipment[item_name] = self.inventory.pop(item_name)
            return "equipped"
        return "not_found"

    def unequip(self, item_name):
        if item_name in self.equipment:
            self.inventory[item_name] = self.equipment.pop(item_name)
            return "unequipped"
        return "not_found"

class Player:
    def __init__(self, name, perk):
        self.name = name
        self.perk = perk

        self.health = 100
        self.damage = 20
        self.resistance = 100
        self.balance = 500

        self.inventory = Inventory()

    def get_stats(self):
        return self.health, self.damage, self.resistance

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
            b = ui.get_input("> ").lower().strip()
            if b in ["купить оружие", f"{classes[command]['weapon']['name']}"]:
                purchase(player, ui, classes[command]['weapon']['name'])
            elif b in ["купить броню", f"{classes[command]['armor']['name']}"]:
                purchase(player, ui, classes[command]['armor']['name'])
            elif b in ["", "выход", "выйти"]:
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
        ui.display("нажми Enter чтобы продолжить или выход чтобы выйти")
        command = ui.get_input("> ").lower().strip()
        if command == "":
            ui.display("\nты можешь выбрать желаемый временной обьем вылазки. напиши числовое значение того, сколько времени хочешь выделить")
            size = ui.get_input("> ").lower().strip()
            if size.isdigit():
                size = int(size)
                while True:
                    if size not in range(30, 121):
                        ui.display("диапазон должен быть от 30 до 120")
                        ui.display("введи новое значение")
                        value = (ui.get_input("> "))
                        if value.isdigit():
                            size = int(value)
                    elif time - size < 0:
                        ui.display(f"тебе не хватает {-(time - size)} секунд. у тебя {time} секунд")
                        ui.display("введи новое значение")
                        value = (ui.get_input("> "))
                        if value.isdigit():
                            size = int(value)
                    else:
                        ui.display(f"\nты выбрал вылазку на {size} секунд")
                        time -= size
                        proceed_loot(player, ui, size)
                        break
            elif size in ["выход", "выйти", "назад"]:
                break
            else:
                ui.pause("\nдоступен ответ только цифрами")
        elif command in ["выйти", "выход", "назад"]:
            break
        else:
            ui.pause("\nтакой команды не существует. нажми Enter чтобы продолжить")
    else:
        ui.pause("\nу тебя недостаточно времени. нажми Enter чтобы продолжить")
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
                ui.display(f"\nтебе на выбор доступны две локации: {names[0]} и {names[1]}")
            else:
                ui.display(f"\nтебе на выбор доступно три локации: {names[0]}, {names[1]} и {names[2]}")
            break
    ui.display("выбери локацию")
    name = ui.get_input().lower().strip()
    if names:
        while name not in names:
            ui.display("такой локации на выбор у тебя нет")
            name = ui.get_input().lower().strip()
    event = Event.get_random_effect(category, name)
    event.apply(player)

def manage_inventory(player, ui, time):
    while time > 0:
        remaining_time = time_left(time, 0)
        ui.display(f"\nу тебя осталось времени: {remaining_time}")
        ui.display(f"вот твой инвентарь: {', '.join(player.inventory.inventory.keys())}")
        ui.display(f"вот то, что у тебя экипировано: {', '.join(player.inventory.equipment.keys())}")
        ui.display("напиши надеть/снять какой либо предмет или нажми Enter чтобы продолжить")
        command = ui.get_input("> ").lower().strip()
        if command in ["выход", "выйти", "назад", ""]:
            return time
        parts = command.split(maxsplit = 1)
        if len(parts) > 1:
            item = parts[1].strip()
            if parts[0] in ["одеть", "надеть", "экипировать"]:
                if time < 20:
                    ui.pause("\nу тебя недостаточно времени")
                    continue
                result = player.inventory.equip(item)
                if result == "equipped":
                    time -= 20
                    ui.display(f"\nты экипировал {item}")
                elif result == "already_equipped":
                    ui.pause("уже экипировано")
                else:
                    ui.pause("\nпредмет не найден")
            elif parts[0] in ["снять", "убрать"]:
                if time < 20:
                    ui.pause("\nу тебя недостаточно времени")
                    continue
                result = player.inventory.unequip(item)
                if result == "unequipped":
                    time -= 20
                    ui.display(f"\nты снял {item}")
                elif result == "not_unequipped":
                    ui.pause("\nпредмет уже в инвентаре")
                else:
                    ui.pause("\nпредмет не найден")
            else:
                ui.pause("\nнеизвестная команда")
        else:
            ui.pause("\nты не указал предмет")
    else:
        ui.pause("\nу тебя недостаточно времени")
        return time

def purchase(player, ui, item):
    if player.balance >= 100:
        ui.pause(f"\nты купил {item}")
        player.balance -= 100
        player.inventory.add_item(item)
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
        if choice == "статистика":
            hp, dmg, res = player.get_stats()
            ui.display(f"\nздоровье: {hp}")
            ui.display(f"урон: {dmg}")
            ui.display(f"защита: {res}")
            ui.pause()
        elif choice == "магазин":
            shop(player, ui)
        elif choice == "инвентарь":
            time = manage_inventory(player, ui, time)
        elif choice == "вылазка":
            time = loot(player, ui, time)
        elif choice in ["выход", "выйти"]:
            break
        else:
            ui.pause("\nтакой команды не существует")
    else:
        ui.display("\nтебе просто пизда")

def main():
    ui = UI()
    player_name = name_create(ui)
    player_perk = perk_choose(ui)

    player = Player(player_name, player_perk)

    menu(player, ui)

# начало кода
print("version 1.00")

main()
