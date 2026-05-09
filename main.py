import random
from data import classes
from entities import Player
from ui import UI, statistic
from utils import time_left
from actions import name_create, perk_choose
from items import shop, inventory_main
from event import loot

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
    name = name_create(ui)
    perk = perk_choose(ui)
    attr = classes[perk]["attributes"]
    player = Player(name, perk, attr)
    menu(time, player, ui)

# начало кода
print("я добавил взаимодействие через цифры и сокращения. поиграйся если интересно и лень писать полные названия для взаимодействия.")
print("version 0.00")

main()
