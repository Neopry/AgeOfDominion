import pygame
import json
import os

# Konfigurace
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ITEM_BOX_SIZE = 80
FONT_SIZE = 18
ITEMS_PER_ROW = 6

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Inventář")
font = pygame.font.Font(None, FONT_SIZE)

# Načtení dat s kontrolou formátu
with open("data/items.json", "r", encoding="utf-8") as f:
    try:
        data = json.load(f)
        # Extrahování všech položek z hierarchie JSON
        items = []
        if "resources" in data:
            for category, category_items in data["resources"].items():
                if isinstance(category_items, list):
                    for item in category_items:
                        if isinstance(item, dict):
                            items.append(item)
                        else:
                            print(f"Chyba: Položka {item} v kategorii {category} není slovník. Přeskakuji.")
        if "buildings" in data and isinstance(data["buildings"], list):
            for item in data["buildings"]:
                if isinstance(item, dict):
                    items.append(item)
                else:
                    print(f"Chyba: Položka {item} v 'buildings' není slovník. Přeskakuji.")
        if "crafting" in data and isinstance(data["crafting"], list):
            for item in data["crafting"]:
                if isinstance(item, dict):
                    items.append(item)
                else:
                    print(f"Chyba: Položka {item} v 'crafting' není slovník. Přeskakuji.")
    except json.JSONDecodeError as e:
        print(f"Chyba při načítání JSON: {e}")
        items = []

def load_icon(path):
    full_path = os.path.join("assets", "icons", os.path.basename(path))
    try:
        return pygame.transform.scale(pygame.image.load(full_path), (64, 64))
    except:
        return None

# Vykreslování inventáře
def draw_inventory():
    screen.fill((40, 40, 40))
    x = 20
    y = 20
    for index, item in enumerate(items):
        if index > 0 and index % ITEMS_PER_ROW == 0:
            x = 20
            y += ITEM_BOX_SIZE + 20

        # Ověření, že item je slovník (pro jistotu)
        if isinstance(item, dict):
            icon = load_icon(item.get("icon", ""))
        else:
            icon = load_icon("")  # Default icon or handle appropriately

        pygame.draw.rect(screen, (100, 100, 100), (x, y, ITEM_BOX_SIZE, ITEM_BOX_SIZE))
        if icon:
            screen.blit(icon, (x + 8, y + 8))
        name_surface = font.render(item["name"], True, (255, 255, 255))
        screen.blit(name_surface, (x, y + ITEM_BOX_SIZE + 5))

        x += ITEM_BOX_SIZE + 20

# Hlavní smyčka
running = True
while running:
    draw_inventory()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()
