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

    @staticmethod
    def getCanChiHour(jd, hour):
        """Tính can chi của giờ"""
        CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

        # Tính chi giờ
        chi_index = ((hour + 1) // 2) % 12

        # Tính can ngày từ jd
        can_day_index = (int(jd) + 9) % 10

        # Tính can giờ Tý theo can ngày
        can_gio_ty_index = {
            0: 0,  # Giáp -> Giáp
            5: 0,  # Kỷ  -> Giáp
            1: 2,  # Ất  -> Bính
            6: 2,  # Canh-> Bính
            2: 4,  # Bính-> Mậu
            7: 4,  # Tân -> Mậu
            3: 6,  # Đinh-> Canh
            8: 6,  # Nhâm-> Canh
            4: 8,  # Mậu -> Nhâm
            9: 8  # Quý -> Nhâm
        }.get(can_day_index, 0)

        can_index = (can_gio_ty_index + chi_index) % 10

        return CAN[can_index], CHI[chi_index]

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
    def getHoangDaoHours(self):
        """Trả về danh sách 6 giờ Hoàng Đạo theo ngày"""
        chi_day = self.getCanChiDay(self.jd)[1]

        table = {
            "Tý":   ["Tý","Sửu","Mão","Ngọ","Thân","Dậu"],
            "Ngọ":  ["Tý","Sửu","Mão","Ngọ","Thân","Dậu"],

            "Sửu":  ["Dần","Mão","Tỵ","Thân","Tuất","Hợi"],
            "Mùi":  ["Dần","Mão","Tỵ","Thân","Tuất","Hợi"],

            "Dần":  ["Tý","Sửu","Thìn","Tỵ","Mùi","Tuất"],
            "Thân": ["Tý","Sửu","Thìn","Tỵ","Mùi","Tuất"],

            "Mão":  ["Tý","Dần","Mão","Ngọ","Mùi","Dậu"],
            "Dậu":  ["Tý","Dần","Mão","Ngọ","Mùi","Dậu"],

            "Thìn": ["Dần","Thìn","Tỵ","Thân","Dậu","Hợi"],
            "Tuất": ["Dần","Thìn","Tỵ","Thân","Dậu","Hợi"],

            "Tỵ":   ["Sửu","Thìn","Ngọ","Mùi","Tuất","Hợi"],
            "Hợi":  ["Sửu","Thìn","Ngọ","Mùi","Tuất","Hợi"],
        }

        return table.get(chi_day, [])

    def getDayType(self):
        """
        Xác định loại ngày theo tháng âm + chi ngày
        Trả về: 'hoang_dao' | 'hac_dao' | 'thuong'
        """

        chi_day = self.getCanChiDay(self.jd)[1]
        month = self.lunarMonth

        table = {
            (1, 7): {
                "hoang_dao": ["Tý", "Sửu", "Tỵ", "Mùi"],
                "hac_dao": ["Ngọ", "Mão", "Hợi", "Dậu"],
            },
            (2, 8): {
                "hoang_dao": ["Dần", "Mão", "Mùi", "Dậu"],
                "hac_dao": ["Thân", "Tý", "Sửu", "Hợi"],
            },
            (3, 9): {
                "hoang_dao": ["Thìn", "Tỵ", "Dậu", "Hợi"],
                "hac_dao": ["Tuất", "Mùi", "Sửu", "Hợi"],
            },
            (4, 10): {
                "hoang_dao": ["Ngọ", "Mùi", "Sửu", "Dậu"],
                "hac_dao": ["Tý", "Dậu", "Tỵ", "Mão"],
            },
            (5, 11): {
                "hoang_dao": ["Sửu", "Mão", "Thân", "Dậu"],
                "hac_dao": ["Dần", "Hợi", "Mùi", "Tỵ"],
            },
            (6, 12): {
                "hoang_dao": ["Mão", "Tỵ", "Tuất", "Hợi"],
                "hac_dao": ["Thìn", "Sửu", "Dậu", "Mùi"],
            },
        }

        for months, rules in table.items():
            if month in months:
                if chi_day in rules["hoang_dao"]:
                    return "hoang_dao"
                elif chi_day in rules["hac_dao"]:
                    return "hac_dao"
                else:
                    return "thuong"

        return "thuong"

