import time
import random
import os
import sys
from turtle import update
import pygame
from lunar_hnd import LunarDate
from functions import FreeWeather
from functions import CustomText
from functions import Pygame_Functions
from datetime import datetime
# ================== SIZE ==================
PORTRAIT_RATIO = 16 / 9
BASE_WIDTH = 500
BASE_HEIGHT = 888
FOOTER_RATIO = 0.13
WALLPAPER_DIR = "wallpaper"

# ================== COLORS ==================
COLOR_MONTH = (0,0,0)
COLOR_DAY_NORMAL = (28,70,176)
COLOR_DAY_SUNDAY = (227,36,36)
COLOR_WEEKDAY_NORMAL = (28,70,176)
COLOR_WEEKDAY_WEEKEND = (227,36,36)
COLOR_DAYNOTE = (227,36,36)
COLOR_QUOTE = (28,70,176)
COLOR_AUTHOR = (243,156,18)
COLOR_LABEL = (127,140,141)
COLOR_TIME = (28,70,176)
COLOR_LUNAR = (0,0,0)
COLOR_FOOTER_BG = (207,230,168)
COLOR_SEPARATOR = (0,0,0)
COLOR_HOANG_DAO = (211,84,0)
COLOR_HAC_DAO = (127,140,141)
COLOR_WEATHER = (0,0,0)
COLOR_MAIN_PANEL = (245,245,245)
COLOR_MAIN_PANEL_BORDER=(0,0,0)

