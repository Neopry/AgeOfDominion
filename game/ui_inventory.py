import pygame
import json
import os

# Inicializace Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Inventář")
font = pygame.font.Font(None, 28)

# Barvy
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)

# Cesty
ITEMS_FILE = os.path.join("data", "items.json")
ICONS_PATH = os.path.join("assets", "icons")

# Přidání cesty k obrázku pozadí
BACKGROUND_IMAGE = os.path.join("assets", "backgrounds", "inventory_bg.jpg")

# Cesty k zvukovým souborům
HOVER_SOUND = os.path.join("assets", "sounds", "hover.wav")
CLICK_SOUND = os.path.join("assets", "sounds", "click.wav")

# Načtení zvuků
hover_sound = pygame.mixer.Sound(HOVER_SOUND) if os.path.exists(HOVER_SOUND) else None
click_sound = pygame.mixer.Sound(CLICK_SOUND) if os.path.exists(CLICK_SOUND) else None

# Funkce pro načtení předmětů
def load_items(file_path):
    if not os.path.exists(file_path):
        print(f"Chyba: Soubor {file_path} neexistuje.")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            items = json.load(f)
            # Ověření, že každá položka je slovník
            if not all(isinstance(item, dict) for item in items):
                print("Chyba: Některé položky nejsou ve správném formátu (dict).")
                return []
            items.sort(key=lambda x: x["name"])
            return items
    except json.JSONDecodeError as e:
        print(f"Chyba při načítání JSON: {e}")
        return []

# Funkce pro uložení stavu inventáře
def save_inventory_state(items, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Chyba při ukládání inventáře: {e}")

# Funkce pro načtení stavu inventáře
def load_inventory_state(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Chyba při načítání stavu inventáře: {e}")
        return []

# Načtení obrázku pozadí
if os.path.exists(BACKGROUND_IMAGE):
    background_img = pygame.image.load(BACKGROUND_IMAGE)
    background_img = pygame.transform.scale(background_img, screen.get_size())
else:
    background_img = None

# Funkce pro vykreslení zaobleného obdélníku
def draw_rounded_rect(surface, color, rect, corner_radius, width=0):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius, width=width)

# Upravená funkce pro vykreslení tooltipu s moderním vzhledem
def draw_tooltip(surface, text, pos):
    tooltip_surf = font.render(text, True, WHITE)
    tooltip_rect = tooltip_surf.get_rect(topleft=pos)
    shadow_rect = tooltip_rect.inflate(14, 10).move(2, 2)  # Stín
    pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=8)  # Poloprůhledný stín
    draw_rounded_rect(surface, LIGHT_BLUE, tooltip_rect.inflate(14, 10), 8)  # Modré pozadí
    surface.blit(tooltip_surf, tooltip_rect.topleft)

# Stav vybraných položek
selected_items = set()

# Upravená funkce pro vykreslení položek s vybraným stavem
def draw_items(surface, items, mouse_pos):
    cols = max(1, screen.get_width() // 150)  # Dynamický počet sloupců
    spacing = 120
    start_x = 50
    start_y = 50
    tooltip = None
    global last_hovered_item

    for i, item in enumerate(items):
        # Ověření, že item je slovník
        if not isinstance(item, dict):
            print(f"Chyba: Položka na indexu {i} není slovník. Přeskakuji.")
            continue

        x = start_x + (i % cols) * spacing
        y = start_y + (i // cols) * spacing

        # Zkusit načíst ikonu
        icon_path = os.path.join(ICONS_PATH, item.get("icon", ""))
        if os.path.exists(icon_path):
            icon_img = pygame.image.load(icon_path)
            icon_img = pygame.transform.scale(icon_img, (64, 64))
        else:
            icon_img = pygame.Surface((64, 64))
            icon_img.fill(GRAY)

        # Detekce myši a animace
        rect = pygame.Rect(x, y, 64, 64)
        if rect.collidepoint(*mouse_pos):
            if hover_sound and last_hovered_item != i:
                hover_sound.play()  # Přehrát zvuk při najetí
            last_hovered_item = i
            icon_img = pygame.transform.scale(icon_img, (72, 72))  # Zvýraznění
            draw_rounded_rect(surface, LIGHT_BLUE, rect.inflate(8, 8), 8, 3)  # Modrý rámeček
            tooltip = f"{item['name']}: {item.get('description', '')}"
        else:
            draw_rounded_rect(surface, GRAY, rect, 8, 1)  # Šedý rámeček

        # Zobrazit stav vybrané položky
        if i in selected_items:
            draw_rounded_rect(surface, (255, 215, 0), rect.inflate(10, 10), 8, 3)  # Zlatý rámeček

        surface.blit(icon_img, (x, y))

    return tooltip

# Načtení předmětů a stavu inventáře
items = load_items(ITEMS_FILE)
inventory_state_file = os.path.join("data", "inventory_state.json")
saved_state = load_inventory_state(inventory_state_file)
if saved_state:
    items = saved_state

# Inventář - hlavní smyčka
running = True
clock = pygame.time.Clock()
last_hovered_item = None
while running:
    # Vykreslení pozadí s poloprůhledným překryvem
    if background_img:
        screen.blit(background_img, (0, 0))
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 100))  # Poloprůhledný bílý překryv
        screen.blit(overlay, (0, 0))
    else:
        screen.fill(WHITE)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_inventory_state(items, inventory_state_file)  # Uložit stav při ukončení
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Levé tlačítko myši
            for i, item in enumerate(items):
                x = start_x + (i % cols) * spacing
                y = start_y + (i // cols) * spacing
                rect = pygame.Rect(x, y, 64, 64)
                if rect.collidepoint(mouse_x, mouse_y):
                    if click_sound:
                        click_sound.play()  # Přehrát zvuk při kliknutí
                    if i in selected_items:
                        selected_items.remove(i)  # Zrušit výběr
                    else:
                        selected_items.add(i)  # Přidat do výběru

    # Vykreslení položek a získání tooltipu
    tooltip = draw_items(screen, items, (mouse_x, mouse_y))

    # Zobrazit tooltip pokud existuje
    if tooltip:
        draw_tooltip(screen, tooltip, (mouse_x + 10, mouse_y + 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
