from ast import Import, Return
import datetime
import random
import os
import sys
import pygame
from lunar_hnd import LunarDate
from functions import FreeWeather
from functions import CustomText

from functions import Pygame_Functions
class LunarPygame:
    # ================== SIZE ==================
    PORTRAIT_RATIO = 16 / 9
    BASE_WIDTH = 500
    BASE_HEIGHT = 888
    FOOTER_RATIO = 0.13
    WALLPAPER_DIR = "wallpaper"
    def __init__(self):
        # Khởi tạo pygame
        pygame.init()
        SW, SH = self.BASE_WIDTH, self.BASE_HEIGHT
        #SW, SH = 500, 888

        if SW >= SH:
            self.H = SH
            self.W = int(self.H / self.PORTRAIT_RATIO)
            self.X = (SW - self.W) // 2
            self.Y = 0
        else:
            self.W, self.H = SW, SH
            self.X = self.Y = 0

        self.scale = min(self.W / self.BASE_WIDTH, self.H / self.BASE_HEIGHT)
        self.footer_h = int(self.H * self.FOOTER_RATIO)
        self.content_h = self.H - self.footer_h
        
        self.screen = pygame.display.set_mode((self.BASE_WIDTH, self.BASE_HEIGHT))
        self.clock = pygame.time.Clock()

        # Tạo renderer
        self.pyfunc = Pygame_Functions()

        # Tạo các font
        self.font1 = pygame.font.SysFont('Times New Roman', 24)
        self.font2 = pygame.font.SysFont('Times New Roman', 20)

        # Danh sách texts
        self.texts = [
            "Đây là dòng text đầu tiên rất dài cần xuống dòng khi vượt quá chiều rộng",
            "Text thứ hai",
            "Text thứ ba cũng rất dài và sẽ được xuống dòng tự động khi cần thiết"
        ]

        # Màu sắc cho từng text
        self.colors = [
            (255, 0, 0),    # Đỏ
            (0, 255, 0),    # Xanh lá
            (0, 0, 255)     # Xanh dương
        ]

        # Font cho từng text
        self.fonts = [self.font1, self.font2, self.font1]

    def load_random_image(self, path, size=None, alpha=False):
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
    def run(self):
        # Game loop
                
        bg = self.load_random_image(
            self.WALLPAPER_DIR,
            (self.W, self.H),
            alpha=False
        )
        if bg:
            self.screen.blit(bg, (0, 0))

        # Vẽ panel
        Return=self.panel_rect = self.pyfunc.create_panel(
            screen=self.screen,
            pygame=pygame,
            x=100,
            y=100,
            panel_color=(240, 240, 240, 150),  # Màu nền với alpha
            panel_border_color=(100, 100, 100),
            panel_transparent=False,            # Panel trong suốt
            texts=self.texts,
            text_colors=self.colors,
            text_fonts=self.fonts,
            gap=8,                            # Khoảng cách giữa các dòng
            auto_expand_height=True,          # Tự động tăng chiều cao
            border_width=2,
            padding=15,
            max_width=300,                    # Chiều rộng tối đa
            max_height=100                    # Chiều cao tối đa
        )
        pygame.display.flip()
        self.clock.tick(30)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
        sys.exit()     
if __name__ == "__main__":
        # Game loop
        app=LunarPygame()
        app.run()