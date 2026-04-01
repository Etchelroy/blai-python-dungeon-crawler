import random
import os
import sys
import io

if os.name == 'nt':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ── Items ────────────────────────────────────────────────────────────────────
WEAPONS = [
    {"name": "Rusty Sword",   "bonus": 2,  "price": 0},
    {"name": "Iron Sword",    "bonus": 5,  "price": 30},
    {"name": "Steel Blade",   "bonus": 10, "price": 60},
    {"name": "Flaming Sword", "bonus": 18, "price": 100},
]

POTIONS = [
    {"name": "Small Potion",  "heal": 20, "price": 10},
    {"name": "Medium Potion", "heal": 50, "price": 25},
    {"name": "Large Potion",  "heal": 100, "price": 50},
]

# ── Enemies ──────────────────────────────────────────────────────────────────
ENEMY_TYPES = {
    "goblin": {"hp": 15, "attack": 3, "defense": 1, "xp": 10, "gold": 15},
    "skeleton": {"hp": 30, "attack": 6, "defense": 2, "xp": 25, "gold": 40},
    "dragon": {"hp": 100, "attack": 12, "defense": 5, "xp": 100, "gold": 200},
}

# ── Hero Class ───────────────────────────────────────────────────────────────
class Hero:
    def __init__(self):
        self.hp = 100
        self.max_hp = 100
        self.base_attack = 8
        self.base_defense = 3
        self.xp = 0
        self.level = 1
        self.gold = 50
        self.weapons = [WEAPONS[0].copy()]
        self.equipped_weapon = 0
        self.potions = []
        self.x = 1
        self.y = 1

    def get_attack(self):
        return self.base_attack + self.weapons[self.equipped_weapon]["bonus"]

    def get_defense(self):
        return self.base_defense

    def take_damage(self, damage):
        reduction = min(damage, self.get_defense() + random.randint(0, 2))
        actual_damage = max(1, damage - reduction)
        self.hp -= actual_damage
        return actual_damage

    def gain_xp(self, amount):
        self.xp += amount
        self.check_level_up()

    def check_level_up(self):
        xp_needed = 50 * self.level
        if self.xp >= xp_needed:
            self.level += 1
            self.xp -= xp_needed
            self.max_hp += 20
            self.hp = self.max_hp
            self.base_attack += 2
            self.base_defense += 1
            return True
        return False

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def is_alive(self):
        return self.hp > 0

# ── Enemy Class ──────────────────────────────────────────────────────────────
class Enemy:
    def __init__(self, enemy_type):
        self.type = enemy_type
        stats = ENEMY_TYPES[enemy_type].copy()
        self.hp = stats["hp"]
        self.max_hp = stats["hp"]
        self.attack = stats["attack"]
        self.defense = stats["defense"]
        self.xp_reward = stats["xp"]
        self.gold_reward = stats["gold"]

    def take_damage(self, damage):
        reduction = min(damage, self.defense + random.randint(0, 1))
        actual_damage = max(1, damage - reduction)
        self.hp -= actual_damage
        return actual_damage

    def is_alive(self):
        return self.hp > 0

