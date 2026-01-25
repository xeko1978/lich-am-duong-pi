import tkinter as tk
from tkinter import font
import datetime
import math


# ================================
# PHẦN TÍNH ÂM LỊCH CỦA HỒ NGỌC ĐỨC
# ================================

class LunarDate:
    """Lớp tính âm lịch dựa trên thuật toán của Hồ Ngọc Đức"""

    def __init__(self, dd, mm, yy):
        self.day = dd
        self.month = mm
        self.year = yy
        self.jd = self.jdFromDate(dd, mm, yy)
        self.lunarYear, self.lunarMonth, self.lunarDay, self.lunarLeap = self.convertSolar2Lunar()

    def jdFromDate(self, dd, mm, yy):
        """Tính số ngày Julian từ ngày dương"""
        a = int((14 - mm) / 12)
        y = yy + 4800 - a
        m = mm + 12 * a - 3
        jd = dd + int((153 * m + 2) / 5) + 365 * y + int(y / 4) - int(y / 100) + int(y / 400) - 32045
        if jd < 2299161:
            jd = dd + int((153 * m + 2) / 5) + 365 * y + int(y / 4) - 32083
        return jd

    def getNewMoonDay(self, k, timeZone):
        """Tính ngày Sóc (new moon)"""
        T = k / 1236.85  # Time in Julian centuries
        T2 = T * T
        T3 = T2 * T
        dr = math.pi / 180
        Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3
        Jd1 = Jd1 + 0.00033 * math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr)
        M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3
        Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3
        F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3
        C1 = (0.1734 - 0.000393 * T) * math.sin(M * dr) + 0.0021 * math.sin(2 * dr * M)
        C1 = C1 - 0.4068 * math.sin(Mpr * dr) + 0.0161 * math.sin(dr * 2 * Mpr)
        C1 = C1 - 0.0004 * math.sin(dr * 3 * Mpr)
        C1 = C1 + 0.0104 * math.sin(dr * 2 * F) - 0.0051 * math.sin(dr * (M + Mpr))
        C1 = C1 - 0.0074 * math.sin(dr * (M - Mpr)) + 0.0004 * math.sin(dr * (2 * F + M))
        C1 = C1 - 0.0004 * math.sin(dr * (2 * F - M)) - 0.0006 * math.sin(dr * (2 * F + Mpr))
        C1 = C1 + 0.0010 * math.sin(dr * (2 * F - Mpr)) + 0.0005 * math.sin(dr * (2 * Mpr + M))
        if T < -11:
            deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
        else:
            deltat = -0.000278 + 0.000265 * T + 0.000262 * T2
        JdNew = Jd1 + C1 - deltat
        return int(JdNew + 0.5 + timeZone / 24)

    def getSunLongitude(self, jdn, timeZone):
        """Tính kinh độ mặt trời"""
        T = (jdn - 2451545.5 - timeZone / 24) / 36525
        T2 = T * T
        dr = math.pi / 180
        M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
        L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2
        DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr * M)
        DL = DL + (0.019993 - 0.000101 * T) * math.sin(dr * 2 * M) + 0.000290 * math.sin(dr * 3 * M)
        L = L0 + DL
        L = L * dr
        L = L - math.pi * 2 * (int(L / (math.pi * 2)))
        return int(L / math.pi * 6)

    def getLunarMonth11(self, yy, timeZone):
        """Tìm tháng 11 âm bắt đầu năm âm lịch"""
        off = self.jdFromDate(31, 12, yy) - 2415021
        k = int(off / 29.530588853)
        nm = self.getNewMoonDay(k, timeZone)
        sunLong = self.getSunLongitude(nm, timeZone)
        if sunLong >= 9:
            nm = self.getNewMoonDay(k - 1, timeZone)
        return nm

    def getLeapMonthOffset(self, a11, timeZone):
        """Tính tháng nhuận"""
        k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
        last = 0
        i = 1
        arc = self.getSunLongitude(self.getNewMoonDay(k + i, timeZone), timeZone)
        while True:
            last = arc
            i += 1
            arc = self.getSunLongitude(self.getNewMoonDay(k + i, timeZone), timeZone)
            if not (arc != last and i < 14):
                break
        return i - 1

    def convertSolar2Lunar(self):
        """Chuyển đổi ngày dương sang âm lịch"""
        timeZone = 7.0  # Múi giờ Việt Nam

        # Tính ngày tháng âm
        dayNumber = self.jd
        k = int((dayNumber - 2415021.076998695) / 29.530588853)
        monthStart = self.getNewMoonDay(k + 1, timeZone)
        if monthStart > dayNumber:
            monthStart = self.getNewMoonDay(k, timeZone)

        a11 = self.getLunarMonth11(self.year, timeZone)
        b11 = a11
        if a11 >= monthStart:
            lunarYear = self.year
            a11 = self.getLunarMonth11(self.year - 1, timeZone)
        else:
            lunarYear = self.year + 1
            b11 = self.getLunarMonth11(self.year + 1, timeZone)

        lunarDay = dayNumber - monthStart + 1
        diff = int((monthStart - a11) / 29)
        lunarLeap = 0
        lunarMonth = diff + 11
        if b11 - a11 > 365:
            leapMonthDiff = self.getLeapMonthOffset(a11, timeZone)
            if diff >= leapMonthDiff:
                lunarMonth = diff + 10
                if diff == leapMonthDiff:
                    lunarLeap = 1

        if lunarMonth > 12:
            lunarMonth = lunarMonth - 12

        if lunarMonth >= 11 and diff < 4:
            lunarYear -= 1

        return lunarYear, lunarMonth, lunarDay, lunarLeap

    def getCanChiYear(self, year):
        """Tính can chi của năm"""
        can = ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"]
        chi = ["Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi"]
        return can[year % 10], chi[year % 12]

    def getCanChiMonth(self, year, month):
        """Tính can chi của tháng"""
        can = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        chi = ["Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu"]

        # Tính can tháng theo năm
        can_index = (year * 12 + month + 3) % 10
        chi_index = (month - 1) % 12

        return can[can_index], chi[chi_index]

    def getCanChiDay(self, jd):
        """Tính can chi của ngày"""
        can = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        chi = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

        # Công thức tính can chi ngày từ số ngày Julian
        can_index = (int(jd) + 9) % 10
        chi_index = (int(jd) + 1) % 12

        return can[can_index], chi[chi_index]


