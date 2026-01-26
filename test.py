import tkinter as tk
from PIL import Image, ImageTk
import datetime
import random
import os

PORTRAIT_RATIO = 16 / 9
BASE_WIDTH = 500
BASE_HEIGHT = 888
FOOTER_RATIO = 0.18
WALLPAPER_DIR = "wallpaper"
FONT = "Arial"

class KioskCalendar:
    def __init__(self, root):
        self.root = root
        root.overrideredirect(True)
        root.attributes("-topmost", True)

        SW, SH = root.winfo_screenwidth(), root.winfo_screenheight()

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

        # Wallpapers
        self.wallpapers = []
        if os.path.isdir(WALLPAPER_DIR):
            self.wallpapers = [
                os.path.join(WALLPAPER_DIR, f)
                for f in os.listdir(WALLPAPER_DIR)
                if f.lower().endswith(".jpg")
            ]

        self.bg_img = None

        self.draw_footer()
        self.update_wallpaper()
        self.update_ui()

    # ---------------------------

    def draw_footer(self):
        self.canvas.create_rectangle(
            0, self.content_h, self.W, self.H,
            fill="#d8efb5", outline="", tags="ui"
        )
        w = self.W // 3
        for i in range(1, 3):
            self.canvas.create_line(
                i * w, self.content_h, i * w, self.H,
                width=2, tags="ui"
            )

    # ---------------------------

    def update_wallpaper(self):
        if not self.wallpapers:
            return

        img = Image.open(random.choice(self.wallpapers))
        img = img.resize((self.W, self.content_h), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(img)

        self.canvas.delete("bg")
        self.canvas.create_image(
            0, 0, anchor="nw", image=self.bg_img, tags="bg"
        )

        self.root.after(900000, self.update_wallpaper)

    # ---------------------------

    def update_ui(self):
        self.canvas.delete("ui")

        now = datetime.datetime.now()

        top = int(50 * self.scale)
        center = self.content_h // 2

        # Header
        self.canvas.create_text(
            self.W//2, top,
            text=f"Tháng {now.month} - {now.year}",
            fill="#2ecc71",
            font=(FONT, int(24*self.scale), "bold"),
            tags="ui"
        )

        # Day number
        self.canvas.create_text(
            self.W//2, center - int(40*self.scale),
            text=str(now.day),
            fill="#1f77b4",
            font=(FONT, int(130*self.scale), "bold"),
            tags="ui"
        )

        thu = ["Hai","Ba","Tư","Năm","Sáu","Bảy","Chủ Nhật"][now.weekday()]
        self.canvas.create_text(
            self.W//2, center + int(60*self.scale),
            text=f"Thứ {thu}",
            fill="#1f77b4",
            font=(FONT, int(30*self.scale), "bold"),
            tags="ui"
        )

        # Quote
        self.canvas.create_text(
            self.W//2, center + int(130*self.scale),
            text="Hôm nay là một trang mới trong cuộc đời bạn.",
            width=int(self.W*0.8),
            justify="center",
            fill="#1f77b4",
            font=(FONT, int(18*self.scale)),
            tags="ui"
        )

        self.canvas.create_text(
            self.W//2, center + int(170*self.scale),
            text="- Khuyết danh",
            fill="#f39c12",
            font=(FONT, int(14*self.scale), "italic"),
            tags="ui"
        )

        # Footer text
        w = self.W // 3
        y = self.content_h + int(35*self.scale)

        self.canvas.create_text(w//2, y, text="GIỜ",
            fill="#888", font=(FONT, int(14*self.scale), "bold"), tags="ui")
        self.canvas.create_text(w//2, y+30,
            text=now.strftime("%H:%M"),
            fill="#1f77b4", font=(FONT, int(22*self.scale), "bold"), tags="ui")

        self.canvas.create_text(w+w//2, y+10,
            text=str(now.day),
            fill="#1f77b4", font=(FONT, int(50*self.scale), "bold"), tags="ui")
        self.canvas.create_text(w+w//2, y+55,
            text=f"THÁNG {now.month}",
            fill="black", font=(FONT, int(16*self.scale), "bold"), tags="ui")

        self.canvas.create_text(w*2+w//2, y,
            text="ÂM LỊCH",
            fill="#888", font=(FONT, int(14*self.scale), "bold"), tags="ui")
        self.canvas.create_text(w*2+w//2, y+30,
            text="Ất Tỵ",
            fill="black", font=(FONT, int(16*self.scale)), tags="ui")

        self.root.after(60000, self.update_ui)

# =============================

if __name__ == "__main__":
    root = tk.Tk()
    KioskCalendar(root)
    root.mainloop()