# ── Combat ───────────────────────────────────────────────────────────────────
def combat(hero, enemy):
    clear()
    enemy_name = enemy.type.capitalize()
    
    while hero.is_alive() and enemy.is_alive():
        print("╔════════════════════════════════════════╗")
        print(f"║ COMBAT: {enemy_name:<31} ║")
        print("╚════════════════════════════════════════╝")
        print(f"\nHero HP:   {hero.hp}/{hero.max_hp} | Lv{hero.level} | ATK{hero.get_attack()} | DEF{hero.get_defense()} | XP{hero.xp}")
        print(f"Enemy HP:  {enemy.hp}/{enemy.max_hp}")
        print("\n[1] Attack")
        print("[2] Use Potion")
        print("[3] Flee")
        
        choice = input("\nChoose action: ").strip()
        clear()
        
        if choice == "1":
            damage = hero.get_attack() + random.randint(-2, 3)
            taken = enemy.take_damage(damage)
            print(f"You attacked! {enemy_name} took {taken} damage.")
            
            if enemy.is_alive():
                enemy_damage = enemy.attack + random.randint(-1, 2)
                taken = hero.take_damage(enemy_damage)
                print(f"{enemy_name} attacked! You took {taken} damage.")
            
        elif choice == "2":
            if not hero.potions:
                print("No potions available!")
            else:
                print("Available potions:")
                for i, potion in enumerate(hero.potions):
                    print(f"  [{i+1}] {potion['name']} ({potion['heal']} HP)")
                potion_choice = input("Use potion (number): ").strip()
                try:
                    idx = int(potion_choice) - 1
                    if 0 <= idx < len(hero.potions):
                        potion = hero.potions.pop(idx)
                        hero.heal(potion["heal"])
                        print(f"Used {potion['name']}! Restored {potion['heal']} HP.")
                        enemy_damage = enemy.attack + random.randint(-1, 2)
                        taken = hero.take_damage(enemy_damage)
                        print(f"{enemy_name} attacked! You took {taken} damage.")
                    else:
                        print("Invalid choice!")
                except:
                    print("Invalid choice!")
                    
        elif choice == "3":
            if random.random() < 0.4:
                print("You fled successfully!")
                input("\nPress ENTER to continue...")
                return "fled"
            else:
                print("Failed to flee!")
                enemy_damage = enemy.attack + random.randint(-1, 2)
                taken = hero.take_damage(enemy_damage)
                print(f"{enemy_name} attacked! You took {taken} damage.")
        else:
            print("Invalid choice!")
        
        input("\nPress ENTER to continue...")
    
    clear()
    if hero.is_alive():
        print("╔════════════════════════════════════════╗")
        print("║ VICTORY!                               ║")
        print("╚════════════════════════════════════════╝")
        hero.gold += enemy.gold_reward
        hero.gain_xp(enemy.xp_reward)
        print(f"\nYou defeated {enemy_name}!")
        print(f"+{enemy.xp_reward} XP")
        print(f"+{enemy.gold_reward} Gold")
        input("\nPress ENTER to continue...")
        return "victory"
    else:
        return "defeat"

