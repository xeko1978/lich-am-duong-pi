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
    def _calculate_text_lines(self, text, font, max_width):
        """Tính toán và tách text thành các dòng dựa trên max_width"""
        words = text.split(' ')
        lines = []
        current_line = ''
        
        for word in words:
            test_line = current_line + word + ' '
            test_width, _ = font.size(test_line)
            
            if test_width > max_width:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + ' '
            else:
                current_line = test_line
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
    
    def _create_text_with_effects(self, pygame, font, text, color,
                                  effect = False, outline=False
                                 ):
        """Tạo surface text với hiệu ứng outline và bevel/emboss"""
        text_surface = font.render(text, True, color)
        
        if not outline and not effect:
            return text_surface
        
        if outline or effect:
               extra_space = effect['offset'] + 1 if effect else 1
               extra_space += outline['thickness'] if outline else 0
               
        surface_width = text_surface.get_width() + extra_space * 2
        surface_height = text_surface.get_height() + extra_space * 2
        
        surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
        
        if outline:

            # Render một bản chữ màu trắng dùng làm viền
            outline_base = font.render(text, True, outline['color'])

            # Vẽ viền bằng cách vẽ bản chữ trắng nhiều lần xung quanh tâm
            # Dùng công thức hình tròn để viền trông mượt mà và dày đều
            for dx in range(-extra_space, extra_space):
                for dy in range(-extra_space, extra_space):
                    # Nếu điểm (dx, dy) nằm trong bán kính hình tròn của độ dày viền
                    if dx*dx + dy*dy <= extra_space*extra_space:
                        surface.blit(outline_base, (extra_space + dx, extra_space + dy))
            surface.blit(text_surface, (extra_space, extra_space))
        
        if effect and effect['name']=="gradient":
            # 1a. Render hình dáng cơ bản của chữ màu trắng để làm khuôn (mask)
            text_shape = font.render(text, True, (255, 255, 255))
            width, height = text_shape.get_size()
    
            # 1b. Tạo một surface để vẽ gradient lên đó
            gradient_surf = pygame.Surface((width, height), pygame.SRCALPHA)
            # 1c. Vẽ gradient dọc từng dòng kẻ (từ trên xuống dưới)
            for y in range(height):
                    # Tính toán tỷ lệ vị trí hiện tại (từ 0.0 ở trên đỉnh đến 1.0 ở đáy)
                ratio = y / height
        
                # Nội suy màu giữa top_color và bottom_color dựa trên tỷ lệ
                r = int(effect['top_color'][0] * (1 - ratio) + effect['bottom_color'][0] * ratio)
                g = int(effect['top_color'][1] * (1 - ratio) + effect['bottom_color'][1] * ratio)
                b = int(effect['top_color'][2] * (1 - ratio) + effect['bottom_color'][2] * ratio)
                current_color = (r, g, b)
        
                # Vẽ 1 dòng ngang với màu đã tính
                pygame.draw.line(gradient_surf, current_color, (0, y), (width, y))
        
                # 1d. QUAN TRỌNG: Áp dụng khuôn chữ vào bề mặt gradient
                # Dùng chế độ BLEND_RGBA_MULT: Chỉ giữ lại màu gradient ở những nơi
                # mà text_shape có màu trắng. Phần nền trong suốt sẽ bị loại bỏ.
                gradient_surf.blit(text_shape, (0, 0), special_flags=pygame.BLEND_RGBA_MULT) 
                surface.blit(gradient_surf, (extra_space, extra_space))
        return surface
    
    def create_panel(self, screen, pygame, x, y, panel_color, panel_border_color, panel_transparent, draw_panel=True, draw_border=True,
                     border_width=2, padding=5, max_width=None, max_height=None,  auto_expand_height=True, auto_shrink_witdh=False,
                     texts="", text_colors=(0,0,0), text_fonts=('Times New Roman', 11), gap=5, gaps_list=None,
                     text_alignments=None, text_outlines=None, text_effects=None, test=False
                     ):
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
            Khoảng cách mặc định giữa các dòng text (chỉ dùng khi gaps_list=None)
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
        text_alignments : list hoặc str
            Canh lề cho text: 'left', 'center', 'right'
        draw_panel : bool
            True nếu vẽ panel (nền)
        draw_border : bool
            True nếu vẽ viền panel
        text_outline_effects : list, bool hoặc None
            Hiệu ứng outline cho text
        text_bevel_emboss_effects : list, bool hoặc None
            Hiệu ứng bevel/emboss cho text
        gaps_list : list of tuple hoặc None
            Danh sách khoảng cách giữa các text
            Mỗi tuple có dạng (line_gap, text_gap):
            - line_gap: khoảng cách giữa các dòng trong cùng 1 text
            - text_gap: khoảng cách từ đáy text này đến đỉnh text tiếp theo
            Nếu None: sử dụng gap cho cả line_gap và text_gap
        """
        
        #if not hasattr(self, 'screen'):
        #    self.screen = pygame.display.get_surface()
        self.screen = screen
        # 1. XỬ LÝ THAM SỐ text_alignments
        if text_alignments is None:
            text_alignments = ['left'] * len(texts)
        elif isinstance(text_alignments, str):
            text_alignments = [text_alignments] * len(texts)
        elif len(text_alignments) != len(texts):
            text_alignments = ['left'] * len(texts)
        
        # 2. XỬ LÝ THAM SỐ HIỆU ỨNG
        if text_outlines is None:
            text_outlines = [False] * len(texts)
        elif isinstance(text_outlines, bool):
            text_outlines = [text_outlines] * len(texts)
        elif len(text_outlines) != len(texts):
            text_outlines = [False] * len(texts)
        
        if text_effects is None:
            text_effects = [False] * len(texts)
        elif isinstance(text_effects, bool):
            text_effects = [text_effects] * len(texts)
        elif len(text_effects) != len(texts):
            text_effects = [False] * len(texts)
        
        # 3. XỬ LÝ THAM SỐ gaps_list
        if gaps_list is None:
            # Sử dụng gap cho cả line_gap và text_gap
            gaps_list = [(gap, gap)] * len(texts)
        elif len(gaps_list) != len(texts):
            # Nếu độ dài không khớp, sử dụng giá trị mặc định
            gaps_list = [(gap, gap)] * len(texts)
        
        # Đảm bảo mỗi phần tử là tuple 2 giá trị
        processed_gaps = []
        for gap_item in gaps_list:
            if isinstance(gap_item, (tuple, list)) and len(gap_item) >= 2:
                processed_gaps.append((int(gap_item[0]), int(gap_item[1])))
            else:
                processed_gaps.append((gap, gap))
        
        gaps_list = processed_gaps
        
        # 4. TÍNH TOÁN CHIỀU RỘNG PANEL
        if max_width is None:
            max_text_width = 0
            for i, text in enumerate(texts):
                text_surface = text_fonts[i].render(text, True, text_colors[i])
                max_text_width = max(max_text_width, text_surface.get_width())
            panel_width = max_text_width# + 2 * padding + 2 * border_width
        else:
            max_text_width = 0
            for i, text in enumerate(texts):
                text_surface = text_fonts[i].render(text, True, text_colors[i])
                max_text_width = max(max_text_width, text_surface.get_width())
            if max_text_width <= max_width and auto_shrink_witdh:
                panel_width = max_text_width# + 2 * padding + 2 * border_width
            else:
                panel_width = max_width
        
        # Chiều rộng vùng vẽ text
        text_area_width = panel_width - 2 * padding - 2 * border_width
        
        # 5. TÍNH TOÁN CHIỀU CAO CẦN THIẾT
        current_y = 0  # Vị trí y tính từ đỉnh panel (chưa tính padding, border)
        
        for i, text in enumerate(texts):
            font = text_fonts[i]
            font_height = font.get_height()
            line_gap, text_gap = gaps_list[i]
            
            # Tách text thành các dòng
            lines = self._calculate_text_lines(text, font, text_area_width)
            
            # Tính chiều cao của text hiện tại
            text_height = 0
            if lines:
                # Chiều cao = (số dòng * chiều cao font) + (khoảng cách giữa các dòng)
                text_height = len(lines) * font_height
                if len(lines) > 1:
                    text_height += (len(lines) - 1) * line_gap
            
            # Thêm chiều cao của text hiện tại
            current_y += text_height
            
            # Thêm text_gap sau text hiện tại (trừ text cuối cùng)
            if i < len(texts) - 1:
                current_y += text_gap
        
        # Tính chiều cao thực tế cần thiết
        required_height = current_y + 2 * padding + 2 * border_width
        
        # 6. XÁC ĐỊNH CHIỀU CAO PANEL THỰC TẾ
        if auto_expand_height:
            panel_height = required_height
        else:
            panel_height = required_height
        
        # Áp dụng giới hạn chiều cao tối đa nếu có
        if max_height is not None:
            panel_height = min(panel_height, max_height)
        
        # 7. TẠO SURFACE
        if panel_transparent:
            panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            if draw_panel and len(panel_color) == 4:
                panel_surface.fill(panel_color)
            elif draw_panel:
                panel_surface.fill((*panel_color, 128))
        else:
            if draw_panel:
                panel_surface = pygame.Surface((panel_width, panel_height))
                panel_surface.fill(panel_color)
            else:
                panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        
        # Vẽ viền
        if draw_border and draw_panel:
            pygame.draw.rect(panel_surface, panel_border_color, 
                            (0, 0, panel_width, panel_height), border_width)
        
        # 8. VẼ TEXT LÊN SURFACE
        current_y = padding + border_width  # Vị trí y bắt đầu vẽ
        text_area_height = panel_height - 2 * padding - 2 * border_width
        
        for i, text in enumerate(texts):
            font = text_fonts[i]
            color = text_colors[i]
            alignment = text_alignments[i]
            outline_effect = text_outlines[i]
            effect = text_effects[i]
            line_gap, text_gap = gaps_list[i]
            font_height = font.get_height()
            
            # Tách text thành các dòng
            lines = self._calculate_text_lines(text, font, text_area_width)
            
            # Vị trí y bắt đầu cho text hiện tại
            text_start_y = current_y
            
            # Vẽ từng dòng của text hiện tại
            for j, line in enumerate(lines):
                # Tạo text surface với hiệu ứng
                text_surface = self._create_text_with_effects(
                    pygame, font, line, color, 
                    effect,
                    outline_effect,
                )
                
                line_width = text_surface.get_width()
                line_height = text_surface.get_height()
                
                # Tính toán vị trí x dựa trên canh lề
                if alignment == 'left':
                    line_x = padding + border_width
                elif alignment == 'center':
                    line_x = (panel_width - line_width) // 2
                elif alignment == 'right':
                    line_x = panel_width - padding - border_width - line_width
                else:
                    line_x = padding + border_width
                
                # Tính toán vị trí y cho dòng hiện tại
                line_y = text_start_y + j * (font_height + line_gap)
                
                # Căn giữa text theo chiều dọc trong phạm vi font_height
                y_offset = (font_height - line_height) // 2
                
                # Kiểm tra xem còn đủ chỗ để vẽ không
                if line_y + font_height <= padding + border_width + text_area_height:
                    panel_surface.blit(text_surface, (line_x, line_y + y_offset))
                else:
                    # Hết chỗ, không vẽ thêm
                    break
            
            # Cập nhật vị trí y cho text tiếp theo
            # Tính chiều cao thực tế của text hiện tại
            text_height = 0
            if lines:
                text_height = len(lines) * font_height
                if len(lines) > 1:
                    text_height += (len(lines) - 1) * line_gap
            
            current_y = text_start_y + text_height
            
            # Thêm text_gap sau text hiện tại (trừ text cuối cùng)
            if i < len(texts) - 1:
                current_y += text_gap
        
        # 9. VẼ PANEL LÊN MÀN HÌNH
        if test==False:        
            self.screen.blit(panel_surface, (x, y))
        
        return pygame.Rect(x, y, panel_width, panel_height)

    #Hàm scle pygame font
    def scale_font(self, font, factor):
        name, size, style = font
        return (name, int(size * factor), style)