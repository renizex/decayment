class UI:
    @staticmethod
    def display(text):
        print(text)

    @staticmethod
    def get_input(prompt="> "):
        return input(prompt)

    def pause(self, message=None):
        if message:
            self.display(message)
        self.display("нажми Enter чтобы продолжить")
        self.get_input()

def statistic(player, ui):
    current_dmg = player.dmg // 2 if player.is_broken_arm else player.dmg
    ui.display(f"\nтвой перк: {player.perk}")
    ui.display(f"здоровье: {player.hp}")
    ui.display(f"урон: {current_dmg}")
    ui.display(f"защита: {round((1 - player.resist) * 100)}%")
    if player.is_broken_leg:
        ui.display("\nу тебя сломана нога")
        ui.display("ты будешь тратить в два раза больше времени на действие")
        ui.display("это пройдет с началом следующей волны, либо ты можешь излечить ее сам с помощью шины")
    if player.is_broken_arm:
        ui.display("\nу тебя сломана рука")
        ui.display("ты будешь наносить в два раза меньше урона по врагам")
        ui.display("(здесь показан текущий урон)")
        ui.display("это пройдет с началом следующей волны, либо ты можешь излечить ее сам с помощью шины")
    ui.pause()

def menu(time, player, ui, time_left, inventory_main, shop, loot):
    while time > 0:
        display_time = time_left(time)
        ui.display(f"\nу тебя осталось времени: {display_time}")
        ui.display(
            "тебе доступно пять опций: просмотр статистики, взаимодействие с инвентарем, поход в магазин, поход на вылазку, выход")
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
