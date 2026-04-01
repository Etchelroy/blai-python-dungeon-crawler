import random
import os
import sys

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
        print(f"\nHero HP:   {hero.hp}/{hero.max_hp}")
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
                    print(f"  [{i+1}] {potion['name']} ({potion['heal']} HP) x{hero.potions.count(potion)}")
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
                        continue
                except:
                    print("Invalid choice!")
                    continue
                    
        elif choice == "3":
            if random.random() < 0.4:
                print("You fled successfully!")
                return "fled"
            else:
                print("Failed to flee!")
                enemy_damage = enemy.attack + random.randint(-1, 2)
                taken = hero.take_damage(enemy_damage)
                print(f"{enemy_name} attacked! You took {taken} damage.")
        else:
            print("Invalid choice!")
            continue
        
        input("\nPress Enter to continue...")
        clear()
    
    if hero.is_alive():
        print(f"Victory! You defeated the {enemy_name}!")
        print(f"Gained {enemy.xp_reward} XP and {enemy.gold_reward} gold.")
        hero.gain_xp(enemy.xp_reward)
        hero.gold += enemy.gold_reward
        return "victory"
    else:
        return "defeat"

# ── Shop ─────────────────────────────────────────────────────────────────────
def shop(hero):
    while True:
        clear()
        print("╔════════════════════════════════════════╗")
        print("║ SHOP                                   ║")
        print("╚════════════════════════════════════════╝")
        print(f"\nGold: {hero.gold}")
        print(f"\n[WEAPONS]")
        for i, weapon in enumerate(WEAPONS):
            owned = "✓" if any(w["name"] == weapon["name"] for w in hero.weapons) else " "
            print(f"  [{owned}] {weapon['name']:<20} {weapon['price']:>3}g (ATK +{weapon['bonus']})")
        
        print(f"\n[POTIONS]")
        for i, potion in enumerate(POTIONS):
            print(f"  [{i+1}] {potion['name']:<20} {potion['price']:>3}g ({potion['heal']} HP)")
        
        print("\n[0] Exit Shop")
        choice = input("\nBuy item (0-7): ").strip()
        
        if choice == "0":
            return
        elif choice in ["1", "2", "3", "4"]:
            idx = int(choice) - 1
            weapon = WEAPONS[idx]
            if hero.gold >= weapon["price"]:
                if any(w["name"] == weapon["name"] for w in hero.weapons):
                    print("Already own this weapon!")
                else:
                    hero.gold -= weapon["price"]
                    hero.weapons.append(weapon.copy())
                    print(f"Purchased {weapon['name']}!")
            else:
                print("Not enough gold!")
        elif choice in ["5", "6", "7"]:
            idx = int(choice) - 5
            potion = POTIONS[idx]
            if hero.gold >= potion["price"]:
                hero.gold -= potion["price"]
                hero.potions.append(potion.copy())
                print(f"Purchased {potion['name']}!")
            else:
                print("Not enough gold!")
        else:
            print("Invalid choice!")
        
        input("\nPress Enter to continue...")

# ── Room Display ─────────────────────────────────────────────────────────────
def display_room(hero, room_type, enemy=None):
    clear()
    print("╔════════════════════════════════════════╗")
    print(f"║ ROOM ({hero.x},{hero.y})                        ║")
    print("╚════════════════════════════════════════╝")
    
    print(f"\nHP: {hero.hp}/{hero.max_hp} | ATK: {hero.get_attack()} | DEF: {hero.get_defense()} | Level: {hero.level} | XP: {hero.xp} | Gold: {hero.gold}")
    print(f"Weapon: {hero.weapons[hero.equipped_weapon]['name']}")
    
    if room_type == "shop":
        print("\n[SHOP] A merchant stands ready to trade.")
    elif room_type == "boss":
        print("\n[BOSS ROOM] The dragon awaits...\n")
        if enemy:
            print(f"Enemy: {enemy.type.upper()} (HP: {enemy.hp}/{enemy.max_hp})")
    elif room_type == "enemy":
        print(f"\n[ENEMY] An {enemy.type} appears!\n")
        print(f"Enemy: {enemy.type.capitalize()} (HP: {enemy.hp}/{enemy.max_hp})")
    else:
        print("\n[EMPTY] The room is empty.")
    
    print("\n[W/A/S/D] Move | [I] Inventory | [E] Equipment | [Enter] Interact")

