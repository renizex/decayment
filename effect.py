class Effect:
    def __init__(self, name):
        self.name = name
        self.is_bleeding = False
        self.is_broken_leg = False

    def apply(self, ui, player):
        pass

    def remove(self, ui, player):
        pass
    
class Bleeding(Effect):
    def apply(self, ui, player):
        pass

    def bleeding(self, ui):
        ui.display(f"у {self.name} открылось кровотечение. он будет терять 5 хп каждый ход")
        self.is_bleeding = True

class BrokenLimbs(Effect):
    def apply(self, ui, player):
        pass

    def broken_leg(self, ui):
        ui.display(f"у {self.name} сломана нога, он ходит через раз")
        self.is_broken_leg = True

    def broken_arm(self, ui):
        ui.display(f"у {self.name} сломана рука, он наносит в два раза меньше урона")
        self.is_broken_arm = True
        self.dmg //= 2

    def remove(self, ui, player):
        ui.display()