import datetime

class PricingEngine:
    def __init__(self):
        # الأنظمة المحدثة بناءً على الفرق بين الستاندرد والسرايا
        self.systems = {
            "ألوبكو ستاندرد (اقتصادي)": {"price_m2": 320, "hardware": "Standard Local"},
            "ألوبكو سرايا (100mm)": {"price_m2": 475, "hardware": "Lavaal (Italy)"},
            "رويال رويال (Premium)": {"price_m2": 780, "hardware": "Lavaal (Italy)"},
            "شوكو ألماني (Schuco)": {"price_m2": 1450, "hardware": "Schuco Original"},
            "واجهات استركشر (SG50)": {"price_m2": 440, "hardware": "Hilti / Wacker"}
        }
        
        self.glass_options = {
            "Double Glazed (24mm)": 150,
            "Single Glass": 0,
            "Reflective / Grey": 50
        }

    def calculate_smart_price(self, width, height, system_name, glass_name, quantity):
        area_per_unit = (width / 100) * (height / 100)
        system_data = self.systems.get(system_name, self.systems["ألوبكو ستاندرد (اقتصادي)"])
        
        price_m2_base = system_data["price_m2"] + self.glass_options.get(glass_name, 0)
        
        unit_price_net = area_per_unit * price_m2_base
        total_net = unit_price_net * quantity
        
        vat = total_net * 0.15
        grand_total = total_net + vat
        
        return {
            "price_m2": price_m2_base,
            "hardware": system_data["hardware"],
            "unit_price_with_vat": round(unit_price_net * 1.15, 2),
            "total_with_vat": round(grand_total, 2)
        }

    def get_validity_dates(self, days=21):
        today = datetime.date.today()
        expiry = today + datetime.timedelta(days=days)
        return today.strftime("%Y-%m-%d"), expiry.strftime("%Y-%m-%d")
