import pygame
import sys
import math

# Khởi tạo pygame
pygame.init()

# Tạo cửa sổ
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Text Effect - Hiệu ứng chữ 3D")

# Màu nền
BACKGROUND = (240, 240, 245)

# Tải font
try:
    font = pygame.font.SysFont("Arial", 80, bold=True)
    small_font = pygame.font.SysFont("Arial", 36)
except:
    font = pygame.font.Font(None, 80)
    small_font = pygame.font.Font(None, 36)

def create_3d_text_effect(text, font, color, thickness=10, outline_color=(0, 0, 0), outline_width=3):
    """
    Tạo hiệu ứng 3D text với phần bo tròn ở trên
    """
    # Bước 1: Tạo text cơ bản
    base_surf = font.render(text, True, color)
    base_width, base_height = base_surf.get_size()
    
    # Tạo mask để biết vị trí của text
    text_mask = pygame.mask.from_surface(base_surf)
    
    # Bước 2: Tạo surface 3D
    # Chiều cao = text_height + thickness (thêm phần đáy)
    surf_width = base_width + outline_width * 2
    surf_height = base_height + thickness + outline_width * 2
    
    final_surf = pygame.Surface((surf_width, surf_height), pygame.SRCALPHA)
    
    # Bước 3: Vẽ outline (nếu có)
    if outline_width > 0:
        # Vẽ text outline tại nhiều vị trí để tạo outline dày
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    outline_text = font.render(text, True, outline_color)
                    final_surf.blit(outline_text, 
                                  (outline_width + dx, outline_width + dy))
    
    # Bước 4: Vẽ phần 3D (thân và đáy)
    # Vẽ phần thân bên dưới text
    for y_offset in range(1, thickness + 1):
        # Tạo gradient màu cho phần thân (tối dần)
        darken_factor = 0.7 - (y_offset / thickness) * 0.3
        body_color = (
            int(color[0] * darken_factor),
            int(color[1] * darken_factor),
            int(color[2] * darken_factor)
        )
        
        body_surf = font.render(text, True, body_color)
        final_surf.blit(body_surf, (outline_width, outline_width + y_offset))
    
    # Bước 5: Vẽ phần bo tròn phía trên
    # Phần bo tròn là các pixel ở mép trên của text
    # Tạo gradient từ sáng (trên cùng) đến tối (dưới cùng của phần bo)
    for y in range(thickness):
        # Tính độ sáng (sáng nhất ở trên cùng, tối dần xuống dưới)
        brightness = 1.0 - (y / thickness) * 0.5
        
        # Màu sáng hơn cho phần bo tròn
        bevel_color = (
            min(255, int(color[0] * brightness * 1.2)),
            min(255, int(color[1] * brightness * 1.2)),
            min(255, int(color[2] * brightness * 1.2))
        )
        
        # Vẽ từng dòng của phần bo tròn
        for x in range(base_width):
            # Kiểm tra xem ở vị trí này có text không
            # Chỉ vẽ bo tròn ở những chỗ có text
            has_text = False
            for check_y in range(min(thickness, base_height)):
                if text_mask.get_at((x, check_y)):
                    has_text = True
                    break
            
            if has_text:
                # Vẽ pixel bo tròn
                # Vị trí Y tính từ trên xuống
                final_surf.set_at((outline_width + x, outline_width + y), bevel_color)
    
    # Bước 6: Vẽ text gốc lên trên cùng (mặt phẳng)
    final_surf.blit(base_surf, (outline_width, outline_width))
    
    return final_surf

def create_simple_3d_text(text, font, color, thickness=10):
    """
    Phiên bản đơn giản hơn của hiệu ứng 3D
    """
    # Tạo text cơ bản
    base_surf = font.render(text, True, color)
    base_width, base_height = base_surf.get_size()
    
    # Tạo surface cho hiệu ứng 3D
    surf_width = base_width + thickness
    surf_height = base_height + thickness
    
    final_surf = pygame.Surface((surf_width, surf_height), pygame.SRCALPHA)
    
    # Vẽ phần "đổ bóng" cho hiệu ứng 3D
    # Vẽ nhiều layer lệch nhau để tạo chiều sâu
    for i in range(thickness, 0, -1):
        # Màu tối dần theo chiều sâu
        dark_factor = 0.3 + 0.7 * (i / thickness)
        shadow_color = (
            int(color[0] * dark_factor),
            int(color[1] * dark_factor),
            int(color[2] * dark_factor)
        )
        
        shadow_surf = font.render(text, True, shadow_color)
        # Vẽ lệch xuống dưới và sang phải
        final_surf.blit(shadow_surf, (i, i))
    
    # Vẽ text gốc lên trên cùng
    final_surf.blit(base_surf, (0, 0))
    
    return final_surf

