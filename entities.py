from items import Inventory
import random
from actions import check_event, miss_chance, crit_chance

class Entity:
    def __init__(self, name, hp, dmg, resist):
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.resist = resist
        self.weapon = None
        self.is_broken_leg = False
        self.is_broken_arm = False
        self.is_bleeding = False
        self.is_skip_turn = False
        self.is_player = False

    def attack(self, target, ui):
        if self.is_bleeding:
            ui.display(f"{self.name} истекает кровью и теряет 5 хп")
            self.hp -= 5
            if self.hp <= 0:
                self.hp = 0
                ui.display(f"{self.name} сдох от кровотечения")
                return True
        if self.is_skip_turn:
            self.is_skip_turn = False
            return False
        if miss_chance(self.is_player):
            ui.display(f"{self.name} попытался нанести удар но промахнулся")
            return False
        is_crit = crit_chance(self.is_player)
        multiplier = 1.5 if is_crit else 1.0
        final_damage = max(1, round(self.dmg * multiplier * target.resist))
        category = self.weapon.category if self.weapon else "blunt"
        target.get_injured(ui, final_damage, category)
        target.hp -= final_damage
        msg = f"{self.name} кританул и нанес {final_damage} урона" if is_crit else f"{self.name} нанес {final_damage} урона"
        ui.display(msg)
        if target.hp <= 0:
            target.hp = 0
            ui.display(f"\n{self.name} победил")
            return True
        ui.display(f"\n{target.name}: {target.hp} хп")
        return False

    def get_injured(self, ui, dmg, damage_type):
        if damage_type == "blunt" and dmg > 30:
            chance = min(dmg / 400, 0.15)
            if not check_event(chance):
                return
            result = random.choices(["leg", "arm"], weights=[35, 65], k=1)[0]
            if result == "leg" and not self.is_broken_leg:
                self.broken_leg(ui)
            elif result == "arm" and not self.is_broken_arm:
                self.broken_arm(ui)
        elif damage_type == "bladed" and dmg > 20:
            chance = min(dmg / 300, 0.20)
            if not check_event(chance):
                return
            if not self.is_bleeding:
                self.bleeding(ui)

    def broken_leg(self, ui):
        ui.display(f"у {self.name} сломана нога, он ходит через раз")
        self.is_broken_leg = True

    def broken_arm(self, ui):
        ui.display(f"у {self.name} сломана рука, он наносит в два раза меньше урона")
        self.is_broken_arm = True
        self.dmg //= 2

    def bleeding(self, ui):
        ui.display(f"у {self.name} открылось кровотечение. он будет терять 5 хп каждый ход")
        self.is_bleeding = True

class Player(Entity):
    def __init__(self, name, perk, stats):
        super().__init__(name=name, hp=stats["hp"], dmg=25 * stats["dmg"], resist=stats["resist"])

        self.perk = perk
        self.balance = 500
        self.parry_rate = 0.1
        self.inventory_manager = Inventory()
        self.base_hp = stats["hp"]
        self.base_dmg = round(stats["dmg"])

    def broken_leg(self, ui):
        ui.display(f"у {self.name} сломана нога, теперь твои действия будут тратить в два раза больше времени")
        self.is_broken_leg = True

    def broken_arm(self, ui):
        ui.display(f"у {self.name} сломана рука, теперь ты наносишь в два раза меньше урона")
        self.is_broken_arm = True
        self.dmg //= 2

    def bleeding(self, ui):
        ui.display(f"у {self.name} открылось кровотечение. ты будешь терять 5 хп каждый ход, пока не вылечишься")
        self.is_bleeding = True

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
