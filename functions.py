import requests
import pygame
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
class Pygame_Functions:
    def __init__(self):
        pass
    def create_panel(self, screen, pygame, x, y, panel_color, panel_border_color, panel_transparent, 
                     texts, text_colors, text_fonts, gap=5, auto_expand_height=True, 
                     border_width=2, padding=10, max_width=None, max_height=None):
        """
        Vẽ panel với text tự động xuống dòng và điều chỉnh chiều cao
        
        Parameters:
        -----------
        pygame : module
            Module pygame
        x, y : int
            Tọa độ panel
        panel_color : tuple
            Màu nền panel (R, G, B) hoặc (R, G, B, A)
        panel_border_color : tuple
            Màu viền panel
        panel_transparent : bool
            True nếu panel trong suốt
        texts : list
            Danh sách các chuỗi text
        text_colors : list
            Danh sách màu sắc cho từng text
        text_fonts : list
            Danh sách font cho từng text
        gap : int
            Khoảng cách giữa các dòng text
        auto_expand_height : bool
            True nếu tự động tăng chiều cao khi text vượt quá
        border_width : int
            Độ dày viền
        padding : int
            Khoảng cách từ viền đến text
        max_width : int
            Bề rộng tối đa của panel (None = tự động tính)
        max_height : int
            Chiều cao tối đa (None = không giới hạn)
        """
        
        # Khởi tạo nếu cần
        #if not hasattr(self, 'screen'):
        #    self.screen = pygame.display.get_surface()

        self.screen=screen
        # Tính toán chiều rộng panel
        if max_width is None:
            # Tìm chiều rộng lớn nhất của các text
            max_text_width = 0
            for i, text in enumerate(texts):
                text_surface = text_fonts[i].render(text, True, text_colors[i])
                max_text_width = max(max_text_width, text_surface.get_width())
            panel_width = max_text_width + 2 * padding + 2 * border_width
        else:
            panel_width = max_width
        
        # Tính toán chiều cao ban đầu
        panel_height = 100  # Chiều cao mặc định
        if max_height:
            panel_height = min(panel_height, max_height)
        
        # Tạo surface cho panel
        if panel_transparent:
            panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        else:
            panel_surface = pygame.Surface((panel_width, panel_height))
            panel_surface.fill(panel_color)
        
        # Vẽ viền
        pygame.draw.rect(panel_surface, panel_border_color, 
                        (0, 0, panel_width, panel_height), border_width)
        
        # Tính toán vùng vẽ text
        text_area_width = panel_width - 2 * padding - 2 * border_width
        text_area_height = panel_height - 2 * padding - 2 * border_width
        
        # Biến lưu vị trí y hiện tại khi vẽ text
        current_y = padding + border_width
        max_used_height = 0
        
        # Xử lý từng text
        for i, text in enumerate(texts):
            font = text_fonts[i]
            color = text_colors[i]
            
            # Tách text thành các từ
            words = text.split(' ')
            current_line = ''
            line_height = 0
            
            for word in words:
                # Thử thêm từ vào dòng hiện tại
                test_line = current_line + word + ' '
                test_surface = font.render(test_line, True, color)
                
                # Nếu vượt quá chiều rộng cho phép
                if test_surface.get_width() > text_area_width:
                    # Vẽ dòng hiện tại nếu có
                    if current_line:
                        line_surface = font.render(current_line, True, color)
                        panel_surface.blit(line_surface, 
                                          (padding + border_width, current_y))
                        current_y += line_surface.get_height() + gap
                        max_used_height = current_y - (padding + border_width)
                    
                    # Bắt đầu dòng mới với từ hiện tại
                    current_line = word + ' '
                    line_height = font.size(word)[1]
                else:
                    current_line = test_line
                    line_height = font.size(test_line)[1]
            
            # Vẽ dòng cuối cùng nếu có
            if current_line:
                line_surface = font.render(current_line, True, color)
                panel_surface.blit(line_surface, 
                                  (padding + border_width, current_y))
                current_y += line_surface.get_height() + gap
                max_used_height = current_y - (padding + border_width)
            
            # Thêm khoảng cách giữa các đoạn text
            if i < len(texts) - 1:
                current_y += gap
        
        # Tính chiều cao thực tế cần thiết
        required_height = max_used_height + 2 * padding + 2 * border_width + gap
        
        # Xử lý điều chỉnh chiều cao
        if auto_expand_height and required_height > panel_height:
            if max_height and required_height > max_height:
                panel_height = max_height  # Giới hạn chiều cao tối đa
            else:
                panel_height = required_height  # Tăng chiều cao
            
            # Tạo lại panel với chiều cao mới
            if panel_transparent:
                new_panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            else:
                new_panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
                new_panel.fill(panel_color)
            
            # Vẽ viền
            pygame.draw.rect(new_panel, panel_border_color, 
                           (0, 0, panel_width, panel_height), border_width)
            
            # Vẽ lại toàn bộ text
            current_y = padding + border_width
            for i, text in enumerate(texts):
                font = text_fonts[i]
                color = text_colors[i]
                
                words = text.split(' ')
                current_line = ''
                
                for word in words:
                    test_line = current_line + word + ' '
                    test_surface = font.render(test_line, True, color)
                    
                    if test_surface.get_width() > text_area_width:
                        if current_line:
                            line_surface = font.render(current_line, True, color)
                            new_panel.blit(line_surface, 
                                         (padding + border_width, current_y))
                            current_y += line_surface.get_height() + gap
                        
                        current_line = word + ' '
                    else:
                        current_line = test_line
                
                if current_line:
                    line_surface = font.render(current_line, True, color)
                    new_panel.blit(line_surface, 
                                 (padding + border_width, current_y))
                    current_y += line_surface.get_height() + gap
                
                if i < len(texts) - 1:
                    current_y += gap
            
            panel_surface = new_panel
        
        # Vẽ panel lên màn hình
        self.screen.blit(panel_surface, (x, y))
        
        # Trả về kích thước thực tế của panel
        return pygame.Rect(x, y, panel_width, panel_height)

    # Hàm helper để tạo panel nhanh với các tham số mặc định
    @staticmethod
    def create_simple_panel(pygame, x, y, width, texts, bg_color=(200, 200, 200), 
                           border_color=(50, 50, 50), font=None, text_color=(0, 0, 0)):
        """
        Tạo panel đơn giản với các tham số mặc định
        """
        if font is None:
            font = pygame.font.SysFont(None, 24)
        
        renderer = Pygame_Functions()
        return renderer.create_panel(
            pygame=pygame,
            x=x,
            y=y,
            panel_color=bg_color,
            panel_border_color=border_color,
            panel_transparent=False,
            texts=texts,
            text_colors=[text_color] * len(texts),
            text_fonts=[font] * len(texts),
            max_width=width
        )