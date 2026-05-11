import random
from data import classes
from entities import Player
from ui import UI, menu
from utils import time_left
from actions import name_create, perk_choose
from items import shop, inventory_main
from event import loot

def main():
    ui = UI()
    time = random.randint(90, 150)
    name = name_create(ui)
    perk = perk_choose(ui)
    attr = classes[perk]["attributes"]
    player = Player(name, perk, attr)
    menu(time, player, ui, time_left, inventory_main, shop, loot)

# начало кода
print("я добавил взаимодействие через цифры и сокращения. поиграйся если интересно и лень писать полные названия для взаимодействия.")
print("version 0.00")

main()
