import streamlit as st
import pandas as pd
from engine import PricingEngine
import urllib.parse
import os

if 'quotation_list' not in st.session_state:
    st.session_state.quotation_list = []

engine = PricingEngine()
st.set_page_config(page_title="مصنع عالم المسكن", layout="wide", page_icon="🏭")

# تنسيق الواجهة
st.markdown("""
    <style>
    .stMetric { border: 2px solid #1a365d; background-color: #ffffff; border-radius: 10px; padding: 10px; }
    .main-title { color: #1a365d; font-size: 26px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h2 style='text-align: center; color: #1a365d;'>عالم المسكن</h2>", unsafe_allow_html=True)
    
    st.header("⚙️ تفاصيل البند")
    
    unit_type = st.selectbox("نوع البند", ["شباك سحاب", "شباك مفصلي", "باب", "واجهة"])
    system = st.selectbox("النظام الإنشائي", list(engine.systems.keys()))
    
    # إضافة خيار اللون كما في الملفات (RAL)
    color = st.selectbox("لون الألمنيوم (RAL)", ["Black Matt 9005", "White 9016", "Grey 7016", "Special Color"])
    
    c_w, c_h = st.columns(2)
    with c_w: width = st.number_input("العرض (سم)", min_value=10, value=120)
    with c_h: height = st.number_input("الارتفاع (سم)", min_value=10, value=140)
        
    glass = st.selectbox("الزجاج", list(engine.glass_options.keys()))
    quantity = st.number_input("العدد", min_value=1, value=1)
    note = st.text_input("ملاحظات")

    if st.button("➕ إضافة للعرض"):
        res = engine.calculate_smart_price(width, height, system, glass, quantity)
        st.session_state.quotation_list.append({
            "النوع": unit_type,
            "النظام": system,
            "المقاس": f"{width}x{height}",
            "اللون": color,
            "سعر المتر": f"{res['price_m2']} ريال",
            "الإكسسوارات": res['hardware'],
            "العدد": quantity,
            "إجمالي البند": res['total_with_vat'],
            "ملاحظات": note if note else "-"
        })
        st.rerun()

st.markdown('<p class="main-title">🏭 نظام تسعير مصنع عالم المسكن للصناعة</p>', unsafe_allow_html=True)

today, expiry = engine.get_validity_dates(days=21)
st.info(f"📅 تاريخ العرض: {today} | ⚠️ صلاحية الأسعار: {expiry}")

if st.session_state.quotation_list:
    df = pd.DataFrame(st.session_state.quotation_list)
    st.subheader("📋 كراسة المقاسات التفصيلية")
    st.dataframe(df, use_container_width=True)

    grand_total = df["إجمالي البند"].sum()
    st.divider()
    st.metric("الإجمالي النهائي (شامل الضريبة 15%)", f"{grand_total:,.2f} ريال")

    # إرسال للواتساب بتفاصيل أكثر
    phone = "966534765830"
    summary = f"*عرض سعر - عالم المسكن*\nالصلاحية حتى: {expiry}\n\n"
    for i, item in enumerate(st.session_state.quotation_list):
        summary += f"{i+1}. {item['النوع']} ({item['النظام']}) | لون: {item['اللون']} | إجمالي: {item['إجمالي البند']} ريال\n"
    summary += f"\n*المجموع النهائي: {grand_total:,.2f} ريال*"
    
    wa_url = f"https://wa.me/{phone}?text={urllib.parse.quote(summary)}"
    st.link_button("🟢 إرسال الكراسة عبر WhatsApp", wa_url, use_container_width=True)
    
    if st.button("🗑️ مسح القائمة", use_container_width=True):
        st.session_state.quotation_list = []
        st.rerun()
else:
    st.info("أهلاً بك.. القائمة فارغة. استخدم القائمة الجانبية لإضافة البنود.")
