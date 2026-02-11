# تأكد أن هذا الملف اسمه engine.py
class PricingEngine:
    def __init__(self):
        # أسعار تقريبية (يمكنك تعديلها بناءً على سعر السوق اليوم)
        self.materials = {
            "سرايا": 650,    # سعر المتر المربع
            "جامبو": 850,
            "عادي": 450
        }
        self.glass_types = {
            "سنجل": 100,
            "دبل": 250,
            "استركشر": 400
        }

    def calculate_base_price(self, width, height, material, glass):
        # التحويل من سم إلى متر مربع
        area = (width / 100) * (height / 100) 
        
        # جلب التكلفة مع وضع قيمة افتراضية إذا لم يوجد النوع
        material_cost = self.materials.get(material, 450)
        glass_cost = self.glass_types.get(glass, 100)
        
        total = area * (material_cost + glass_cost)
        return round(total, 2)