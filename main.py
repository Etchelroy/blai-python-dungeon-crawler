import random
import os
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ── Items ──────────────────────────────────────────────────────────────────────

WEAPONS = [
    {"name": "Rusty Sword",   "bonus": 2,  "price": 0},
    {"name": "Iron Sword",    "bonus": 5,  "price": 30},
    {"name": "Steel Blade",   "bonus": 10, "price": 60},
    {"name": "Flaming Sword", "bonus": 18, "price": 100},
]

POTIONS = [
    {"name": "Small Potion",  "heal": 20, "price": 15},
    {"name": "Large Potion",  "heal": 50, "price": 35},
]

# ── Enemy templates ────────────────────────────────────────────────────────────

ENEMY_TEMPLATES = {
    "Goblin":   {"hp": 20,  "max_hp": 20,  "attack": 5,  "defense": 1, "xp": 15, "gold": 10},
    "Skeleton": {"hp": 35,  "max_hp": 35,  "attack": 9,  "defense": 3, "xp": 25, "gold": 20},
    "Dragon":   {"hp": 120, "max_hp": 120, "attack": 22, "defense": 8, "xp": 200,"gold": 150},
}

def make_enemy(kind):
    t = ENEMY_TEMPLATES[kind]
    return {k: v for k, v in t.items()}
    
def spawn_enemy():
    r = random.random()
    if r < 0.55:
        return make_enemy("Goblin")
    else:
        return make_enemy("Skeleton")

# ── Rooms ──────────────────────────────────────────────────────────────────────
# Layout (grid):
#   [0:Entrance] -- [1:Forest]
#       |                |
#   [2:Cave]    -- [3:Shop]
#                        |
#                   [4:Dragon's Lair]

ROOM_NAMES = [
    "Entrance Hall",
    "Dark Forest",
    "Damp Cave",
    "Merchant's Shop",
    "Dragon's Lair",
]

CONNECTIONS = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2, 4],
    4: [3],
}

def build_rooms():
    rooms = []
    for i, name in enumerate(ROOM_NAMES):
        room = {
            "name": name,
            "id": i,
            "exits": CONNECTIONS[i],
            "enemy": None,
            "cleared": False,
            "is_shop": i == 3,
            "is_boss": i == 4,
        }
        rooms.append(room)
    # Spawn enemies in non-shop, non-boss rooms
    for r in rooms:
        if not r["is_shop"] and not r["is_boss"]:
            r["enemy"] = spawn_enemy()
    # Boss in final room
    rooms[4]["enemy"] = make_enemy("Dragon")
    return rooms

# ── Hero ───────────────────────────────────────────────────────────────────────

def make_hero():
    return {
        "name": "Hero",
        "hp": 80,
        "max_hp": 80,
        "attack": 12,
        "defense": 4,
        "xp": 0,
        "level": 1,
        "xp_next": 50,
        "gold": 20,
        "weapon": WEAPONS[0].copy(),
        "inventory": [],  # list of potions
    }

def hero_total_attack(hero):
    return hero["attack"] + hero["weapon"]["bonus"]

def level_up(hero):
    while hero["xp"] >= hero["xp_next"]:
        hero["level"] += 1
        hero["xp"] -= hero["xp_next"]
        hero["xp_next"] = int(hero["xp_next"] * 1.6)
        hero["attack"] += 3
        hero["defense"] += 2
        hero["max_hp"] += 15
        hero["hp"] = min(hero["hp"] + 15, hero["max_hp"])
        print(f"\n  ★ LEVEL UP! You are now level {hero['level']}!")
        print(f"    ATK +3 | DEF +2 | Max HP +15")
        input("  Press Enter to continue...")

# ── UI helpers ─────────────────────────────────────────────────────────────────

def bar(val, max_val, length=20, fill='█', empty='░'):
    filled = int(length * val / max(max_val, 1))
    return fill * filled + empty * (length - filled)

def print_header():
    print("=" * 60)
    print("           ⚔  DUNGEON CRAWLER  ⚔")
    print("=" * 60)

def print_hero_stats(hero):
    print(f"\n  Hero  Lv.{hero['level']}   Gold: {hero['gold']}g")
    print(f"  HP  [{bar(hero['hp'], hero['max_hp'], 16)}] {hero['hp']}/{hero['max_hp']}")
    print(f"  XP  [{bar(hero['xp'], hero['xp_next'], 16)}] {hero['xp']}/{hero['xp_next']}")
    print(f"  ATK: {hero_total_attack(hero)} ({hero['attack']}+{hero['weapon']['bonus']})  "
          f"DEF: {hero['defense']}  Weapon: {hero['weapon']['name']}")
    potions = [p['name'] for p in hero['inventory']]
    print(f"  Potions: {', '.join(potions) if potions else 'none'}")

def print_enemy_stats(enemy):
    name = next(k for k, v in ENEMY_TEMPLATES.items() if v["max_hp"] == enemy["max_hp"])
    print(f"\n  Enemy: {name}")
    print(f"  HP  [{bar(enemy['hp'], enemy['max_hp'], 16)}] {enemy['hp']}/{enemy['max_hp']}")
    print(f"  ATK: {enemy['attack']}  DEF: {enemy['defense']}")

