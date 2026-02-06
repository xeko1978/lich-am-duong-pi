class PanelRenderer:
    def _calculate_text_lines(self, text, font, max_width):
        """
        Tính toán và tách text thành các dòng dựa trên max_width
        """
        if not text:
            return []
        
        words = text.split(' ')
        lines = []
        current_line = ''
        
        for word in words:
            if not word:
                continue
                
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
                                 outline_effect=False, outline_color=(255, 255, 255),
                                 bevel_emboss_effect=False, bevel_offset=2):
        """
        Tạo surface text với hiệu ứng outline và bevel/emboss
        """
        # Tạo text gốc
        text_surface = font.render(text, True, color)
        
        if not outline_effect and not bevel_emboss_effect:
            return text_surface
        
        # Tính toán không gian thêm cho hiệu ứng
        extra_space = bevel_offset + 2 if bevel_emboss_effect else 2
        surface_width = text_surface.get_width() + extra_space * 2
        surface_height = text_surface.get_height() + extra_space * 2
        
        surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
        
        # Vẽ outline
        if outline_effect:
            offsets = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
            for dx, dy in offsets:
                outline_surf = font.render(text, True, outline_color)
                surface.blit(outline_surf, (extra_space + dx, extra_space + dy))
        
        # Vẽ bevel/emboss
        if bevel_emboss_effect:
            shadow_color = (0, 0, 0, 150)
            shadow_surf = font.render(text, True, shadow_color)
            surface.blit(shadow_surf, (extra_space + bevel_offset, extra_space + bevel_offset))
            
            highlight_color = (255, 255, 255, 150)
            highlight_surf = font.render(text, True, highlight_color)
            surface.blit(highlight_surf, (extra_space - bevel_offset, extra_space - bevel_offset))
        
        # Vẽ text chính
        surface.blit(text_surface, (extra_space, extra_space))
        
        return surface
    
    def create_panel(self, screen, pygame, x, y, panel_color, panel_border_color, panel_transparent, 
                     texts, text_colors, text_fonts, gap=0, auto_expand_height=True, 
                     border_width=2, padding=10, max_width=None, max_height=None, 
                     text_alignments=None, draw_panel=True, draw_border=True,
                     text_outline_effects=None, text_bevel_emboss_effects=None,
                     gaps_list=None, test=False):
        """
        Vẽ panel với text tự động xuống dòng và điều chỉnh chiều cao
        
        Parameters:
        -----------
        gaps_list : list of tuple hoặc None
            Danh sách khoảng cách giữa các text
            Mỗi tuple có dạng (line_gap, text_gap)
            - line_gap: khoảng cách giữa các dòng trong cùng 1 text
            - text_gap: khoảng cách từ đáy text này đến đỉnh text tiếp theo
        """
        
        #if not hasattr(self, 'screen'):
        #    self.screen = pygame.display.get_surface()
        self.screen=screen

        # 1. XỬ LÝ THAM SỐ
        if text_alignments is None:
            text_alignments = ['left'] * len(texts)
        elif isinstance(text_alignments, str):
            text_alignments = [text_alignments] * len(texts)
        elif len(text_alignments) != len(texts):
            text_alignments = ['left'] * len(texts)
        
        # Xử lý hiệu ứng
        if text_outline_effects is None:
            text_outline_effects = [False] * len(texts)
        elif isinstance(text_outline_effects, bool):
            text_outline_effects = [text_outline_effects] * len(texts)
        elif len(text_outline_effects) != len(texts):
            text_outline_effects = [False] * len(texts)
        
        if text_bevel_emboss_effects is None:
            text_bevel_emboss_effects = [False] * len(texts)
        elif isinstance(text_bevel_emboss_effects, bool):
            text_bevel_emboss_effects = [text_bevel_emboss_effects] * len(texts)
        elif len(text_bevel_emboss_effects) != len(texts):
            text_bevel_emboss_effects = [False] * len(texts)
        
        # Xử lý gaps_list
        if gaps_list is None:
            gaps_list = [(gap, gap)] * len(texts)
        elif len(gaps_list) != len(texts):
            gaps_list = [(gap, gap)] * len(texts)
        
        processed_gaps = []
        for gap_item in gaps_list:
            if isinstance(gap_item, (tuple, list)) and len(gap_item) >= 2:
                processed_gaps.append((int(gap_item[0]), int(gap_item[1])))
            else:
                processed_gaps.append((gap, gap))
        gaps_list = processed_gaps
        
        # 2. TÍNH TOÁN CHIỀU RỘNG PANEL
        if max_width is None:
            max_text_width = 0
            for i, text in enumerate(texts):
                text_surface = text_fonts[i].render(text, True, text_colors[i])
                max_text_width = max(max_text_width, text_surface.get_width())
            panel_width = max_text_width + 2 * padding + 2 * border_width
        else:
            panel_width = max_width
        
        text_area_width = panel_width - 2 * padding - 2 * border_width
        
        # 3. TÍNH TOÁN CHIỀU CAO CẦN THIẾT (đơn giản hóa)
        current_y = 0
        
        for i, text in enumerate(texts):
            font = text_fonts[i]
            line_gap, text_gap = gaps_list[i]
            
            # Tính chiều cao font
            font_height = font.get_height()
            
            # Tách text thành các dòng
            lines = self._calculate_text_lines(text, font, text_area_width)
            
            # Tính chiều cao cho text này
            if lines:
                text_height = len(lines) * font_height
                if len(lines) > 1:
                    text_height += (len(lines) - 1) * line_gap
                
                current_y += text_height
                
                # Thêm text_gap sau text (trừ text cuối)
                if i < len(texts) - 1:
                    current_y += text_gap
        
        # Tính chiều cao thực tế cần thiết
        required_height = current_y + 2 * padding + 2 * border_width
        
        # 4. XÁC ĐỊNH CHIỀU CAO PANEL
        if auto_expand_height:
            panel_height = required_height
        else:
            panel_height = required_height
        
        if max_height is not None:
            panel_height = min(panel_height, max_height)
        
        # 5. TẠO SURFACE
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
        
        # 6. VẼ TEXT LÊN SURFACE (sử dụng bounding box và căn giữa)
        current_y = padding + border_width
        text_area_height = panel_height - 2 * padding - 2 * border_width
        for i, text in enumerate(texts):
            font = text_fonts[i]
            color = text_colors[i]
            alignment = text_alignments[i]
            outline_effect = text_outline_effects[i]
            bevel_effect = text_bevel_emboss_effects[i]
            line_gap, text_gap = gaps_list[i]
            font_height = font.get_height()
            
            # Tách text thành các dòng
            lines = self._calculate_text_lines(text, font, text_area_width)
            
            # Vẽ từng dòng
            for j, line in enumerate(lines):
                # Tạo text surface với hiệu ứng
                text_surface = self._create_text_with_effects(
                    pygame, font, line, color, 
                    outline_effect, (255, 255, 255),
                    bevel_effect, 2
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
                
                # Tính vị trí y: căn giữa text trong ô có chiều cao font_height
                line_y = current_y + j * (font_height + line_gap)
                y_offset = (font_height - line_height) // 2
                
                # Kiểm tra xem còn đủ chỗ để vẽ không
                if line_y + y_offset + line_height <= padding + border_width + text_area_height:
                    panel_surface.blit(text_surface, (line_x, line_y + y_offset))
                else:
                    break
            
            # Cập nhật vị trí y cho text tiếp theo
            if lines:
                text_height = len(lines) * font_height
                if len(lines) > 1:
                    text_height += (len(lines) - 1) * line_gap
                current_y += text_height
            
            # Thêm text_gap sau text (trừ text cuối)
            if i < len(texts) - 1:
                current_y += text_gap
        
        # 7. VẼ PANEL LÊN MÀN HÌNH
        if test==False:        
            self.screen.blit(panel_surface, (x, y))
        
        return pygame.Rect(x, y, panel_width, panel_height)
    
    @staticmethod
    def create_simple_panel(pygame, x, y, width, texts, bg_color=(200, 200, 200), 
                           border_color=(50, 50, 50), font=None, text_color=(0, 0, 0),
                           align='left', draw_panel=True, draw_border=True,
                           gaps_list=None):
        """
        Tạo panel đơn giản với các tham số mặc định
        """
        if font is None:
            font = pygame.font.SysFont(None, 24)
        
        renderer = PanelRenderer()
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
            text_alignments=align,
            draw_panel=draw_panel,
            draw_border=draw_border,
            gaps_list=gaps_list
        )