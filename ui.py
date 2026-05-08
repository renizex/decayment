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