# ── Combat ─────────────────────────────────────────────────────────────────────

def combat(hero, enemy, rooms, current_room_id):
    enemy_name = next(k for k, v in ENEMY_TEMPLATES.items() if v["max_hp"] == enemy["max_hp"])
    fled = False
    while hero["hp"] > 0 and enemy["hp"] > 0:
        clear()
        print_header()
        print_hero_stats(hero)
        print("\n" + "-" * 60)
        print_enemy_stats(enemy)
        print("\n" + "-" * 60)
        print("  COMBAT OPTIONS:")
        print("  [1] Attack")
        if hero["inventory"]:
            print("  [2] Use Potion")
        print("  [3] Flee")
        choice = input("\n  > ").strip()

        if choice == "1":
            # Hero attacks
            dmg = max(1, hero_total_attack(hero) - enemy["defense"] + random.randint(-2, 3))
            enemy["hp"] -= dmg
            print(f"\n  You hit {enemy_name} for {dmg} damage!")
            if enemy["hp"] <= 0:
                print(f"\n  ✓ You defeated the {enemy_name}!")
                print(f"  +{enemy['xp']} XP  +{enemy['gold']} gold")
                hero["xp"] += enemy["xp"]
                hero["gold"] += enemy["gold"]
                input("  Press Enter to continue...")
                level_up(hero)
                return "win", fled
            # Enemy attacks
            e_dmg = max(1, enemy["attack"] - hero["defense"] + random.randint(-2, 3))
            hero["hp"] -= e_dmg
            print(f"  {enemy_name} hits you for {e_dmg} damage!")
            if hero["hp"] <= 0:
                input("  Press Enter to continue...")
                return "dead", fled
            input("  Press Enter to continue...")

        elif choice == "2" and hero["inventory"]:
            potion = hero["inventory"].pop(0)
            hero["hp"] = min(hero["hp"] + potion["heal"], hero["max_hp"])
            print(f"\n  You used {potion['name']} and restored {potion['heal']} HP.")
            print(f"  HP is now {hero['hp']}/{hero['max_hp']}")
            # Enemy still attacks
            e_dmg = max(1, enemy["attack"] - hero["defense"] + random.randint(-2, 3))
            hero["hp"] -= e_dmg
            print(f"  {enemy_name} hits you for {e_dmg} damage!")
            if hero["hp"] <= 0:
                input("  Press Enter to continue...")
                return "dead", fled
            input("  Press Enter to continue...")

        elif choice == "3":
            if random.random() < 0.5:
                print("\n  You fled successfully!")
                input("  Press Enter to continue...")
                fled = True
                return "fled", fled
            else:
                print("\n  You failed to flee!")
                e_dmg = max(1, enemy["attack"] - hero["defense"] + random.randint(-2, 3))
                hero["hp"] -= e_dmg
                print(f"  {enemy_name} hits you for {e_dmg} damage while you tried to escape!")
                if hero["hp"] <= 0:
                    input("  Press Enter to continue...")
                    return "dead", fled
                input("  Press Enter to continue...")
        else:
            print("  Invalid choice.")
            input("  Press Enter...")

    return "win" if enemy["hp"] <= 0 else "dead", fled

# ── Shop ───────────────────────────────────────────────────────────────────────

def shop(hero):
    while True:
        clear()
        print_header()
        print_hero_stats(hero)
        print("\n" + "=" * 60)
        print("  MERCHANT'S SHOP")
        print("=" * 60)
        print("\n  WEAPONS:")
        for i, w in enumerate(WEAPONS[1:], 1):
            equipped = " (equipped)" if hero["weapon"]["name"] == w["name"] else ""
            print(f"  [{i}] {w['name']:20s}  ATK+{w['bonus']}   {w['price']}g{equipped}")
        print("\n  POTIONS:")
        for j, p in enumerate(POTIONS, len(WEAPONS)):
            print(f"  [{j}] {p['name']:20s}  +{p['heal']} HP  {p['price']}g")
        print("\n  [0] Leave shop")
        choice = input("\n  > ").strip()
        if choice == "0":
            break
        try:
            idx = int(choice)
            if 1 <= idx <= len(WEAPONS) - 1:
                w = WEAPONS[idx]
                if hero["gold"] >= w["price"]:
                    hero["gold"] -= w["price"]
                    hero["weapon"] = w.copy()
                    print(f"\n  Equipped {w['name']}!")
                else:
                    print("\n  Not enough gold!")
                input("  Press Enter...")
            elif len(WEAPONS) <= idx < len(WEAPONS) + len(POTIONS):
                p = POTIONS[idx - len(WEAPONS)]
                if hero["gold"] >= p["price"]:
                    hero["gold"] -= p["price"]
                    hero["inventory"].append(p.copy())
                    print(f"\n  Bought {p['name']}!")
                else:
                    print("\n  Not enough gold!")
                input("  Press Enter...")
        except ValueError:
            pass

