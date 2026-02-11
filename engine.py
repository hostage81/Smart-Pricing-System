import datetime

class PricingEngine:
    def __init__(self):
        # أنظمة مصنع عالم المسكن المحدثة 2026
        self.systems = {
            "Alupco (Standard)": {"price_m2": 550},
            "Saraya (Royal)": {"price_m2": 780},
            "Schuco (Premium)": {"price_m2": 1450},
            "Structure Glass": {"price_m2": 950}
        }
        
        self.glass_options = {
            "Double Glass (24mm)": 150,
            "Clear Single": 0,
            "Reflective Glass": 50
        }

    def calculate_smart_price(self, width, height, system_name, glass_name, quantity):
        # المساحة بالمتر المربع للشباك الواحد
        area_per_unit = (width / 100) * (height / 100)
        
        system_data = self.systems.get(system_name, self.systems["Alupco (Standard)"])
        base_rate = system_data["price_m2"]
        glass_extra = self.glass_options.get(glass_name, 0)
        
        # سعر الوحدة قبل الضريبة
        unit_price_net = area_per_unit * (base_rate + glass_extra)
        
        # السعر الإجمالي للكمية (قبل الضريبة)
        total_net = unit_price_net * quantity
        
        # الضريبة 15%
        vat = total_net * 0.15
        grand_total = total_net + vat
        
        return {
            "area_unit": round(area_per_unit, 2),
            "unit_price_with_vat": round(unit_price_net * 1.15, 2),
            "total_with_vat": round(grand_total, 2)
        }

    def get_validity_dates(self, days=7):
        # حساب تاريخ اليوم وتاريخ انتهاء العرض
        today = datetime.date.today()
        expiry = today + datetime.timedelta(days=days)
        return today.strftime("%Y-%m-%d"), expiry.strftime("%Y-%m-%d")
