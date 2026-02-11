import streamlit as st
import pandas as pd
from engine import PricingEngine
import urllib.parse

# 1. تهيئة الذاكرة
if 'quotation_list' not in st.session_state:
    st.session_state.quotation_list = []

engine = PricingEngine()

# 2. إعداد الصفحة (متوافقة تماماً مع الجوال)
st.set_page_config(page_title="مصنع عالم المسكن", layout="wide", page_icon="🏭")

# تنسيق مخصص للجوال
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #f1f3f6; }
    .stMetric { border: 2px solid #1a365d; background-color: #ffffff; border-radius: 10px; padding: 10px; }
    .main-title { color: #1a365d; font-size: 24px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية (Sidebar) - هنا تقع قوة التصميم للجوال
with st.sidebar:
    st.image("logo.png", use_container_width=True) # يمكنك استبداله برابط لوغو المصنع
    st.header("⚙️ مدخلات المشروع")
    
    unit_type = st.selectbox("نوع البند", ["شباك سحاب", "شباك مفصلي", "باب", "واجهة استركشر", "ثابت"])
    system = st.selectbox("النظام الإنشائي", list(engine.systems.keys()))
    
    col_w, col_h = st.columns(2)
    with col_w:
        width = st.number_input("العرض (سم)", min_value=10, value=120)
    with col_h:
        height = st.number_input("الارتفاع (سم)", min_value=10, value=140)
        
    glass = st.selectbox("نوع الزجاج", list(engine.glass_options.keys()))
    quantity = st.number_input("العدد (الكمية)", min_value=1, value=1)
    note = st.text_input("ملاحظات (اختياري)")

    if st.button("➕ إضافة البند للعرض"):
        res = engine.calculate_smart_price(width, height, system, glass, quantity)
        st.session_state.quotation_list.append({
            "النوع": unit_type,
            "النظام": system,
            "المقاس": f"{width}x{height}",
            "العدد": quantity,
            "سعر الوحدة": res['unit_price_with_vat'],
            "الإجمالي": res['total_with_vat'],
            "ملاحظات": note if note else "-"
        })
        st.success("تمت الإضافة!")
        st.rerun()

# 4. الشاشة الرئيسية (نتائج العرض)
st.markdown('<p class="main-title">🏭 نظام تسعير مصنع عالم المسكن للصناعة</p>', unsafe_allow_html=True)

today, expiry = engine.get_validity_dates(days=21) # صلاحية 21 يوم كما في ملفاتك
st.info(f"📅 تاريخ العرض: {today} | ⚠️ الصلاحية: {expiry}")

if st.session_state.quotation_list:
    df = pd.DataFrame(st.session_state.quotation_list)
    
    # عرض الجدول (يتحول لتمرير أفقي على الجوال تلقائياً)
    st.subheader("📋 تفاصيل كراسة المقاسات")
    st.dataframe(df, use_container_width=True)

    # الإجماليات
    grand_total = df["الإجمالي"].sum()
    st.write("---")
    st.metric("الإجمالي الكلي للمشروع (شامل الضريبة)", f"{grand_total:,.2f} ريال")

    # أزرار التواصل في الأسفل (كبيرة وسهلة للمس بالاصبع)
    phone = "966534765830"
    summary = f"*عرض سعر - عالم المسكن*\nتاريخ: {today}\n"
    for i, item in enumerate(st.session_state.quotation_list):
        summary += f"- {item['النوع']} {item['المقاس']} (عدد {item['العدد']})\n"
    summary += f"\n*المجموع: {grand_total:,.2f} ريال*"
    
    wa_url = f"https://wa.me/{phone}?text={urllib.parse.quote(summary)}"
    
    st.link_button("🟢 إرسال الكراسة عبر WhatsApp", wa_url, use_container_width=True)
    
    if st.button("🗑️ مسح القائمة والبدء من جديد", use_container_width=True):
        st.session_state.quotation_list = []
        st.rerun()
else:
    st.warning("أهلاً بك.. القائمة فارغة حالياً. استخدم القائمة الجانبية (على اليمين أو من زر السهم في أعلى اليسار بالجوال) لإضافة البنود.")

