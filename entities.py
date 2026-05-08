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
        super().__init__(name=name, hp=100, dmg=25 * stats['dmg'], resist=1.0)

        self.perk = perk
        self.weapon = None
        self.balance = 500
        self.parry_rate = 0.1
        self.inventory_manager = Inventory()
        self.base_hp = stats['hp']
        self.base_dmg = self.dmg

class Enemy(Entity):
    def __init__(self, name, hp, dmg, resist, quality, weapon_object):
        super().__init__(name, hp, dmg, resist)
        self.quality = quality
        self.weapon = weapon_object
        self.is_double_move = False
        self.is_skip_turn = False

    @property
    def can_move(self):
        if self.is_broken_leg:
            if not self.is_double_move:
                self.is_double_move = True
                return False
            else:
                return True
        return True

def heal(ui, player, name, quality):
    amount = 15 if quality == 1 else 40
    old_hp = player.hp
    player.hp += amount
    if player.hp > player.base_hp:
        player.hp = player.base_hp
    actual_heal = player.hp - old_hp
    ui.display(f"\nты использовал {name} и подлечился на {actual_heal} хп")
    ui.display(f"твое здоровье равняется {player.hp} хп")
    if actual_heal < amount and player.hp == 100:
        ui.display("(эффект ограничен максимальным запасом здоровья)")

def heal_limbs(ui, player, name, quality):
    if not player.is_broken_leg and not player.is_broken_arm:
        ui.display(f"ты поигрался с {name}ом, как ребенок. но из за того, что кости не сломаны, ты ничего не вылечил")
        return False
    ui.display(f"ты использовал {name}")
    if quality == 1:
        ui.display("и вылечил все переломы")
        player.dmg = player.base_dmg
        player.is_broken_leg = False
        player.is_broken_arm = False
    return True

def heal_bleeding(ui, player, name, quality):
    if not player.is_bleeding:
        ui.display(f"ты поигрался с {name}ом и положил его на место")
        return False
    ui.display(f"ты использовал {name}")
    if quality == 1:
        ui.display("и остановил кровотечение")
        player.is_bleeding = False
    return True
