import tkinter as tk
from PIL import Image, ImageTk
import datetime
import random
import os

from numpy import spacing

from lunar_hnd import LunarDate

# ================== SIZE ==================
PORTRAIT_RATIO = 16 / 9
BASE_WIDTH = 500
BASE_HEIGHT = 888
FOOTER_RATIO = 0.12
WALLPAPER_DIR = "wallpaper"


# ================== COLORS ==================
COLOR_MONTH = "#000000"
COLOR_DAY_NORMAL = "#1c46b0"
COLOR_DAY_SUNDAY = "#e74c3c"
COLOR_WEEKDAY_NORMAL = "#1c46b0"
COLOR_WEEKDAY_WEEKEND = "#e74c3c"
COLOR_QUOTE = "#1c46b0"
COLOR_AUTHOR = "#f39c12"
COLOR_LABEL = "#7f8c8d"
COLOR_TIME = "#1c46b0"
COLOR_LUNAR = "#000000"
COLOR_FOOTER_BG = "#cfe6a8"
COLOR_SEPARATOR = "#000000"
COLOR_HOANG_DAO = "#d35400"
COLOR_HAC_DAO = "#7f8c8d"
COLOR_SHADOW = "#777777"

# ================== EFFECTS ==================
OFFSET_SHADOW = 2

# ================== FONTS ==================
FONT_MONTH = ("Arial", 15, "bold")
FONT_LUNAR_MONTH = ("Arial", 13, "bold")
FONT_DAY = ("Times New Roman", 140, "bold")
FONT_WEEKDAY = ("Times New Roman", 26, "bold")
FONT_QUOTE = ("Arial", 11, "italic")
FONT_AUTHOR = ("Arial", 10, "bold")
FONT_LABEL = ("Arial", 11, "bold")
FONT_NORMAL = ("Arial", 11, "")
FONT_TIME_BIG = ("Arial", 18, "bold")
FONT_LUNAR_DAY = ("Arial", 42, "bold")

# ================== SPACING ==================
FOOTER_LABEL_SPACING = 1.5


WEEKDAYS = ["Thứ Hai","Thứ Ba","Thứ Tư","Thứ Năm","Thứ Sáu","Thứ Bảy","Chủ Nhật"]

