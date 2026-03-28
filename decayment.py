import random

# тут я буду пытаться усовершенствовать свою боевую систему, переработать ее через функции, углубить и сделать лучше.
# мой текущий распорядок действий:
# 1 - разобраться в функциях окончательно и понять, как мне использовать их в этом коде
# 2 - переработать старый код, оптимизировать его и пересоздать через функции
# 3 - углубить, добавить новые механики, стартовый экран, геймовер экран, валюту, торговца, вещи
# 4 - избавить код от прошлых ошибок, сделать его читаемым
# 5 - отточить механики, отполировать
# 6 - презентовать семье, друзьям
# 7 - выложить на гитхаб (опционально)

class Location:
    def __init__(self, name, description, risk, time_cost, events, actions = None):
        self.name = name
        self.description = description
        self.risk = risk
        self.time_cost = time_cost
        self.events = events
        self.actions = actions or []

places = {
    "small_places": {
        "good_chance": [
            Location("аванпост", "", "", "", ""),
            Location("гора", "" "", "", "", ""),
            Location("пещера", "", "", "", ""),
                ],
        "medium_chance": [
            Location("холм", "", "", "", ""),
            Location("долина", "", "", "", ""),
                ],
        "bad_chance": [
            Location("коробки", "", "", "", ""),
            Location("мусор", "", "", "", ""),
                ],
    },
        "medium_places": {
            "good_chance": [
            Location("бункер П", "", "", "", ""),
            Location("башня", "", "", "", ""),
            Location("место крушения", "", "", "", ""),
                ],
            "medium_chance": [
            Location("аванпост", "", "", "", ""),
            Location("гора", "", "", "", ""),
            Location("пещера", "", "", "", ""),
                ],
            "bad_chance": [
            Location("холм", "", "", "", ""),
            Location("долина", "", "", "", ""),
                ],
    },
        "large_places": {
            "good_chance": [
            Location("лаборатория", "", "", "", ""),
            Location("замок рейдеров", "", "", "", ""),
                ],
            "medium_chance": [
            Location("бункер П.", "", "", "", ""),
            Location("башня", "", "", "", ""),
            Location("место крушения", "", "", "", ""),
                ],
            "bad_chance": [
            Location("аванпост", "", "", "", ""),
            Location("гора", "", "", "", ""),
            Location("пещера", "", "", "", "")
                ],
    },
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

class Event:
    def __init__(self, effect):

        self.effect = effect


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

    def small_loot(self, time):
        pass

    def medium_loot(self, time):
        pass

    def large_loot(self, time):
        pass

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
        ui.display(f"\nты находишься в магазине. твой баланс в рублях - {player.balance}")
        ui.display(f"каждый товар стоит 100 рублей. для списка товаров или руководства")
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

def purchase(player, ui, thing):
    if player.balance >= 100:
        ui.pause(f"\nты купил {thing}")
        player.balance -= 100
        player.inventory.add_item(thing)
    else:
        ui.pause(f"\nу тебя недостаточно рублей")

def time_left(remaining_time, lost_time):
    remaining_time -= lost_time
    remaining_minutes = remaining_time // 60
    remaining_seconds = remaining_time % 60
    result = f"{remaining_minutes}:{remaining_seconds:02d}"
    return result

def loot(player, ui, time):
    while time > 0:
        remaining_time = time_left(time, 0)
        ui.display(f"\nты вылез из своей базы на вылазку. у тебя осталось времени: {remaining_time}")
        ui.display("нажми Enter чтобы продолжить или выход чтобы выйти")
        command = ui.get_input("> ").lower().strip()
        if command == "":
            ui.display("\nты можешь выбрать желаемый временной обьем вылазки. напиши числовое значение того, сколько времени хочешь выделить")
            size = ui.get_input("> ").lower().strip()
            if size.isdigit():
                size = int(size)
                if size in range(10, 91) and time - size >= 0:
                    ui.display(f"\nи так, ты выбрал вылазку на {size} секунд")
                    ui.display(f"после окончания у тебя останется {time - size} секунд")
                    ui.pause()
                    time -= size
                    if size <= 30:
                        player.small_loot(size)
                    elif size in range(31, 61):
                        player.medium_loot(size)
                    else:
                        player.large_loot(size)

                elif time - size < 0:
                    ui.pause("\nу тебя недостаточно времени")
                else:
                    ui.pause("\nслишком большое/маленькое число. доступный диапазон: от 10 до 90")
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