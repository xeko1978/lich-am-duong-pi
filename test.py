import pygame
import os
import random

# ---------------- CONFIG ----------------
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 480

WALLPAPER_DIR = "wallpaper"

BG_CHANGE_TIME     = 60_000   # 60 giây (ms)
PANEL_CHANGE_TIME  = 30_000   # 30 giây (ms)

PANEL_SIZE = (300, 200)
PANEL_POS  = (50, 50)
# ----------------------------------------


def load_random_image(path, size=None, alpha=False):
    files = [
        f for f in os.listdir(path)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if not files:
        return None

    filename = random.choice(files)
    img = pygame.image.load(os.path.join(path, filename))

    if alpha:
        img = img.convert_alpha()
    else:
        img = img.convert()

    if size:
        img = pygame.transform.smoothscale(img, size)

    return img


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Wallpaper Demo")

    clock = pygame.time.Clock()

    # --- load ảnh lần đầu ---
    background = load_random_image(
        WALLPAPER_DIR,
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        alpha=False
    )

    panel_surface = pygame.Surface(PANEL_SIZE, pygame.SRCALPHA)
    panel_image = load_random_image(
        WALLPAPER_DIR,
        PANEL_SIZE,
        alpha=True
    )

    panel_surface.blit(panel_image, (0, 0))

    # --- timer ---
    last_bg_change    = pygame.time.get_ticks()
    last_panel_change = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = pygame.time.get_ticks()

        # --- đổi background mỗi 60s ---
        if now - last_bg_change >= BG_CHANGE_TIME:
            bg = load_random_image(
                WALLPAPER_DIR,
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                alpha=False
            )
            if bg:
                background = bg
            last_bg_change = now

        # --- đổi panel mỗi 30s ---
        if now - last_panel_change >= PANEL_CHANGE_TIME:
            img = load_random_image(
                WALLPAPER_DIR,
                PANEL_SIZE,
                alpha=True
            )
            if img:
                panel_surface.fill((0, 0, 0, 0))
                panel_surface.blit(img, (0, 0))
            last_panel_change = now

        # --- render ---
        if background:
            screen.blit(background, (0, 0))

        screen.blit(panel_surface, PANEL_POS)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