# ================== APP ==================
class LunarCalendarApp:
    def __init__(self, root):
        self.root = root
        root.overrideredirect(True)
        root.attributes("-topmost", True)

        SW, SH = root.winfo_screenwidth(), root.winfo_screenheight()
        #SW, SH = 500, 888

        if SW >= SH:
            self.H = SH
            self.W = int(self.H / PORTRAIT_RATIO)
            self.X = (SW - self.W) // 2
            self.Y = 0
        else:
            self.W, self.H = SW, SH
            self.X = self.Y = 0

        root.geometry(f"{self.W}x{self.H}+{self.X}+{self.Y}")

        self.scale = min(self.W / BASE_WIDTH, self.H / BASE_HEIGHT)
        self.footer_h = int(self.H * FOOTER_RATIO)
        self.content_h = self.H - self.footer_h

        self.canvas = tk.Canvas(root, width=self.W, height=self.H, highlightthickness=0)
        self.canvas.pack()

        # Exit
        root.bind("<Escape>", lambda e: root.destroy())
        root.bind("<Control-q>", lambda e: root.destroy())
        self.canvas.bind("<Button-3>", lambda e: root.destroy())

        self.wallpapers = []
        self.bg_image = None

        self.load_wallpapers()
        self.update_all()
        self.update_wallpaper()

    def draw_shadow_text(self, x, y, text, font,
                         main_color,
                         shadow_color="#888888",
                         offset=2,
                         tag="text"):

        # shadow (dưới phải)
        self.canvas.create_text(
            x + offset, y + offset,
            text=text,
            fill=shadow_color,
            font=font,
            tags=tag
        )

        # text chính
        self.canvas.create_text(
            x, y,
            text=text,
            fill=main_color,
            font=font,
            tags=tag
        )
        
    def scale_font(self,font, factor):
        name, size, style = font
        return (name, int(size * factor), style)

    def load_wallpapers(self):
        if not os.path.exists("wallpaper"):
            return
        self.wallpapers = [
            os.path.join("wallpaper", f)
            for f in os.listdir("wallpaper")
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

    def load_quote(self):
        if not os.path.exists("quotes.txt"):
            return "", ""
        with open("quotes.txt", encoding="utf-8") as f:
            lines = [l.strip() for l in f if "\t" in l]
        if not lines:
            return "", ""
        text, author = random.choice(lines).split("\t", 1)
        return text, f"— {author}"

    def update_all(self):
        self.canvas.delete("text")

        now = datetime.datetime.now()
        #now = datetime.datetime(2026, 1, 27, 22, 59)
        ld = LunarDate(now.day, now.month, now.year)

        # ===== CAN CHI =====
        year_cc = " ".join(ld.getCanChiYear(ld.lunarYear))
        month_cc = " ".join(ld.getCanChiMonth(ld.lunarYear, ld.lunarMonth))
        day_cc = " ".join(ld.getCanChiDay(ld.jd))
        hour_cc = LunarDate.get_lunar_hour_info(ld.jd, now.hour)['name']

        weekday = now.weekday()
        is_sunday = weekday == 6
        is_weekend = weekday >= 5

        day_color = COLOR_DAY_SUNDAY if is_sunday else COLOR_DAY_NORMAL
        weekday_color = COLOR_WEEKDAY_WEEKEND if is_weekend else COLOR_WEEKDAY_NORMAL

        # ===== TOP =====
        top = int(30 * self.scale)
        center = self.content_h // 2
        self.canvas.create_text(
            self.W//2, top,
            text=f"Tháng {now.month} - {now.year}",
            fill=COLOR_MONTH,
            font=self.scale_font(FONT_MONTH,self.scale),
            tags="text"
        )
        # ===== Day number =====
        self.draw_shadow_text(
            self.W//2, center - int(40*self.scale),
            text=str(now.day),
            font=self.scale_font(FONT_DAY,self.scale),
            main_color=day_color, shadow_color=COLOR_SHADOW, offset=OFFSET_SHADOW
        )

        # ===== Week day =====
        self.draw_shadow_text(
            self.W//2, center + int(60*self.scale),
            text=WEEKDAYS[weekday],
            font=self.scale_font(FONT_WEEKDAY,self.scale),
            main_color=weekday_color, shadow_color=COLOR_SHADOW, offset=OFFSET_SHADOW
        )

        # ===== Quote & Author =====
        quote, author = self.load_quote()
        quote_text_id=self.canvas.create_text(
            self.W//2, center + int(130*self.scale),
            text=quote,
            fill=COLOR_QUOTE,
            font=self.scale_font(FONT_QUOTE,self.scale),
            width=int(self.W*0.8),
            #spacing2 = int(FONT_QUOTE[1]*self.scale*0.3),
            #spacing3 = int(FONT_QUOTE[1]*self.scale*0.3),
            justify="center",
            tags="text"
        )
        bbox=self.canvas.bbox(quote_text_id)
        quote_height=bbox[3] - bbox[1]
        self.canvas.create_text(
            self.W//2, center + int(130*self.scale)+quote_height,
            text=author,
            fill=COLOR_AUTHOR,
            font=self.scale_font(FONT_AUTHOR,self.scale),
            tags="text"
        )

        # ===== FOOTER =====

        self.canvas.create_rectangle(
            0, self.content_h, self.W, self.H,
            fill=COLOR_FOOTER_BG, outline="", tags="text"
        )
        col_w = self.W // 3
        self.canvas.create_line(col_w, self.content_h, col_w, self.H,
            fill=COLOR_SEPARATOR, width=1, tags="text")
        self.canvas.create_line(col_w * 2,  self.content_h, col_w * 2, self.H,
            fill=COLOR_SEPARATOR, width=1, tags="text")

        x_left = col_w // 2
        x_mid = col_w + col_w // 2
        x_right = col_w * 2 + col_w // 2

        y0 = self.content_h
        sp = 10

        # ===== LEFT: GIỜ =====
        yl1=y0+int(sp*self.scale)
        self.canvas.create_text(x_left, yl1,
            text="GIỜ",
            fill=COLOR_LABEL,
            font=self.scale_font(FONT_LABEL,self.scale),
            tags="text")

        yl2= yl1+int((sp+FONT_LABEL[1])*self.scale)
        self.canvas.create_text(x_left, yl2,
            text=f"Giờ {hour_cc}",
            fill=COLOR_LUNAR,
            font=self.scale_font(FONT_NORMAL,self.scale),
            tags="text")

        yl3=yl2+int((sp+FONT_NORMAL[1])*self.scale)
        self.canvas.create_text(x_left, yl3,
            text=now.strftime("%H:%M"),
            fill=COLOR_TIME,
            font=self.scale_font(FONT_TIME_BIG,self.scale),
            tags="text")
        
        hoang_dao_hours = ld.getHoangDaoHours()
        hd_line1 = ", ".join(hoang_dao_hours[:3])
        hd_line2 = ", ".join(hoang_dao_hours[3:])
        yl4=yl3+int((sp+FONT_TIME_BIG[1])*self.scale)
        self.canvas.create_text(x_left, yl4,
            text=hd_line1,
            fill=COLOR_LUNAR,
            font=self.scale_font(FONT_NORMAL,self.scale),
            tags="text")

        yl5=yl4+int((sp+FONT_NORMAL[1])*self.scale)
        self.canvas.create_text(x_left, yl5,
            text=hd_line2,
            fill=COLOR_LUNAR,
            font=self.scale_font(FONT_NORMAL, self.scale), 
            tags="text")

        # ===== MIDDLE: NGÀY ÂM =====
        ym1=y0+int((sp+FONT_LUNAR_DAY[1]/2)*self.scale)
        self.canvas.create_text(x_mid, ym1,
            text=f"{ld.lunarDay:02d}",
            fill=day_color,
            font=self.scale_font(FONT_LUNAR_DAY, self.scale), 
            tags="text")

        ym2=ym1+int((FONT_LUNAR_DAY[1]/2+sp)*self.scale)
        self.canvas.create_line(
            x_mid - 35, ym2,
            x_mid + 35, ym2,
            fill=day_color, width=2, tags="text"
        )

        ym3=ym2+int((sp+FONT_LABEL[1]/2)*self.scale)
        self.canvas.create_text(x_mid, ym3,
            text=f"THÁNG {ld.lunarMonth}",
            fill=COLOR_LUNAR,
            font=self.scale_font(FONT_LUNAR_MONTH, self.scale), 
            tags="text")
        
        day_type = ld.getDayType()
        if day_type == "hoang_dao":
            day_text = "● Ngày Hoàng Đạo"
            day_color = COLOR_HOANG_DAO
        elif day_type == "hac_dao":
            day_text = "● Ngày Hắc Đạo"
            day_color = COLOR_HAC_DAO
        else:
            day_text = ""
            day_color = COLOR_HOANG_DAO
        ym4=ym3+int((FONT_LUNAR_MONTH[1]+sp)*self.scale)    
        self.canvas.create_text(x_mid, ym4,
            text=day_text,
            fill=day_color,
            font=self.scale_font(FONT_NORMAL, self.scale), 
            tags="text")

        # ===== RIGHT: ÂM LỊCH =====
        yr1=y0+int(sp*self.scale)
        self.canvas.create_text(x_right, yr1,
            text="ÂM LỊCH",
            fill=COLOR_LABEL,
            font=self.scale_font(FONT_LABEL,self.scale), 
            tags="text")

        yr2=yr1 +int((FONT_NORMAL[1]+sp*1.2)*self.scale)
        self.canvas.create_text(x_right, yr2,
            text=f"Năm {year_cc}",
            fill=COLOR_LUNAR,
            font=self.scale_font(FONT_NORMAL, self.scale), 
            tags="text")

        yr3=yr2 +int((FONT_NORMAL[1]+sp*1.2)*self.scale)
        self.canvas.create_text(x_right, yr3,
            text=f"Tháng {month_cc}",
            fill=COLOR_LUNAR,
            font=self.scale_font(FONT_NORMAL, self.scale), 
            tags="text")

        yr4=yr3 +int((FONT_NORMAL[1]+sp*1.2)*self.scale)
        self.canvas.create_text(x_right, yr4,
            text=f"Ngày {day_cc}",
            fill=COLOR_LUNAR,
            font=self.scale_font(FONT_NORMAL, self.scale), 
            tags="text")

        self.root.after(90000, self.update_all)

    def update_wallpaper(self):
        if not self.wallpapers:
            return
        img = Image.open(random.choice(self.wallpapers)).resize(
            (self.W, self.content_h), Image.LANCZOS
        )
        self.bg_image = ImageTk.PhotoImage(img)
        self.canvas.delete("bg")
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw", tags="bg")
        self.canvas.tag_lower("bg")
        self.root.after(90000, self.update_wallpaper)

# ================== MAIN ==================
if __name__ == "__main__":
    root = tk.Tk()
    LunarCalendarApp(root)
    root.mainloop()