# ── Game over / victory ────────────────────────────────────────────────────────

def game_over():
    clear()
    print("=" * 60)
    print("""
   ██████╗  █████╗ ███╗   ███╗███████╗
  ██╔════╝ ██╔══██╗████╗ ████║██╔════╝
  ██║  ███╗███████║██╔████╔██║█████╗  
  ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  
  ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
                OVER
    """)
    print("=" * 60)
    print("\n  You have fallen in the dungeon...")
    print("  Better luck next time, brave hero.\n")
    input("  Press Enter to exit...")

def victory():
    clear()
    print("=" * 60)
    print("""
 ██╗   ██╗██╗ ██████╗████████╗ ██████╗ ██████╗ ██╗   ██╗
 ██║   ██║██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝
 ██║   ██║██║██║        ██║   ██║   ██║██████╔╝ ╚████╔╝ 
 ╚██╗ ██╔╝██║██║        ██║   ██║   ██║██╔══██╗  ╚██╔╝  
  ╚████╔╝ ██║╚██████╗   ██║   ╚██████╔╝██║  ██║   ██║   
   ╚═══╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝  
    """)
    print("=" * 60)
    print("\n  You slew the Dragon and saved the realm!")
    print("  The dungeon is clear. You are a legend!\n")
    input("  Press Enter to exit...")

# ── Main loop ──────────────────────────────────────────────────────────────────

def main():
    clear()
    print_header()
    print("""
  Welcome, brave adventurer!
  Navigate 5 rooms, defeat enemies, shop for gear,
  and slay the Dragon to claim victory!

  Controls: Enter the number of your choice at each prompt.
    """)
    hero_name = input("  Enter your hero's name: ").strip() or "Hero"
    hero = make_hero()
    hero["name"] = hero_name
    rooms = build_rooms()
    current = 0  # start at Entrance Hall

    while True:
        room = rooms[current]
        clear()
        print_header()
        print_hero_stats(hero)
        print("\n" + "=" * 60)
        print(f"  ROOM: {room['name']}")
        print("=" * 60)

        # Shop room
        if room["is_shop"]:
            print("\n  A merchant greets you with a smile.")
            print("  [1] Enter the shop")
            print("  [2] Move to another room")
            ch = input("\n  > ").strip()
            if ch == "1":
                shop(hero)
                continue
            elif ch == "2":
                pass  # fall through to movement
            else:
                continue

        # Boss room
        elif room["is_boss"] and not room["cleared"]:
            print("\n  The air grows hot. You hear heavy breathing...")
            print("  The DRAGON awaits!")
            print("\n  [1] Fight the Dragon!")
            print("  [2] Retreat (go back)")
            ch = input("\n  > ").strip()
            if ch == "1":
                result, _ = combat(hero, room["enemy"], rooms, current)
                if result == "dead":
                    game_over()
                    sys.exit()
                elif result == "win":
                    room["cleared"] = True
                    victory()
                    sys.exit()
                # fled back to previous room handled below via movement
                continue
            elif ch == "2":
                pass  # fall through to movement
            else:
                continue

        # Normal room with living enemy
        elif not room["is_shop"] and not room["is_boss"] and not room["cleared"] and room["enemy"]:
            ename = next(k for k, v in ENEMY_TEMPLATES.items() if v["max_hp"] == room["enemy"]["max_hp"])
            print(f"\n  A {ename} blocks your path!")
            print("\n  [1] Fight!")
            print("  [2] Move to another room (flee room)")
            ch = input("\n  > ").strip()
            if ch == "1":
                result, _ = combat(hero, room["enemy"], rooms, current)
                if result == "dead":
                    game_over()
                    sys.exit()
                elif result == "win":
                    room["cleared"] = True
                    room["enemy"] = None
                continue
            elif ch == "2":
                pass  # fall through to movement
            else:
                continue

        elif room["cleared"]:
            print("\n  This room is cleared.")

        # Movement
        print("\n  EXITS:")
        for i, exit_id in enumerate(room["exits"], 1):
            status = ""
            r = rooms[exit_id]
            if r["cleared"]:
                status = " [cleared]"
            elif r["is_shop"]:
                status = " [SHOP]"
            elif r["is_boss"]:
                status = " [BOSS]"
            elif r["enemy"]:
                ename = next(k for k, v in ENEMY_TEMPLATES.items() if v["max_hp"] == r["enemy"]["max_hp"])
                status = f" [{ename}]"
            print(f"  [{i}] Go to {r['name']}{status}")
        print("  [0] Stay / look around")

        ch = input("\n  > ").strip()
        if ch == "0":
            continue
        try:
            idx = int(ch) - 1
            if 0 <= idx < len(room["exits"]):
                current = room["exits"][idx]
            else:
                print("  Invalid exit.")
                input("  Press Enter...")
        except ValueError:
            print("  Invalid choice.")
            input("  Press Enter...")

if __name__ == "__main__":
    main()