# ── Shop System ──────────────────────────────────────────────────────────────
def shop(hero):
    while True:
        clear()
        print("╔════════════════════════════════════════╗")
        print("║ SHOP                                   ║")
        print("╚════════════════════════════════════════╝")
        print(f"\nGold: {hero.gold}")
        print(f"HP: {hero.hp}/{hero.max_hp} | Level {hero.level} | XP {hero.xp}")
        print("\n[1] Buy Weapon")
        print("[2] Buy Potion")
        print("[3] View Inventory")
        print("[4] Leave")
        
        choice = input("\nChoose: ").strip()
        
        if choice == "1":
            clear()
            print("╔════════════════════════════════════════╗")
            print("║ WEAPONS                                ║")
            print("╚════════════════════════════════════════╝")
            for i, weapon in enumerate(WEAPONS):
                print(f"[{i+1}] {weapon['name']:<20} ATK+{weapon['bonus']:<2} | {weapon['price']} gold")
            buy = input("\nBuy (number, 0 to cancel): ").strip()
            try:
                idx = int(buy) - 1
                if idx == -1:
                    continue
                if 0 <= idx < len(WEAPONS):
                    weapon = WEAPONS[idx]
                    if hero.gold >= weapon["price"]:
                        hero.gold -= weapon["price"]
                        hero.weapons.append(weapon.copy())
                        print(f"\nBought {weapon['name']}!")
                        input("Press ENTER to continue...")
                    else:
                        print("\nNot enough gold!")
                        input("Press ENTER to continue...")
                else:
                    print("\nInvalid choice!")
                    input("Press ENTER to continue...")
            except:
                print("\nInvalid choice!")
                input("Press ENTER to continue...")
        
        elif choice == "2":
            clear()
            print("╔════════════════════════════════════════╗")
            print("║ POTIONS                                ║")
            print("╚════════════════════════════════════════╝")
            for i, potion in enumerate(POTIONS):
                print(f"[{i+1}] {potion['name']:<20} HEAL+{potion['heal']:<3} | {potion['price']} gold")
            buy = input("\nBuy (number, 0 to cancel): ").strip()
            try:
                idx = int(buy) - 1
                if idx == -1:
                    continue
                if 0 <= idx < len(POTIONS):
                    potion = POTIONS[idx]
                    if hero.gold >= potion["price"]:
                        hero.gold -= potion["price"]
                        hero.potions.append(potion.copy())
                        print(f"\nBought {potion['name']}!")
                        input("Press ENTER to continue...")
                    else:
                        print("\nNot enough gold!")
                        input("Press ENTER to continue...")
                else:
                    print("\nInvalid choice!")
                    input("Press ENTER to continue...")
            except:
                print("\nInvalid choice!")
                input("Press ENTER to continue...")
        
        elif choice == "3":
            clear()
            print("╔════════════════════════════════════════╗")
            print("║ INVENTORY                              ║")
            print("╚════════════════════════════════════════╝")
            print("\nWeapons:")
            for i, weapon in enumerate(hero.weapons):
                equipped = " [EQUIPPED]" if i == hero.equipped_weapon else ""
                print(f"  [{i+1}] {weapon['name']:<20} ATK+{weapon['bonus']}{equipped}")
            print("\nPotions:")
            if hero.potions:
                for i, potion in enumerate(hero.potions):
                    print(f"  [{i+1}] {potion['name']:<20} HEAL+{potion['heal']}")
            else:
                print("  (none)")
            print("\n[1] Equip Weapon")
            print("[2] Back")
            inv_choice = input("\nChoose: ").strip()
            if inv_choice == "1":
                clear()
                print("Equip which weapon?")
                for i, weapon in enumerate(hero.weapons):
                    print(f"  [{i+1}] {weapon['name']}")
                eq = input("\nChoose: ").strip()
                try:
                    idx = int(eq) - 1
                    if 0 <= idx < len(hero.weapons):
                        hero.equipped_weapon = idx
                        print(f"\nEquipped {hero.weapons[idx]['name']}!")
                        input("Press ENTER to continue...")
                except:
                    pass
        
        elif choice == "4":
            break

# ── Room System ──────────────────────────────────────────────────────────────
class GameWorld:
    def __init__(self):
        self.rooms = {}
        self.current_enemy = None
        self.init_rooms()
    
    def init_rooms(self):
        self.rooms = {
            (0, 0): {"name": "Guard Room",      "type": "normal", "enemy": None},
            (1, 0): {"name": "Goblin Den",      "type": "normal", "enemy": None},
            (2, 0): {"name": "Skeleton Crypt",  "type": "normal", "enemy": None},
            (1, 1): {"name": "Merchant's Hall", "type": "shop",   "enemy": None},
            (2, 1): {"name": "Dragon's Lair",   "type": "boss",   "enemy": None},
        }
        self.spawn_enemies()
    
    def spawn_enemies(self):
        for pos in self.rooms:
            room = self.rooms[pos]
            if room["type"] == "normal":
                if random.random() < 0.6:
                    enemy_type = random.choice(["goblin", "skeleton"])
                    room["enemy"] = Enemy(enemy_type)
            elif room["type"] == "boss":
                room["enemy"] = Enemy("dragon")
    
    def get_room(self, x, y):
        return self.rooms.get((x, y))
    
    def describe_room(self, hero):
        room = self.get_room(hero.x, hero.y)
        if not room:
            return "Unknown area."
        
        desc = f"\n{room['name']}\n"
        if room["type"] == "boss":
            desc += "The terrifying dragon awaits...\n"
        elif room["type"] == "shop":
            desc += "A merchant stands ready.\n"
        elif room["enemy"]:
            desc += f"A {room['enemy'].type} lurks here!\n"
        else:
            desc += "This room is empty.\n"
        return desc

