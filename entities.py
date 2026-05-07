from items import Inventory

class Entity:
    def __init__(self, name, hp, dmg, resist):
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.resist = resist
        self.is_broken_leg = False
        self.is_broken_arm = False
        self.is_bleeding = False
        self.is_skip_turn = False

class Player(Entity):
    def __init__(self, name, perk, stats):
        super().__init__(name=name, hp=100, dmg=stats['dmg'], resist=1.0)

        self.perk = perk
        self.weapon = None
        self.balance = 500
        self.parry_rate = 0.1
        self.inventory_manager = Inventory()
        self.base_hp = stats['hp']
        self.base_dmg = stats['dmg']

class Enemy(Entity):
    def __init__(self, name, hp, dmg, resist, quality, weapon_object):
        super().__init__(name, hp, dmg, resist)
        self.quality = quality
        self.weapon = weapon_object
        self.is_double_move = False

    def can_move(self):
        if self.is_broken_leg:
            if not self.is_double_move:
                self.is_double_move = True
                return False
            else:
                return True
        return True