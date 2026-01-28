import pygame
import sys
import random

class TransparentPanelDemo:
    def __init__(self):
        # Khởi tạo Pygame
        pygame.init()
        
        # Thiết lập cửa sổ
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Panel Trong Suốt - Di chuyển bằng phím mũi tên")
        
        # Màu sắc
        self.COLORS = {
            'background': (240, 240, 245),
            'text': (30, 30, 40),
            'panel1': (255, 100, 100, 150),  # Đỏ, alpha=150
            'panel2': (100, 200, 255, 100),   # Xanh, alpha=100
            'panel3': (150, 255, 150, 120),   # Xanh lá, alpha=120
            'shapes': [(255, 200, 100), (200, 150, 255), (100, 220, 180)]
        }
        
        # Vị trí panel chính
        self.panel_x, self.panel_y = 200, 150
        self.panel_width, self.panel_height = 300, 200
        
        # Tạo font chữ
        self.font_large = pygame.font.SysFont('arial', 24, bold=True)
        self.font_normal = pygame.font.SysFont('arial', 18)
        self.font_small = pygame.font.SysFont('arial', 16)
        
        # Tạo các surface trong suốt
        self.create_transparent_surfaces()
        
        # Tạo các hình dạng ngẫu nhiên cho nền
        self.background_shapes = self.generate_background_shapes()
        
        # Biến điều khiển
        self.show_info = True
        self.current_alpha = 150
        
        # FPS controller
        self.clock = pygame.time.Clock()
        self.fps = 60
        
    def create_transparent_surfaces(self):
        """Tạo các surface trong suốt với kích thước khác nhau"""
        # Panel chính (lớn)
        self.main_panel = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)
        
        # Panel nhỏ 1
        self.small_panel1 = pygame.Surface((150, 120), pygame.SRCALPHA)
        
        # Panel nhỏ 2
        self.small_panel2 = pygame.Surface((180, 140), pygame.SRCALPHA)
        
    def generate_background_shapes(self):
        """Tạo các hình dạng ngẫu nhiên cho nền"""
        shapes = []
        for _ in range(15):
            shape_type = random.choice(['circle', 'rect', 'triangle'])
            x = random.randint(50, self.WIDTH - 50)
            y = random.randint(50, self.HEIGHT - 50)
            size = random.randint(30, 80)
            color = random.choice(self.COLORS['shapes'])
            speed = random.uniform(0.5, 2.0)
            direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
            
            shapes.append({
                'type': shape_type,
                'x': x, 'y': y,
                'size': size,
                'color': color,
                'speed': speed,
                'direction': direction
            })
        return shapes
    
    def draw_background(self):
        """Vẽ nền với các hình dạng chuyển động"""
        # Màu nền chính
        self.screen.fill(self.COLORS['background'])
        
        # Vẽ các hình dạng
        for shape in self.background_shapes:
            # Cập nhật vị trí
            shape['x'] += shape['direction'][0] * shape['speed']
            shape['y'] += shape['direction'][1] * shape['speed']
            
            # Kiểm tra biên và đảo hướng
            if shape['x'] < 50 or shape['x'] > self.WIDTH - 50:
                shape['direction'][0] *= -1
            if shape['y'] < 50 or shape['y'] > self.HEIGHT - 50:
                shape['direction'][1] *= -1
            
            # Vẽ hình dạng
            if shape['type'] == 'circle':
                pygame.draw.circle(self.screen, shape['color'], 
                                 (int(shape['x']), int(shape['y'])), 
                                 shape['size'], 2)  # Chỉ vẽ viền
            elif shape['type'] == 'rect':
                rect = pygame.Rect(shape['x'] - shape['size']//2, 
                                 shape['y'] - shape['size']//2, 
                                 shape['size'], shape['size'])
                pygame.draw.rect(self.screen, shape['color'], rect, 2)
            elif shape['type'] == 'triangle':
                points = [
                    (shape['x'], shape['y'] - shape['size']//2),
                    (shape['x'] - shape['size']//2, shape['y'] + shape['size']//2),
                    (shape['x'] + shape['size']//2, shape['y'] + shape['size']//2)
                ]
                pygame.draw.polygon(self.screen, shape['color'], points, 2)
    
    def draw_transparent_panel(self, surface, color, x, y, title="Panel"):
        """Vẽ một panel trong suốt với title và border"""
        # Xóa surface cũ
        surface.fill((0, 0, 0, 0))
        
        # Vẽ panel chính với viền
        pygame.draw.rect(surface, color, 
                        (0, 0, surface.get_width(), surface.get_height()),
                        border_radius=15)
        
        # Vẽ viền
        border_color = (color[0]//2, color[1]//2, color[2]//2, 200)
        pygame.draw.rect(surface, border_color,
                        (0, 0, surface.get_width(), surface.get_height()),
                        width=3, border_radius=15)
        
        # Thêm tiêu đề nếu có
        if title:
            title_surface = self.font_normal.render(title, True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(surface.get_width()//2, 25))
            
            # Vẽ thanh tiêu đề
            pygame.draw.rect(surface, (color[0]//2, color[1]//2, color[2]//2, 200),
                           (10, 10, surface.get_width()-20, 30),
                           border_radius=8)
            
            surface.blit(title_surface, title_rect)
        
        # Hiển thị surface lên màn hình
        self.screen.blit(surface, (x, y))
        
        return pygame.Rect(x, y, surface.get_width(), surface.get_height())
    
    def draw_text_on_panel(self, panel_rect, lines):
        """Vẽ text lên panel"""
        y_offset = 60
        for line in lines:
            text = self.font_small.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(midtop=(panel_rect.centerx, panel_rect.y + y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25
    
    def draw_info_panel(self):
        """Vẽ panel thông tin điều khiển"""
        if not self.show_info:
            return
            
        info_panel = pygame.Surface((250, 150), pygame.SRCALPHA)
        info_color = (50, 50, 60, 220)
        
        # Vẽ panel thông tin
        pygame.draw.rect(info_panel, info_color, 
                        (0, 0, 250, 150),
                        border_radius=10)
        
        # Thêm viền
        pygame.draw.rect(info_panel, (100, 100, 120, 255),
                        (0, 0, 250, 150),
                        width=2, border_radius=10)
        
        # Hiển thị
        self.screen.blit(info_panel, (20, 20))
        
        # Vẽ text
        info_lines = [
            "ĐIỀU KHIỂN:",
            "Mũi tên: Di chuyển panel",
            "A/D: Thay đổi độ mờ",
            "I: Bật/tắt thông tin",
            "R: Đặt lại vị trí",
            "ESC: Thoát"
        ]
        
        y_offset = 30
        for line in info_lines:
            color = (255, 255, 255) if ":" in line else (200, 200, 220)
            font = self.font_small if ":" not in line else self.font_small
            text = font.render(line, True, color)
            self.screen.blit(text, (35, 20 + y_offset))
            y_offset += 20 if ":" in line else 25
    
    def draw_alpha_indicator(self):
        """Hiển thị thanh chỉ độ mờ"""
        # Vẽ nền thanh
        bar_rect = pygame.Rect(self.WIDTH - 220, 20, 200, 30)
        pygame.draw.rect(self.screen, (50, 50, 60, 220), bar_rect, border_radius=5)
        
        # Vẽ thanh độ mờ
        alpha_width = int((self.current_alpha / 255) * 180)
        alpha_bar = pygame.Rect(self.WIDTH - 210, 25, alpha_width, 20)
        pygame.draw.rect(self.screen, (100, 200, 100), alpha_bar, border_radius=3)
        
        # Vẽ text
        alpha_text = self.font_small.render(f"Độ mờ: {self.current_alpha}/255", True, (255, 255, 255))
        self.screen.blit(alpha_text, (self.WIDTH - 210, 55))
    
    def run(self):
        """Vòng lặp chính của chương trình"""
        running = True
        
        while running:
            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    # Thoát khi nhấn ESC
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    # Bật/tắt thông tin
                    elif event.key == pygame.K_i:
                        self.show_info = not self.show_info
                    
                    # Reset vị trí
                    elif event.key == pygame.K_r:
                        self.panel_x, self.panel_y = 200, 150
                    
                    # Thay đổi độ mờ
                    elif event.key == pygame.K_a:  # Giảm độ mờ
                        self.current_alpha = max(50, self.current_alpha - 25)
                        self.COLORS['panel1'] = (255, 100, 100, self.current_alpha)
                    
                    elif event.key == pygame.K_d:  # Tăng độ mờ
                        self.current_alpha = min(255, self.current_alpha + 25)
                        self.COLORS['panel1'] = (255, 100, 100, self.current_alpha)
            
            # Điều khiển di chuyển bằng phím mũi tên
            keys = pygame.key.get_pressed()
            speed = 5
            if keys[pygame.K_LEFT]:
                self.panel_x -= speed
            if keys[pygame.K_RIGHT]:
                self.panel_x += speed
            if keys[pygame.K_UP]:
                self.panel_y -= speed
            if keys[pygame.K_DOWN]:
                self.panel_y += speed
            
            # Giới hạn di chuyển trong màn hình
            self.panel_x = max(0, min(self.WIDTH - self.panel_width, self.panel_x))
            self.panel_y = max(0, min(self.HEIGHT - self.panel_height, self.panel_y))
            
            # Vẽ nền
            self.draw_background()
            
            # Vẽ các panel trong suốt
            panel1_rect = self.draw_transparent_panel(
                self.main_panel, 
                self.COLORS['panel1'],
                self.panel_x, self.panel_y,
                "PANEL CHÍNH"
            )
            
            # Vẽ panel nhỏ 1
            panel2_rect = self.draw_transparent_panel(
                self.small_panel1,
                self.COLORS['panel2'],
                self.panel_x + 320, self.panel_y + 50,
                "Panel nhỏ 1"
            )
            
            # Vẽ panel nhỏ 2
            panel3_rect = self.draw_transparent_panel(
                self.small_panel2,
                self.COLORS['panel3'],
                self.panel_x - 100, self.panel_y + 80,
                "Panel nhỏ 2"
            )
            
            # Thêm text vào panel chính
            self.draw_text_on_panel(panel1_rect, [
                "Panel này có độ mờ",
                f"Alpha: {self.current_alpha}/255",
                "Có thể nhìn thấy nền",
                "Di chuyển panel bằng",
                "phím mũi tên"
            ])
            
            # Vẽ panel thông tin
            self.draw_info_panel()
            
            # Vẽ thanh chỉ độ mờ
            self.draw_alpha_indicator()
            
            # Vẽ hướng dẫn di chuyển
            move_text = self.font_small.render(f"Vị trí: ({self.panel_x}, {self.panel_y})", 
                                              True, self.COLORS['text'])
            self.screen.blit(move_text, (self.WIDTH // 2 - 100, self.HEIGHT - 40))
            
            # Cập nhật màn hình
            pygame.display.flip()
            
            # Giới hạn FPS
            self.clock.tick(self.fps)
        
        # Thoát Pygame
        pygame.quit()
        sys.exit()

# Chạy chương trình
if __name__ == "__main__":
    print("=" * 50)
    print("CHƯƠNG TRÌNH DEMO PANEL TRONG SUỐT")
    print("=" * 50)
    print("Hướng dẫn sử dụng:")
    print("  • Mũi tên: Di chuyển panel chính")
    print("  • A/D: Giảm/Tăng độ mờ")
    print("  • I: Bật/tắt panel thông tin")
    print("  • R: Đặt lại vị trí panel")
    print("  • ESC: Thoát chương trình")
    print("=" * 50)
    print()
    
    app = TransparentPanelDemo()
    app.run()