# Tạo các text mẫu
texts = []

# Text 1: 3D với outline
text1_surf = create_3d_text_effect(
    "3D TEXT", font, 
    color=(100, 150, 255),  # Xanh dương
    thickness=12,
    outline_color=(0, 0, 0),
    outline_width=3
)
texts.append({
    "surface": text1_surf,
    "x": width // 2 - text1_surf.get_width() // 2,
    "y": 150,
    "label": "3D với outline đen"
})

# Text 2: 3D không outline
text2_surf = create_simple_3d_text(
    "PYGAME 3D", font,
    color=(255, 100, 150),  # Hồng
    thickness=15
)
texts.append({
    "surface": text2_surf,
    "x": width // 2 - text2_surf.get_width() // 2,
    "y": 300,
    "label": "3D không outline"
})

# Text 3: Màu khác
text3_surf = create_3d_text_effect(
    "HELLO", font,
    color=(100, 255, 150),  # Xanh lá
    thickness=10,
    outline_color=(50, 50, 100),
    outline_width=2
)
texts.append({
    "surface": text3_surf,
    "x": width // 2 - text3_surf.get_width() // 2,
    "y": 450,
    "label": "3D với outline xanh đậm"
})

# Vòng lặp chính
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Vẽ nền
    screen.fill(BACKGROUND)
    
    # Vẽ tiêu đề
    title = small_font.render("Hiệu ứng chữ 3D với phần bo tròn", True, (50, 50, 80))
    screen.blit(title, (width // 2 - title.get_width() // 2, 30))
    
    # Vẽ minh họa hiệu ứng 3D
    pygame.draw.rect(screen, (220, 220, 220), (50, 100, 300, 150), 2)
    pygame.draw.line(screen, (200, 100, 100), (100, 120), (180, 120), 3)  # Mặt trên
    pygame.draw.line(screen, (100, 100, 200), (180, 120), (180, 200), 3)  # Mặt bên
    pygame.draw.line(screen, (150, 150, 150), (100, 120), (100, 200), 3)  # Mặt bên khác
    pygame.draw.line(screen, (100, 200, 100), (100, 200), (180, 200), 3)  # Mặt đáy
    
    # Vẽ mô tả
    desc1 = small_font.render("Mặt trên: bo tròn", True, (80, 80, 100))
    desc2 = small_font.render("Mặt bên: thẳng đứng", True, (80, 80, 100))
    desc3 = small_font.render("Mặt đáy: phẳng", True, (80, 80, 100))
    screen.blit(desc1, (60, 130))
    screen.blit(desc2, (60, 170))
    screen.blit(desc3, (60, 210))
    
    # Vẽ các text
    for text_info in texts:
        screen.blit(text_info["surface"], (text_info["x"], text_info["y"]))
        
        # Vẽ label
        label = small_font.render(text_info["label"], True, (70, 70, 90))
        screen.blit(label, (text_info["x"], text_info["y"] - 40))
    
    # Vẽ hướng dẫn
    instruction = small_font.render("Nhấn ESC để thoát", True, (100, 100, 120))
    screen.blit(instruction, (width // 2 - instruction.get_width() // 2, height - 50))
    
    # Vẽ thông tin
    info = small_font.render("Ánh sáng chiếu từ góc trên-trái 45°", True, (100, 100, 120))
    screen.blit(info, (width // 2 - info.get_width() // 2, height - 90))
    
    # Vẽ biểu tượng ánh sáng
    light_x, light_y = width - 100, 80
    pygame.draw.circle(screen, (255, 255, 200), (light_x, light_y), 20)
    # Vẽ tia sáng
    for angle in range(30, 60, 5):
        rad = math.radians(angle)
        end_x = light_x + 50 * math.cos(rad)
        end_y = light_y + 50 * math.sin(rad)
        pygame.draw.line(screen, (255, 255, 100, 100), (light_x, light_y), (end_x, end_y), 2)
    
    light_label = small_font.render("Ánh sáng", True, (120, 120, 80))
    screen.blit(light_label, (light_x - 40, light_y - 40))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()