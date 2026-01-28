import requests
import tkinter as tk

class FreeWeather:
    def __init__(self):
      self.district,  self.weather, self.temp, self.humidity = self.get_current_weather_free()
      
    def get_current_weather_free(self):
        try:
            # --- kiểm tra mạng THỰC SỰ ---
            requests.get("https://1.1.1.1", timeout=2)

        except Exception:
        # ❌ không có Internet
            return ("Offline", "Không có Internet", None, None)
        try:
            # 1. Lấy vị trí theo IP
            loc = requests.get("http://ip-api.com/json").json()
            lat = loc["lat"]
            lon = loc["lon"]
            location = loc.get("district", loc.get("city", "Không rõ"))

            # 2. Gọi Open-Meteo (free, không cần key)
            url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitude={lat}&longitude={lon}"
                "&current=temperature_2m,relative_humidity_2m,weather_code"
            )
            data = requests.get(url).json()["current"]

            temperature = round(data["temperature_2m"])
            humidity = int(data["relative_humidity_2m"])
            code = data["weather_code"]

            # 3. Map mã thời tiết → tiếng Việt
            weather_map = {
                0: "Trời quang",
                1: "Ít mây",
                2: "Mây rải rác",
                3: "Nhiều mây",
                45: "Sương mù",
                48: "Sương mù dày",
                51: "Mưa phùn nhẹ",
                61: "Mưa nhẹ",
                63: "Mưa vừa",
                65: "Mưa to",
                80: "Mưa rào nhẹ",
                95: "Dông"
            }

            weather = weather_map.get(code, "Không xác định")

            # 4. Trả về tuple
            return location, weather, temperature, humidity
        except Exception:
            # 👉 fallback khi mất mạng
            return ("Offline", "Không có Internet", None, None)
class CustomText:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
    def draw_shadow_text(
        self,
        x, y,
        text,
        font,
        main_color,
        outline_width=2,
        bevel_offset=1,
        outline_color="white",
        shadow_color="#666666",
        highlight_color="#eeeeee",
        tag="text"):
        # ===== 1. Viền trắng (outline) =====
        for dx in (-outline_width, 0, outline_width):
            for dy in (-outline_width, 0, outline_width):
                if dx != 0 or dy != 0:
                    self.canvas.create_text(
                        x + dx, y + dy,
                        text=text,
                        fill=outline_color,
                        font=font,
                        tags=tag
                )

        # ===== 2. Highlight (bevel sáng trên trái) =====
        self.canvas.create_text(
            x - bevel_offset,
            y - bevel_offset,
            text=text,
            fill=highlight_color,
            font=font,
            tags=tag
        )

        # ===== 3. Shadow (bevel tối dưới phải) =====
        self.canvas.create_text(
            x + bevel_offset,
            y + bevel_offset,
            text=text,
            fill=shadow_color,
            font=font,
            tags=tag
        )

        # ===== 4. Text chính =====
        self.canvas.create_text(
            x, y,
            text=text,
            fill=main_color,
            font=font,
            tags=tag
        )
    def draw_text_with_ouline(
        self,
        x, y,
        text,
        font,
        main_color,
        outline_width=1,
        outline_color="white",
        tag="text"):
        # ===== 1. Viền trắng (outline) =====
        for dx in (-outline_width, 0, outline_width):
            for dy in (-outline_width, 0, outline_width):
                if dx != 0 or dy != 0:
                    self.canvas.create_text(
                        x + dx, y + dy,
                        text=text,
                        fill=outline_color,
                        font=font,
                        tags=tag
                )

         # ===== 2. Text chính =====
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