# ── Main Game Loop ───────────────────────────────────────────────────────────
def game_over_defeat():
    clear()
    print("╔════════════════════════════════════════╗")
    print("║ DEFEAT                                 ║")
    print("║ You have fallen in the dungeon...      ║")
    print("╚════════════════════════════════════════╝")
    input("\nPress ENTER to quit...")

def game_over_victory():
    clear()
    print("╔════════════════════════════════════════╗")
    print("║ VICTORY!                               ║")
    print("║ You defeated the dragon!               ║")
    print("║ The dungeon is now yours!              ║")
    print("╚════════════════════════════════════════╝")
    input("\nPress ENTER to quit...")

def main():
    hero = Hero()
    world = GameWorld()
    
    clear()
    print("╔════════════════════════════════════════╗")
    print("║ DUNGEON CRAWLER                        ║")
    print("║ Defeat the dragon to escape!           ║")
    print("╚════════════════════════════════════════╝")
    input("\nPress ENTER to begin...")
    
    while True:
        clear()
        print("╔════════════════════════════════════════╗")
        print(f"║ Level {hero.level} | HP {hero.hp}/{hero.max_hp} | ATK {hero.get_attack()} | DEF {hero.get_defense()} | XP {hero.xp} | Gold {hero.gold}")
        print("╚════════════════════════════════════════╝")
        
        room = world.get_room(hero.x, hero.y)
        print(world.describe_room(hero))
        
        print("═" * 40)
        print(f"Position: ({hero.x}, {hero.y})")
        print("Navigation:")
        if world.get_room(hero.x - 1, hero.y):
            print("  [A] Left")
        if world.get_room(hero.x + 1, hero.y):
            print("  [D] Right")
        if world.get_room(hero.x, hero.y - 1):
            print("  [W] Up")
        if world.get_room(hero.x, hero.y + 1):
            print("  [S] Down")
        
        if room["type"] == "shop":
            print("  [E] Enter Shop")
        elif room["enemy"]:
            print("  [E] Fight")
        
        print("  [I] Inventory")
        print("  [Q] Quit Game")
        
        action = input("\nAction: ").strip().lower()
        
        if action == "a":
            if world.get_room(hero.x - 1, hero.y):
                hero.x -= 1
        elif action == "d":
            if world.get_room(hero.x + 1, hero.y):
                hero.x += 1
        elif action == "w":
            if world.get_room(hero.x, hero.y - 1):
                hero.y -= 1
        elif action == "s":
            if world.get_room(hero.x, hero.y + 1):
                hero.y += 1
        elif action == "e":
            if room["type"] == "shop":
                shop(hero)
            elif room["enemy"]:
                result = combat(hero, room["enemy"])
                if result == "victory":
                    room["enemy"] = None
                    if room["type"] == "boss":
                        game_over_victory()
                        return
                elif result == "defeat":
                    game_over_defeat()
                    return
        elif action == "i":
            clear()
            print("╔════════════════════════════════════════╗")
            print("║ INVENTORY                              ║")
            print("╚════════════════════════════════════════╝")
            print("\nWeapons:")
            for i, weapon in enumerate(hero.weapons):
                equipped = " [EQUIPPED]" if i == hero.equipped_weapon else ""
                print(f"  [{i+1}] {weapon['name']:<20} ATK+{weapon['bonus']}{equipped}")
            print("\nPotions:")
            if hero.potions:
                for i, potion in enumerate(hero.potions):
                    print(f"  [{i+1}] {potion['name']:<20} HEAL+{potion['heal']}")
            else:
                print("  (none)")
            input("\nPress ENTER to continue...")
        elif action == "q":
            break
        
        if not hero.is_alive():
            game_over_defeat()
            return

if __name__ == "__main__":
    main()