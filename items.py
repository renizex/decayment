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