# ================================
# PHẦN GIAO DIỆN
# ================================

class LunarCalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lịch Âm Dương - Thuật toán Hồ Ngọc Đức")
        self.root.configure(bg='#2c3e50')

        # Các câu trích dẫn
        self.quotes = [
            "Sự vắng mặt mài sắc tình yêu, sự hiện diện gia cố nó. - Thomas Fuller",
            "Thời gian là thứ quý giá nhất mà chúng ta có. - Aristotle",
            "Mỗi ngày là một trang mới trong cuộc đời bạn. - Khuyết danh",
            "Hãy sống như thể bạn sẽ chết vào ngày mai. Học như thể bạn sẽ sống mãi mãi. - Mahatma Gandhi"
        ]

        # Màu sắc chủ đạo
        self.colors = {
            'bg': '#2c3e50',
            'main': 'white',
            'header': '#3498db',
            'day': '#e74c3c',
            'lunar': '#27ae60',
            'hour': '#9b59b6',
            'quote_bg': '#e8f4f8',
            'lucky_bg': '#ffeaa7',
            'lunar_bg': '#d5f4e6'
        }

        # Khởi tạo giao diện
        self.setup_ui()

        # Cập nhật thời gian thực
        self.update_time()

    def setup_ui(self):
        """Thiết lập giao diện chính"""
        # Frame chính với viền
        self.main_frame = tk.Frame(self.root, bg='white',
                                   highlightbackground=self.colors['header'],
                                   highlightthickness=2,
                                   relief='ridge')
        self.main_frame.pack(padx=20, pady=20)

        # Kích thước cố định
        self.main_frame.pack_propagate(False)
        self.main_frame.config(width=450, height=620)

    def update_time(self):
        """Cập nhật thời gian và thông tin"""
        now = datetime.datetime.now()

        # Xóa widget cũ
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # ===== HEADER: Tháng/Năm Dương lịch =====
        header_font = font.Font(family="Arial", size=20, weight="bold")
        month_names = ["", "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5",
                       "Tháng 6", "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10",
                       "Tháng 11", "Tháng 12"]
        header = tk.Label(self.main_frame,
                          text=f"{month_names[now.month]}-{now.year}",
                          font=header_font,
                          bg='white',
                          fg=self.colors['header'])
        header.pack(pady=(25, 5))

        # ===== NGÀY DƯƠNG LỊCH LỚN =====
        day_font = font.Font(family="Arial", size=85, weight="bold")
        day_label = tk.Label(self.main_frame,
                             text=f"{now.day:02d}",
                             font=day_font,
                             bg='white',
                             fg=self.colors['day'])
        day_label.pack()

        # ===== THỨ TRONG TUẦN =====
        weekday_font = font.Font(family="Arial", size=22, weight="bold")
        weekdays = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm",
                    "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
        weekday_label = tk.Label(self.main_frame,
                                 text=weekdays[now.weekday()],
                                 font=weekday_font,
                                 bg='white',
                                 fg=self.colors['bg'])
        weekday_label.pack(pady=5)

        # ===== CÂU TRÍCH DẪN =====
        quote_index = (now.day - 1) % len(self.quotes)
        quote_frame = tk.Frame(self.main_frame, bg=self.colors['quote_bg'], height=75)
        quote_frame.pack(fill='x', padx=30, pady=15)
        quote_frame.pack_propagate(False)

        quote_font = font.Font(family="Arial", size=11, slant="italic")
        quote = tk.Label(quote_frame,
                         text=self.quotes[quote_index],
                         font=quote_font,
                         bg=self.colors['quote_bg'],
                         fg='#2c3e50',
                         justify='center',
                         wraplength=350)
        quote.pack(expand=True, padx=10, pady=10)

        # ===== PHẦN THÔNG TIN GIỜ =====
        time_frame = tk.Frame(self.main_frame, bg='white')
        time_frame.pack(pady=10)

        # Giờ âm lịch
        lunar_hour_info = self.get_lunar_hour_info(now.hour)
        hour_font = font.Font(family="Arial", size=14, weight="bold")

        # Cột 1: Tên giờ
        hour_col1 = tk.Frame(time_frame, bg='white')
        hour_col1.grid(row=0, column=0, padx=15)

        tk.Label(hour_col1, text="GIỜ ÂM LỊCH",
                 font=font.Font(family="Arial", size=12),
                 bg='white', fg='#7f8c8d').pack()

        tk.Label(hour_col1, text=lunar_hour_info['name'],
                 font=hour_font,
                 bg='white', fg=self.colors['hour']).pack()

        # Cột 2: Thời gian hiện tại
        time_col = tk.Frame(time_frame, bg='white')
        time_col.grid(row=0, column=1, padx=15)

        tk.Label(time_col, text="GIỜ HIỆN TẠI",
                 font=font.Font(family="Arial", size=12),
                 bg='white', fg='#7f8c8d').pack()

        time_str = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
        tk.Label(time_col, text=time_str,
                 font=font.Font(family="Arial", size=24, weight="bold"),
                 bg='white', fg=self.colors['day']).pack()

        # Cột 3: Giờ tốt
        good_hours_col = tk.Frame(time_frame, bg='white')
        good_hours_col.grid(row=0, column=2, padx=15)

        tk.Label(good_hours_col, text="GIỜ TỐT",
                 font=font.Font(family="Arial", size=12),
                 bg='white', fg='#7f8c8d').pack()

        good_hours = ["Dần(3-5)", "Thìn(7-9)", "Tỵ(9-11)",
                      "Thân(15-17)", "Dậu(17-19)", "Hợi(21-23)"]
        good_hours_text = "\n".join(good_hours[:3]) + "\n" + "\n".join(good_hours[3:])
        tk.Label(good_hours_col, text=good_hours_text,
                 font=font.Font(family="Arial", size=10, weight="bold"),
                 bg='white', fg=self.colors['lunar'],
                 justify='center').pack()

        # ===== NGÀY HOÀNG ĐẠO =====
        lunar_date = LunarDate(now.day, now.month, now.year)
        is_lucky_day = self.is_lucky_day(lunar_date.lunarDay, lunar_date.lunarMonth)

        lucky_frame = tk.Frame(self.main_frame, bg=self.colors['lucky_bg'], height=55)
        lucky_frame.pack(fill='x', padx=40, pady=15)
        lucky_frame.pack_propagate(False)

        lucky_font = font.Font(family="Arial", size=14, weight="bold")
        lucky_color = '#e74c3c' if is_lucky_day else '#7f8c8d'
        lucky_text = "NGÀY HOÀNG ĐẠO" if is_lucky_day else "NGÀY BÌNH THƯỜNG"

        tk.Label(lucky_frame, text=lucky_text,
                 font=lucky_font,
                 bg=self.colors['lucky_bg'],
                 fg=lucky_color).pack(expand=True)

        # ===== THÔNG TIN ÂM LỊCH =====
        lunar_info = self.get_lunar_date_info(now)
        lunar_frame = tk.Frame(self.main_frame, bg=self.colors['lunar_bg'], height=110)
        lunar_frame.pack(fill='x', padx=30, pady=15)
        lunar_frame.pack_propagate(False)

        # Tiêu đề Âm lịch
        title_font = font.Font(family="Arial", size=18, weight="bold")
        tk.Label(lunar_frame, text="ÂM LỊCH VIỆT NAM",
                 font=title_font,
                 bg=self.colors['lunar_bg'],
                 fg=self.colors['lunar']).pack(pady=(15, 5))

        # Thông tin chi tiết âm lịch
        info_font = font.Font(family="Arial", size=14)
        tk.Label(lunar_frame, text=lunar_info,
                 font=info_font,
                 bg=self.colors['lunar_bg'],
                 fg='#2c3e50',
                 justify='center').pack(expand=True)

        # ===== FOOTER =====
        footer_frame = tk.Frame(self.main_frame, bg='white')
        footer_frame.pack(fill='x', pady=(10, 15))

        # Thông tin thuật toán
        algo_font = font.Font(family="Arial", size=9)
        tk.Label(footer_frame,
                 text=f"Thuật toán Hồ Ngọc Đức | Cập nhật: {now.strftime('%H:%M:%S')}",
                 font=algo_font,
                 bg='white',
                 fg='#95a5a6').pack()

        # ===== CẬP NHẬT TỰ ĐỘNG =====
        self.root.after(1000, self.update_time)

    def get_lunar_hour_info(self, hour):
        """Lấy thông tin giờ âm lịch"""
        lunar_hours = [
            {"name": "Tý", "time": "23-1", "element": "Thủy"},
            {"name": "Sửu", "time": "1-3", "element": "Thổ"},
            {"name": "Dần", "time": "3-5", "element": "Mộc"},
            {"name": "Mão", "time": "5-7", "element": "Mộc"},
            {"name": "Thìn", "time": "7-9", "element": "Thổ"},
            {"name": "Tỵ", "time": "9-11", "element": "Hỏa"},
            {"name": "Ngọ", "time": "11-13", "element": "Hỏa"},
            {"name": "Mùi", "time": "13-15", "element": "Thổ"},
            {"name": "Thân", "time": "15-17", "element": "Kim"},
            {"name": "Dậu", "time": "17-19", "element": "Kim"},
            {"name": "Tuất", "time": "19-21", "element": "Thổ"},
            {"name": "Hợi", "time": "21-23", "element": "Thủy"}
        ]

        index = ((hour + 1) // 2) % 12
        return lunar_hours[index]

    def is_lucky_day(self, lunar_day, lunar_month):
        """Kiểm tra ngày hoàng đạo (đơn giản hóa)"""
        # Một số ngày được coi là tốt theo dân gian
        lucky_days = [1, 3, 4, 7, 8, 9, 11, 13, 14, 16, 17, 19, 21, 23, 25, 27, 29]
        return lunar_day in lucky_days

    def get_lunar_date_info(self, solar_date):
        """Lấy thông tin âm lịch đầy đủ"""
        try:
            lunar = LunarDate(solar_date.day, solar_date.month, solar_date.year)

            # Lấy can chi
            year_can, year_chi = lunar.getCanChiYear(lunar.lunarYear)
            month_can, month_chi = lunar.getCanChiMonth(lunar.lunarYear, lunar.lunarMonth)
            day_can, day_chi = lunar.getCanChiDay(lunar.jd)

            # Tên tháng âm
            month_names = ["", "Giêng", "Hai", "Ba", "Tư", "Năm",
                           "Sáu", "Bảy", "Tám", "Chín", "Mười", "Một", "Chạp"]

            # Tạo chuỗi thông tin
            leap_text = " (nhuận)" if lunar.lunarLeap else ""
            info = f"Năm {year_can} {year_chi}\n"
            info += f"Tháng {month_can} {month_chi} ({month_names[lunar.lunarMonth]}{leap_text})\n"
            info += f"Ngày {day_can} {day_chi}"

            return info

        except Exception as e:
            return f"Lỗi tính âm lịch: {e}"

    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()


# ================================
# HÀM MAIN VÀ THIẾT LẬP
# ================================

def main():
    # Tạo cửa sổ chính
    root = tk.Tk()

    # Thiết lập kích thước và vị trí
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 500
    window_height = 700
    position_right = screen_width - window_width - 50
    position_top = 50

    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    root.resizable(False, False)

    # Thêm phím tắt
    def refresh(event=None):
        print("Đang làm mới dữ liệu...")
        app.update_time()

    def quit_app(event=None):
        print("Thoát chương trình...")
        root.quit()

    root.bind('<F5>', refresh)
    root.bind('<r>', refresh)
    root.bind('<Control-q>', quit_app)
    root.bind('<Control-Q>', quit_app)
    root.bind('<Escape>', quit_app)

    # Tạo ứng dụng
    app = LunarCalendarApp(root)

    # Thông tin khởi động
    print("=" * 60)
    print("LỊCH ÂM DƯƠNG VIỆT NAM - Thuật toán Hồ Ngọc Đức")
    print("=" * 60)
    print("Phím tắt:")
    print("  F5 hoặc R      : Làm mới dữ liệu")
    print("  Ctrl+Q hoặc Esc: Thoát chương trình")
    print("=" * 60)

    # Chạy ứng dụng
    app.run()


if __name__ == "__main__":
    main()