# ── Inventory ────────────────────────────────────────────────────────────────
def inventory(hero):
    clear()
    print("╔════════════════════════════════════════╗")
    print("║ INVENTORY                              ║")
    print("╚════════════════════════════════════════╝")
    
    print(f"\nGold: {hero.gold}")
    print(f"\n[WEAPONS] ({len(hero.weapons)})")
    for i, weapon in enumerate(hero.weapons):
        equipped = "★" if i == hero.equipped_weapon else " "
        print(f"  [{equipped}] {weapon['name']:<20} ATK +{weapon['bonus']}")
    
    print(f"\n[POTIONS] ({len(hero.potions)})")
    potion_counts = {}
    for potion in hero.potions:
        potion_counts[potion["name"]] = potion_counts.get(potion["name"], 0) + 1
    for potion_name, count in potion_counts.items():
        for potion in POTIONS:
            if potion["name"] == potion_name:
                print(f"  {potion_name:<20} x{count}")
                break
    
    print("\n[0] Back")
    choice = input("Choose option: ").strip()

def equipment(hero):
    clear()
    print("╔════════════════════════════════════════╗")
    print("║ EQUIPMENT                              ║")
    print("╚════════════════════════════════════════╝")
    
    print(f"\nWeapons:")
    for i, weapon in enumerate(hero.weapons):
        equipped = "★" if i == hero.equipped_weapon else " "
        print(f"  [{equipped}] {i+1}: {weapon['name']:<20} ATK +{weapon['bonus']}")
    
    print("\n[0] Back")
    choice = input("Equip weapon (0-5): ").strip()
    if choice == "0":
        return
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(hero.weapons):
            hero.equipped_weapon = idx
            print(f"Equipped {hero.weapons[idx]['name']}!")
        else:
            print("Invalid choice!")
    except:
        print("Invalid choice!")
    input("\nPress Enter to continue...")

# ── Main Game ────────────────────────────────────────────────────────────────
def main():
    hero = Hero()
    rooms = {}
    
    # Initialize 5-room grid: (0,0)-(2,2) with (1,1) as center (shop)
    for x in range(0, 3):
        for y in range(0, 3):
            if (x, y) == (1, 1):
                rooms[(x, y)] = {"type": "shop", "enemy": None}
            elif (x, y) == (2, 2):
                rooms[(x, y)] = {"type": "boss", "enemy": Enemy("dragon")}
            else:
                if random.random() < 0.6:
                    enemy_type = random.choice(["goblin", "skeleton"])
                    rooms[(x, y)] = {"type": "enemy", "enemy": Enemy(enemy_type)}
                else:
                    rooms[(x, y)] = {"type": "empty", "enemy": None}
    
    # Ensure spawn room is empty
    rooms[(1, 1)]["type"] = "shop"
    rooms[(1, 1)]["enemy"] = None
    
    game_over = False
    
    while not game_over:
        current_room = rooms[(hero.x, hero.y)]
        display_room(hero, current_room["type"], current_room["enemy"])
        
        choice = input("\nAction: ").strip().lower()
        
        if choice == "w" and hero.y > 0:
            hero.y -= 1
        elif choice == "s" and hero.y < 2:
            hero.y += 1
        elif choice == "a" and hero.x > 0:
            hero.x -= 1
        elif choice == "d" and hero.x < 2:
            hero.x += 1
        elif choice == "i":
            inventory(hero)
        elif choice == "e":
            equipment(hero)
        elif choice == "":
            if current_room["type"] == "shop":
                shop(hero)
            elif current_room["type"] == "enemy" and current_room["enemy"]:
                result = combat(hero, current_room["enemy"])
                if result == "victory":
                    current_room["enemy"] = None
                    current_room["type"] = "empty"
                elif result == "defeat":
                    clear()
                    print("╔════════════════════════════════════════╗")
                    print("║ YOU DIED                               ║")
                    print("╚════════════════════════════════════════╝")
                    print(f"\nReached Level: {hero.level}")
                    print(f"Total XP: {hero.xp}")
                    game_over = True
                input("\nPress Enter to continue...")
            elif current_room["type"] == "boss" and current_room["enemy"]:
                result = combat(hero, current_room["enemy"])
                if result == "victory":
                    clear()
                    print("╔════════════════════════════════════════╗")
                    print("║ VICTORY! DRAGON DEFEATED!             ║")
                    print("╚════════════════════════════════════════╝")
                    print(f"\nFinal Level: {hero.level}")
                    print(f"Total XP: {hero.xp}")
                    print(f"Total Gold: {hero.gold}")
                    game_over = True
                elif result == "defeat":
                    clear()
                    print("╔════════════════════════════════════════╗")
                    print("║ DEFEATED BY THE DRAGON                 ║")
                    print("╚════════════════════════════════════════╝")
                    print(f"\nReached Level: {hero.level}")
                    print(f"Total XP: {hero.xp}")
                    game_over = True
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()