WEEKDAYS = ["Thứ Hai","Thứ Ba","Thứ Tư","Thứ Năm","Thứ Sáu","Thứ Bảy","Chủ Nhật"]
class LunarPygame:

    # ================== SPACING ==================


    def __init__(self):
        # Khởi tạo pygame
        pygame.init()
        info = pygame.display.Info()
        SW, SH = info.current_w, info.current_h
        SW, SH = 500, 888
        print(info.current_w, info.current_h)
        #SW, SH = 500, 888

        if SW >= SH:
            self.H = SH
            self.W = int(self.H / PORTRAIT_RATIO)
            self.X = (SW - self.W) // 2
            self.Y = 0
        else:
            self.W, self.H = SW, SH
            self.X = self.Y = 0

        self.scale = min(self.W / BASE_WIDTH, self.H / BASE_HEIGHT)
        self.footer_h = int(self.H * FOOTER_RATIO)
        self.content_h = self.H - self.footer_h
        
        self.screen = pygame.display.set_mode((self.W, self.H))
        self.clock = pygame.time.Clock()
        self.background = None

        # Tạo renderer
        self.pyfunc = Pygame_Functions()

        # Tạo các font với kích thước khác nhau
        self.font_month = pygame.font.SysFont('Times New Roman', int(20*self.scale), bold=False)
        self.font_day = pygame.font.SysFont('Times New Roman', int(140*self.scale), bold=True)
        self.font_weekday = pygame.font.SysFont('Times New Roman', int(26*self.scale), bold=True)
        self.font_daynote = pygame.font.SysFont('Times New Roman', int(14*self.scale))
        self.font_daynote = pygame.font.SysFont('Times New Roman', int(14 * self.scale))
        self.font_qoute = pygame.font.SysFont('Times New Roman', int(14*self.scale))
        self.font_author = pygame.font.SysFont('Times New Roman', int(14*self.scale))
        self.font_label = pygame.font.SysFont('Arial', int(11*self.scale))
        self.font_time = pygame.font.SysFont('Arial', int(18*self.scale), bold=True)
        self.font_lunarday = pygame.font.SysFont('Arial', int(42*self.scale), bold=True)
        self.font_weather = pygame.font.SysFont('Arial', int(10*self.scale), bold=True)
        
        self.top = int(10 * self.scale)
        self.center = self.content_h // 2
        self.quote, self.author = self.load_quote()

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
    def load_quote(self):
        if not os.path.exists("quotes.txt"):
            return "", ""
        with open("quotes.txt", encoding="utf-8") as f:
            lines = [l.strip() for l in f if "\t" in l]
        if not lines:
            return "", ""
        text, author = random.choice(lines).split("\t", 1)
        return text, f"— {author}"
    def update_wallpaper(self):
        bg = self.load_random_image(
            WALLPAPER_DIR,
            (self.W, self.H),
            alpha=False
        )
        if bg:
            self.background = bg    
    def update_info(self):
        now = datetime.now()
        g_month= f"Tháng {now.month} - {now.year}"
        g_day= str(now.day)
        weekday = now.weekday()
        is_sunday = weekday == 6
        is_weekend = weekday >= 5
        g_weekday= WEEKDAYS[weekday]
        

        # Main panel --------------------------------------------------------------
        main_panel_x, main_panel_y = 0, self.top        
        panel_main_texts = [g_month, g_day, g_weekday]
        main_panel_text_colors = [
            COLOR_MONTH,
            COLOR_DAY_SUNDAY if is_sunday else COLOR_DAY_NORMAL,
            COLOR_WEEKDAY_WEEKEND if is_weekend else COLOR_WEEKDAY_NORMAL
        ]        
        main_panel_text_fonts = [self.font_month, self.font_day, self.font_weekday]
        main_panel_text_gaps = [
            (0, 200*self.scale),  # Khoảng cách từ tháng đến ngày
            (0, -20*self.scale),  # Khoảng cách từ ngày đến thứ
            (0, 20*self.scale),  # Khoảng cách từ thứ đến ghi chú ngày
        ]
        main_panel_text_alignments = ['center', 'center', 'center']

        main_panel_text_outlines = [{"color": (255,255,255), "thickness": 1}, {"color": (255,255,255), "thickness": 1}, {"color": (255,255,255), "thickness": 1}]
        main_panel_text_effects = [False, {"name": "gradient", 'top_color': (100, 180, 255), 'bottom_color': (28, 70, 176),'offset': 0}, False]
        main_panel_rect = self.pyfunc.create_panel(
            screen= self.screen, pygame=pygame,            
            x=main_panel_x, y=main_panel_y,
            panel_color=COLOR_MAIN_PANEL,
            panel_border_color=COLOR_MAIN_PANEL_BORDER,
            panel_transparent=True,
            draw_panel=False,
            draw_border=False,
            border_width=1,
            padding=5,
            max_width=self.W,
            max_height=None,
            auto_expand_height=True,
            auto_shrink_witdh=False,
            texts=panel_main_texts,
            text_colors=main_panel_text_colors,
            text_fonts=main_panel_text_fonts,
            gap=0,  # Giá trị mặc định, chỉ dùng khi gaps_list=None
            gaps_list= main_panel_text_gaps,  # Truyền gaps_list tùy chỉnh
            text_alignments=main_panel_text_alignments,  
            text_outlines=main_panel_text_outlines,
            text_effects=main_panel_text_effects
        )


        # Daynote panel --------------------------------------------------------------
        daynote_panel_x, daynot_panel_y = 0, self.top+main_panel_rect[3]        
        daynote_panel_texts = ["Ghi chú ngày"]
        daynote_panel_text_colors = [COLOR_DAYNOTE]        
        daynote_panel_text_fonts = [self.font_daynote]
        daynote_panel_text_gaps = [0]
        daynote_panel_text_alignments = ['center']

        daynote_panel_text_outlines = [{"color": (255,255,255), "thickness": 1}]
        daynote_panel_text_effects = [False]
        daynote_panel_rect = self.pyfunc.create_panel(
            screen= self.screen, pygame=pygame,            
            x=daynote_panel_x, y=daynot_panel_y,
            panel_color=(255,255,255),
            panel_border_color=(0,0,0),
            panel_transparent=True,
            draw_panel=False,
            draw_border=False,
            border_width=1,
            padding=2,
            max_width=self.W,
            max_height=None,
            auto_expand_height=True,
            auto_shrink_witdh=False,
            texts=daynote_panel_texts,
            text_colors=daynote_panel_text_colors,
            text_fonts=daynote_panel_text_fonts,
            gap=0,  # Giá trị mặc định, chỉ dùng khi gaps_list=None
            gaps_list= daynote_panel_text_gaps,  # Truyền gaps_list tùy chỉnh
            text_alignments=daynote_panel_text_alignments,  
            text_outlines=daynote_panel_text_outlines,
            text_effects=daynote_panel_text_effects
        )

        # Test quote panel --------------------------------------------------------------
        quote_panel_x, quote_panel_y = self.W//2, self.top+main_panel_rect[3] + daynote_panel_rect[3]  
        quote_panel_texts = [self.quote, self.author]
        quote_panel_text_colors = [COLOR_QUOTE, COLOR_AUTHOR]        
        quote_panel_text_fonts = [self.font_qoute, self.font_author]
        quote_panel_text_gaps = [0,0]
        quote_panel_text_alignments = ['center','center']
        quote_panel_text_outlines = [False, False]
        quote_panel_text_effects = [False, False]
        quote_panel_rect = self.pyfunc.create_panel(
            screen= self.screen, pygame=pygame,            
            x=quote_panel_x, y=quote_panel_y,
            panel_color=(255,255,255),
            panel_border_color=(0,0,0),
            panel_transparent=True,
            draw_panel=True,
            draw_border=False,
            border_width=1,
            padding=0,
            max_width=self.W-4*self.scale,
            max_height=None,
            auto_expand_height=True,
            auto_shrink_witdh=True,
            texts=quote_panel_texts,
            text_colors=quote_panel_text_colors,
            text_fonts=quote_panel_text_fonts,
            gap=0,  # Giá trị mặc định, chỉ dùng khi gaps_list=None
            gaps_list= quote_panel_text_gaps,  # Truyền gaps_list tùy chỉnh
            text_alignments=quote_panel_text_alignments,  
            text_outlines=quote_panel_text_outlines,
            text_effects=quote_panel_text_effects,
            test = True
         )
        # Quote panel --------------------------------------------------------------
        quote_panel_x, quote_panel_y = self.W//2 - quote_panel_rect[2]//2, self.top+main_panel_rect[3] + daynote_panel_rect[3]  
        quote_panel_rect = self.pyfunc.create_panel(
            screen= self.screen, pygame=pygame,            
            x=quote_panel_x, y=quote_panel_y,
            panel_color=(255,255,255),
            panel_border_color=(0,0,0),
            panel_transparent=True,
            draw_panel=True,
            draw_border=False,
            border_width=1,
            padding=0,
            max_width=self.W-4*self.scale,
            max_height=None,
            auto_expand_height=True,
            auto_shrink_witdh=True,
            texts=quote_panel_texts,
            text_colors=quote_panel_text_colors,
            text_fonts=quote_panel_text_fonts,
            gap=0,  # Giá trị mặc định, chỉ dùng khi gaps_list=None
            gaps_list= quote_panel_text_gaps,  # Truyền gaps_list tùy chỉnh
            text_alignments=quote_panel_text_alignments,  
            text_outlines=quote_panel_text_outlines,
            text_effects=quote_panel_text_effects
        )        
        
    def run(self):
        # Game loop
        clock = pygame.time.Clock()
        running = True

        self.update_wallpaper()
        self.update_info()
        # ---- Thời gian ban đầu ----
        now = datetime.now()
        last_minute = (now.hour, now.minute)
        last_wallpaper_time = time.time()

        while running:
            # ===== EVENT =====
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  # chuột phải
                        running = False

            # ===== CHECK TIME =====
            now = datetime.now()
            self.need_redraw = True
            
            # 1️⃣ Mỗi khi đổi phút
            current_minute = (now.hour, now.minute)
            if current_minute != last_minute:
                last_minute = current_minute
                self.need_redraw = True
                self.quote, self.author = self.load_quote()                

            # 2️⃣ Mỗi 30 phút
            current_time = time.time()
            if current_time - last_wallpaper_time >= 30 * 60:
                last_wallpaper_time = current_time
                self.update_wallpaper()
                self.need_redraw = True
                
            # ===== DRAW =====
            if self.need_redraw:
                self.screen.blit(self.background, (0,0))
                self.update_info()
                pygame.display.flip()
                self.need_redraw = False
            clock.tick(30)

        pygame.quit()
        sys.exit()     
if __name__ == "__main__":
        # Game loop
        app=LunarPygame()
        app.run()