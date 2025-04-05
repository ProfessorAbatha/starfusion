
import pygame
import time
import math
import json

pygame.init()

with open("config.json") as f:
    config = json.load(f)

WIDTH, HEIGHT = 1000, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stellar Forge: Clicker Prototype")

WHITE = (255, 255, 255)
GRAY = (30, 30, 30)
BLUE = (100, 149, 237)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

font = pygame.font.SysFont("Arial", 24)

clicks = 0
stage = "Hydrogen Cloud"
auto_cps = 0
fusion_stage = 0
element_fuel = config["element_fuel"].copy()
fusion_table = config["fusion_table"]
max_stage = len(fusion_table) - 1

clock = pygame.time.Clock()
running = True

def draw_window():
    win.fill(GRAY)
    pygame.draw.circle(win, YELLOW, (WIDTH//2, HEIGHT//2), 60)
    fuel = element_fuel[fusion_table[fusion_stage]["name"]]
    stage_info = f"{fusion_table[fusion_stage]['name']} → {fusion_table[fusion_stage]['next']}"
    texts = [
        f"Stage: {stage}",
        f"Clicks: {int(clicks)}",
        f"Auto-CPS: {auto_cps}",
        f"Fuel: {fuel:.0f} {fusion_table[fusion_stage]['name']}",
        f"Fusion Stage: {stage_info}"
    ]
    for i, txt in enumerate(texts):
        surf = font.render(txt, True, WHITE)
        win.blit(surf, (20, 20 + i*30))
    pygame.draw.rect(win, WHITE, (20, 200, 300, 20), 2)
    progress = min(1.0, clicks / config["protostar_threshold"]) if stage == "Hydrogen Cloud" else min(1.0, clicks / config["fusion_threshold"])
    pygame.draw.rect(win, BLUE, (22, 202, progress * 296, 16))
    pygame.display.update()

while running:
    clock.tick(60)
    clicks += auto_cps / 60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if math.hypot(mx - WIDTH//2, my - HEIGHT//2) <= 60:
                clicks += 1

    if stage == "Hydrogen Cloud" and clicks >= config["protostar_threshold"]:
        stage = "Protostar"
        auto_cps = 1
    elif stage == "Protostar" and clicks >= config["fusion_threshold"]:
        stage = "Fusion"
        auto_cps = 2

    current = fusion_table[fusion_stage]
    if stage == "Fusion" and element_fuel[current["name"]] >= current["cost"]:
        element_fuel[current["name"]] -= current["cost"]
        next_elem = current["next"]
        if next_elem in element_fuel:
            element_fuel[next_elem] += 1
        if element_fuel[current["name"]] <= 0 and fusion_stage < max_stage:
            fusion_stage += 1

    draw_window()

pygame.quit()
