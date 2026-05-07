from data import classes, edens, drop, locations, enemies, items
from entities import Player, Enemy
from ui import UI

def game_over(ui):
    ui.display("ты проиграл, увы")

def not_ready(ui, *_):
    ui.display("\nувы, данная функция пока что не готова")
    ui.pause()

def nothing(ui, *_):
    ui.display("\nувы, ты ничего не нашел")
    ui.pause()

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

def heal_limbs(ui, player, name, quality):
    if not game_flags["broken_leg"] and not game_flags["broken_arm"]:
        ui.display(f"ты поигрался с {name}ом, как ребенок. но из за того, что кости не сломаны, ты ничего не вылечил")
        return False
    ui.display(f"ты использовал {name}")
    if quality == 1:
        ui.display("и вылечил все переломы")
        player.dmg = player.base_dmg
        game_flags["broken_leg"] = False
        game_flags["broken_arm"] = False
    return True

def heal_bleeding(ui, _, name, quality):
    if not game_flags["bleeding"]:
        ui.display(f"ты поигрался с {name}ом и положил его на место")
        return False
    ui.display(f"ты использовал {name}")
    if quality == 1:
        ui.display("и остановил кровотечение")
        game_flags["bleeding"] = False
    return True

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

def location_choice(ui, player, time, category, location):
    value = locations_events[category][location]["cost"]
    time = spend_time(time, value)
    event = get_random_effect(category, location)
    if event:
        event.apply(ui, player)
    return time

def inventory_main(ui, player, time=None, in_combat=False):
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
                    spend_time(time, 5)
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
                    spend_time(time, 5)
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
                    spend_time(time, 5)
                    if in_combat:
                        return time, True
            else:
                ui.pause("у тебя не было экипировано оружие")
        else:
            ui.pause("такой команды не существует")
    else:
        ui.pause("у тебя недостаточно времени")
        return time, True

def time_left(time):
    minutes = round(time // 60)
    seconds = round(time % 60)
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
    time = 999
    # time = random.randint(90, 150)
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
