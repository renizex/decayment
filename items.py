class Weapon:
    def __init__(self, name, dmg, category, descr="ты как это увидел вообще", price=0, is_schematic=False, is_buyable=True):
        self.name = name
        self.dmg = dmg
        self.category = category
        self.descr = descr
        self.price = price
        self.is_schematic = is_schematic
        self.is_buyable = is_buyable

class Items:
    def __init__(self, name, effect, quality):
        self.name = name
        self.effect = effect
        self.quality = quality

    def apply(self, ui, player):
        result = self.effect(ui, player, self.name, self.quality)
        if result:
            player.inventory_manager.remove_item(self.name, 1)

class Inventory:
    def __init__(self):
        self.inventory = {}
        self.equipment = {}
        self.weapons = {}

    def add_item(self, item, quantity=1):
        if isinstance(item, Weapon):
            self.weapons[item.name] = item
        else:
            self.inventory[item.name] = self.inventory.get(item.name, 0) + quantity

    def remove_item(self, item_name, quantity = 1):
        if self.inventory.get(item_name, 0) - quantity >= 0:
            self.inventory[item_name] -= quantity
            if self.inventory[item_name] == 0:
                del self.inventory[item_name]
            return "removed"
        return "not_found"

    def equip(self, player, item):
        if item in self.weapons:
            if player.weapon and player.weapon.name == item:
                return "already_equipped", player.weapon.name
            if player.weapon:
                old_weapon_name = player.weapon.name
                player.dmg -= player.weapon.dmg
                player.weapon = self.weapons[item]
                player.dmg += player.weapon.dmg
                return "changed", old_weapon_name
            else:
                player.weapon = self.weapons[item]
                player.dmg += player.weapon.dmg
                return "equipped", player.weapon.name
        return "not_found", item

    @staticmethod
    def unequip(player):
        if player.weapon:
            weapon = player.weapon.name
            player.dmg -= player.weapon.dmg
            player.weapon = None
            return "unequipped", weapon
        return "not_found", None

def shop(player, ui):
    from data import weapons
    while True:
        ui.display(f"\nты находишься в магазине. твой баланс в эденах - {player.balance}")
        ui.display(f"когда будешь готов, напиши название предмета, который хочешь купить, чтобы узнать подробнее и выход чтобы выйти")
        ui.display("(ты можешь вывести весь список оружий на выбор написав список)")
        command = ui.get_input("> ").lower().strip()
        if command in weapons and weapons[command].is_buyable:
            ui.display(f"\n{weapons[command].name} - {weapons[command].descr}")
            ui.display(f"цена: {weapons[command].price} эденов")
            ui.display(f"выбирай, что ты будешь делать. пиши купить или выход")
            result = ui.get_input("> ").lower().strip()
            if result in ["1",  "купить", weapons[command].name.lower()]:
                can_buy = True
                if weapons[command].is_schematic:
                    schematic = "чертеж " + weapons[command].name
                    if schematic not in player.inventory_manager.inventory:
                        ui.pause("\nу тебя нет чертежа этого предмета")
                        can_buy = False
                if can_buy:
                    price = weapons[command].price
                    if player.balance < price:
                        ui.pause("\nу тебя не хватает денег")
                        continue
                    ui.display(f"\nты купил {weapons[command].name}")
                    price = weapons[command].price
                    player.balance -= price
                    player.inventory_manager.add_item(command)
            elif result in ["0", "", "выход", "выйти"]:
                continue
            else:
                ui.pause("\nтакой команды не существует")
            continue
        elif command in ["2", "список"]:
            ui.display("у тебя на выбор есть:\n")
            for weapon in weapons.values():
                if weapon.is_buyable:
                    ui.display(f"{weapon.name} - {weapon.price} эденов")
            ui.pause()
        elif command in ["0", "", "выход", "выйти"]:
            return
        else:
            ui.pause("\nтакой команды не существует")

def inventory_main(ui, player, time=None, in_combat=False):
    from utils import time_left, spend_time
    from data import items, weapons
    while time is None or time > 0:
        items_list = ", ".join(player.inventory_manager.inventory.keys())
        weapons_list = ", ".join(player.inventory_manager.weapons.keys())
        if time is not None:
            remaining_time = time_left(time)
            ui.display(f"\nу тебя осталось времени: {remaining_time}")
        ui.display(f"\nвот твои расходники: {items_list if items_list else 'пусто'}")
        ui.display(f"вот твой арсенал: {weapons_list if weapons_list else 'пусто'}")
        ui.display(f"вот то, что у тебя экипировано: {player.weapon.name if player.weapon else 'безоружен'}")
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
                    spend_time(player, time, 5)
                    if in_combat:
                        return time, True
            else:
                ui.display("у тебя нет такого предмета")
        elif command in weapons:
            result, weapon = player.inventory_manager.equip(player, command)
            if result in ["equipped", "changed"]:
                if result == "equipped":
                    ui.display(f"ты экипировал {command}")
                else:
                    ui.display(f"ты поменял {weapon} на {command}")
                if time is not None:
                    spend_time(player, time, 5)
                    if in_combat:
                        return time, True
            elif result == "already_equipped":
                ui.display("уже экипировано")
            else:
                ui.pause("такого оружия у тебя нет")
        elif command in ["снять", "убрать"]:
            result, weapon = player.inventory_manager.unequip(player)
            if result == "unequipped":
                ui.display(f"ты успешно снял {weapon}")
                if time is not None:
                    spend_time(player, time, 5)
                    if in_combat:
                        return time, True
            else:
                ui.pause("у тебя не было экипировано оружие")
        else:
            ui.pause("такой команды не существует")
    else:
        ui.pause("у тебя недостаточно времени")
        return time, True
