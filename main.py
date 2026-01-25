import tkinter as tk
from PIL import Image, ImageTk
import datetime
import random
import os

from lunar_hnd import LunarDate

# ================== SIZE ==================
WIDTH = 500
HEIGHT = 700
FOOTER_HEIGHT = 120

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

# ================== FONTS ==================
FONT_MONTH = ("Arial", 15, "bold")
FONT_DAY = ("Times New Roman", 140, "bold")
FONT_WEEKDAY = ("Times New Roman", 26, "bold")
FONT_QUOTE = ("Arial", 11, "italic")
FONT_AUTHOR = ("Arial", 10, "bold")
FONT_LABEL = ("Arial", 11, "bold")
FONT_NORMAL = ("Arial", 11)
FONT_TIME_BIG = ("Arial", 18, "bold")
FONT_LUNAR_DAY = ("Arial", 42, "bold")

WEEKDAYS = ["Thứ Hai","Thứ Ba","Thứ Tư","Thứ Năm","Thứ Sáu","Thứ Bảy","Chủ Nhật"]

# ================== APP ==================
class LunarCalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lịch Âm Dương")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

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
        self.canvas.create_text(
            WIDTH//2, 20,
            text=f"Tháng {now.month} - {now.year}",
            fill=COLOR_MONTH, font=FONT_MONTH, tags="text"
        )

        self.draw_shadow_text(
            WIDTH // 2, HEIGHT // 2 - 160,
            text=str(now.day),
            font=FONT_DAY,
            main_color=day_color, shadow_color="#777777", offset=2
        )

        #self.canvas.create_text(
        #    WIDTH//2, HEIGHT//2 - 40,
        #    text=WEEKDAYS[weekday],
        #    fill=weekday_color, font=FONT_WEEKDAY, tags="text"
        #)
        self.draw_shadow_text(
            WIDTH // 2, HEIGHT // 2 - 60,
            text=WEEKDAYS[weekday],
            font=FONT_WEEKDAY,
            main_color=weekday_color, shadow_color="#777777", offset=1
        )

        quote, author = self.load_quote()
        self.canvas.create_text(
            WIDTH//2, HEIGHT//2 -20,
            text=quote,
            fill=COLOR_QUOTE,
            font=FONT_QUOTE,
            width=420,
            justify="center",
            tags="text"
        )

        self.canvas.create_text(
            WIDTH//2, HEIGHT//2 ,
            text=author,
            fill=COLOR_AUTHOR,
            font=FONT_AUTHOR,
            tags="text"
        )

        # ===== FOOTER =====
        footer_top = HEIGHT - FOOTER_HEIGHT
        col_w = WIDTH // 3

        self.canvas.create_rectangle(
            0, footer_top, WIDTH, HEIGHT,
            fill=COLOR_FOOTER_BG, outline="", tags="text"
        )

        self.canvas.create_line(col_w, footer_top, col_w, HEIGHT,
            fill=COLOR_SEPARATOR, width=1, tags="text")
        self.canvas.create_line(col_w * 2, footer_top, col_w * 2, HEIGHT,
            fill=COLOR_SEPARATOR, width=1, tags="text")

        x_left = col_w // 2
        x_mid = col_w + col_w // 2
        x_right = col_w * 2 + col_w // 2

        y0 = footer_top + 15
        lh = 22

        # ===== LEFT: GIỜ =====
        self.canvas.create_text(x_left, y0,
            text="GIỜ", fill=COLOR_LABEL, font=FONT_LABEL, tags="text")

        self.canvas.create_text(x_left, y0 + lh,
            text=f"Giờ {hour_cc}",
            fill=COLOR_LUNAR, font=FONT_NORMAL, tags="text")

        self.canvas.create_text(x_left, y0 + lh * 2,
            text=now.strftime("%H:%M"),
            fill=COLOR_TIME, font=FONT_TIME_BIG, tags="text")
        hoang_dao_hours = ld.getHoangDaoHours()
        hd_line1 = ", ".join(hoang_dao_hours[:3])
        hd_line2 = ", ".join(hoang_dao_hours[3:])
        self.canvas.create_text(x_left, y0 + lh * 3,
            text=hd_line1,
            fill=COLOR_LUNAR, font=FONT_NORMAL, tags="text")

        self.canvas.create_text(x_left, y0 + lh * 4,
            text=hd_line2,
            fill=COLOR_LUNAR, font=FONT_NORMAL, tags="text")

        # ===== MIDDLE: NGÀY ÂM =====
        self.canvas.create_text(x_mid, y0+15,
            text=f"{ld.lunarDay:02d}",
            fill=day_color,
            font=FONT_LUNAR_DAY,
            tags="text")

        self.canvas.create_line(
            x_mid - 35, y0 + lh * 1.2+15,
            x_mid + 35, y0 + lh * 1.2+15,
            fill=day_color, width=2, tags="text"
        )

        self.canvas.create_text(x_mid, y0 + lh * 2+15,
            text=f"THÁNG {ld.lunarMonth}",
            fill=COLOR_LUNAR, font=FONT_LABEL, tags="text")
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
        self.canvas.create_text(x_mid, y0 + lh * 3+15,
            text=day_text,
            fill=day_color, font=FONT_NORMAL, tags="text")

        # ===== RIGHT: ÂM LỊCH =====
        self.canvas.create_text(x_right, y0,
            text="ÂM LỊCH", fill=COLOR_LABEL, font=FONT_LABEL, tags="text")

        self.canvas.create_text(x_right, y0 + lh*1.5,
            text=f"Năm {year_cc}",
            fill=COLOR_LUNAR, font=FONT_NORMAL, tags="text")

        self.canvas.create_text(x_right, y0 + lh * 2.5,
            text=f"Tháng {month_cc}",
            fill=COLOR_LUNAR, font=FONT_NORMAL, tags="text")

        self.canvas.create_text(x_right, y0 + lh * 3.5,
            text=f"Ngày {day_cc}",
            fill=COLOR_LUNAR, font=FONT_NORMAL, tags="text")

        self.root.after(90000, self.update_all)

    def update_wallpaper(self):
        if not self.wallpapers:
            return
        img = Image.open(random.choice(self.wallpapers)).resize(
            (WIDTH, HEIGHT-FOOTER_HEIGHT), Image.LANCZOS
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
