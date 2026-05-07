import random

class Event:
    def __init__(self, effect, weight, quality=0):
        self.effect = effect
        self.weight = weight
        self.quality = quality

    def apply(self, ui, player):
        self.effect(ui, player, self.quality)

def get_random_effect(category, place):
    events_list = locations_events[category][place]["events"]
    if isinstance(events_list, list):
        weights_list = [evnt.weight for evnt in events_list]
        chosen_effect = random.choices(events_list, weights=weights_list, k=1)[0]
        return chosen_effect
    return None

def get_random_loot(ui, player, quality):
    found_items = {}
    repeats = max(1, quality // 2)
    if quality % 2 != 0:
        if random.random() > 0.5:
            repeats += 1
    item_list = list(drop[quality].keys())
    weights_list = list(drop[quality].values())
    for _ in range(repeats):
        while True:
            chosen_item = random.choices(item_list, weights=weights_list, k=1)[0]
            index = item_list.index(chosen_item)
            if chosen_item == "ничего":
                break
            elif chosen_item in player.inventory_manager.weapons:
                item_list.pop(index)
                weights_list.pop(index)
                continue
            else:
                get_item(player, chosen_item, 1)
                if chosen_item in found_items:
                    found_items[chosen_item] += 1
                else:
                    found_items[chosen_item] = 1
                break
    for name, count in found_items.items():
        ui.display(f"получено: {name} (x{count})")
    if not found_items:
        ui.display("тебе ничего не выпало")
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
    player.hp -= quality * 10
    ui.display(f"\nты {result} и получил {damage} урона")
    ui.pause(f"твое хп равно {player.hp}")

def get_item(player, item, quantity):
    if item == "eden":
        player.balance += quantity
    else:
        player.inventory_manager.add_item(item, quantity)

def enter_location(ui, _, quality):
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