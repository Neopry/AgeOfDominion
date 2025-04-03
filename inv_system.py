import json

class Inventory:
    def __init__(self, max_weight=50):
        self.items = {}
        self.max_weight = max_weight
        self.current_weight = 0
        self.base_speed = 100  # Základní rychlost hráče v %
    
    def load_items(self, json_data):
        """Načte data o všech dostupných předmětech z JSON souboru"""
        self.all_items = {item["name"]: item for category in json_data["resources"].values() for item in category}
    
    def add_item(self, item_name, quantity=1):
        """Přidá předmět do inventáře, pokud nepřesáhne max hmotnost"""
        if item_name in self.all_items:
            item = self.all_items[item_name]
            item_weight = item.get("weight", 0) * quantity
            new_weight = self.current_weight + item_weight
            
            # Ověření max hmotnosti
            if new_weight > self.max_weight + 20:  # Limit přetížení (o 20 kg víc než max)
                print(f"❌ Nelze přidat {item_name}, příliš těžké!")
                return False
            
            if item_name in self.items:
                self.items[item_name]["quantity"] += quantity
            else:
                self.items[item_name] = {"quantity": quantity, "weight": item_weight}
            
            self.current_weight = new_weight
            return True
        return False
    
    def remove_item(self, item_name, quantity=1):
        """Odebere předmět z inventáře"""
        if item_name in self.items and self.items[item_name]["quantity"] >= quantity:
            item_weight = self.all_items[item_name].get("weight", 0) * quantity
            self.items[item_name]["quantity"] -= quantity
            self.current_weight -= item_weight
            
            if self.items[item_name]["quantity"] <= 0:
                del self.items[item_name]
            return True
        return False
    
    def calculate_speed(self):
        """Vypočítá rychlost hráče na základě přetížení"""
        overload = max(0, self.current_weight - self.max_weight)
        speed_penalty = overload  # 1 kg nadváhy = -1 % rychlosti
        return max(30, self.base_speed - speed_penalty)  # Min. rychlost 30 %
    
    def get_inventory(self):
        """Vrátí aktuální obsah inventáře"""
        return {
            "items": self.items,
            "weight": self.current_weight,
            "capacity": f"{self.current_weight}/{self.max_weight} kg ({(self.current_weight/self.max_weight) * 100:.1f}%)",
            "speed": self.calculate_speed()
        }
    
    def save_inventory(self, filename="inventory.json"):
        """Uloží inventář do JSON souboru"""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.get_inventory(), file, indent=4, ensure_ascii=False)
    
    def load_inventory(self, filename="inventory.json"):
        """Načte inventář z JSON souboru"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.items = data["items"]
                self.current_weight = data["weight"]
        except FileNotFoundError:
            print("❌ Soubor s inventářem nenalezen.")

# Načtení JSON dat
with open("game_data.json", "r", encoding="utf-8") as file:
    game_data = json.load(file)

inventory = Inventory(max_weight=50)
inventory.load_items(game_data)

# Přidání předmětů
test_items = ["Kámen", "Kláda", "Klacek"]
for item in test_items:
    inventory.add_item(item, 5)

# Výpis obsahu inventáře
print(json.dumps(inventory.get_inventory(), indent=4, ensure_ascii=False))

# Uložení inventáře
inventory.save_inventory()
