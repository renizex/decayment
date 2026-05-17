import random

class Event:
    def __init__(self, effect, weight, quality=0):
        self.effect = effect
        self.weight = weight
        self.quality = quality

    def apply(self, ui, player):
        self.effect(ui, player, self.quality)

def location_choice(ui, player, time, category, location):
    locations = player.locations[category][location]["cost"]
    time = player.spend_time(player, time, locations)
    event = get_random_effect(category, location, player.locations)
    if event:
        event.apply(ui, player)
    return time

def get_random_effect(category, place, locations_events):
    events_list = locations_events[category][place]["events"]
    if isinstance(events_list, list):
        weights_list = [evnt.weight for evnt in events_list]
        chosen_effect = random.choices(events_list, weights=weights_list, k=1)[0]
        return chosen_effect
    return None

def get_random_loot(ui, player, quality):
    drop = player.drop[quality]
    found_items = {}
    repeats = max(1, quality // 2)
    if quality % 2 != 0:
        if random.random() > 0.5:
            repeats += 1
    item_list = list(drop.keys())
    weights_list = list(drop.values())
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
    edens = {
        1: (30, 50),
        2: (50, 100),
        3: (100, 200)
    }
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

def enter_location(ui, player, quality):
    for name in player.locations["good_places"]:
        if player.locations["good_places"][name]["events"][0].quality == quality:
            ui.display(player.locations_text[quality]["desc"])
            ui.display(player.locations_text[quality]["options"])
            while True:
                ui.display("что ты сделаешь?")
                choice = ui.get_input("> ")
                match choice:
                    case "1":
                        ui.display(player.locations_text[quality]["try_enter"])
                        return
                    case "2":
                        ui.display(player.locations_text[quality]["scout_around"])
                        return
                    case "3":
                        ui.display("ты ушел в ужасе")
                        return
                    case _:
                        ui.pause("неизвестная команда")
    else:
        ui.pause("ты как сюда попал вообще")
        return

def loot(player, ui, time, time_left):
    while time > 0:
        locations_events = player.locations
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
                    ui.display("введи новое значение, либо Enter чтобы выйти")
                    value = ui.get_input("> ")
                    if value.isdigit():
                        value = int(value)
                    elif value in ["", "0", "выйти"]:
                        break
                else:
                    time_categories = []
                    high_place = None
                    low_place = None
                    ui.display(f"\nты выбрал вылазку на {value} секунд")
                    for category in locations_events:
                        for place in locations_events[category]:
                            time_categories.append([place, locations_events[category][place]["cost"], category])
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
                            assert isinstance(low_place, list)
                            assert isinstance(high_place, list)
                            ui.display(f"ты можешь пойти в {low_place[0]} ({low_place[1]} сек)")
                            ui.display(f"если добавишь {high_place[1] - value} сек, сможешь пойти в {high_place[0]}")
                            ui.display("хочешь ли ты пойти куда либо из этих локаций?")
                            ui.display("если да, напиши название локации, либо нажми Enter чтобы выйти")
                            result = ui.get_input("> ").lower().strip()
                            if result in ["", "0", "выход", "выйти"]:
                                break
                            elif result == low_place[0]:
                                time = location_choice(ui, player, time, low_place[2], low_place[0])
                            elif result == high_place[0]:
                                time = location_choice(ui, player, time, high_place[2], high_place[0])
                            else:
                                ui.pause(f"неизвестная команда")
                                break
                        else:
                            ui.display("тебе не хватает вообще ни на какую локацию. миниум - 30 сек")
                    else:
                        last_place = sorted_list[-1]
                        ui.display(f"ты выделил слишком много времени для одной локации. максимум - {last_place[0]}, {last_place[1]} сек")
                        ui.display(f"хочешь ли ты отправиться в эту локацию?")
                        ui.display("если да, нажми Enter, либо 0 чтобы выйти")
                        result = ui.get_input("> ").lower().strip()
                        if result in ["0", "выход", "выйти"]:
                            break
                        elif result in ["", "1", "да"]:
                            time = location_choice(ui, player, time, last_place[2], last_place[0])
                        else:
                            ui.display("неизвестная команда")
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
                cost = locations_events[found_category][found_name]["cost"]
                if time >= cost:
                    time = location_choice(ui, player, time, found_category, found_name)
                else:
                    ui.display(f"тебе не хватает времени на эту локацию, нужно {cost} сек")
            else:
                ui.display("такой локации не существует")
        else:
            ui.pause("\nнеизвестная команда")
    else:
        ui.pause("\nу тебя недостаточно времени")
        return time
