import streamlit as st
from engine import PricingEngine
import os
from dotenv import load_dotenv
from google import genai

# تحميل الإعدادات
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
engine = PricingEngine()

st.set_page_config(page_title="FBS - Smart Pricing", page_icon="🏗️")

st.title("🏗️ نظام FBS للتسعير الذكي")

# القائمة الجانبية للمدخلات
with st.sidebar:
    st.header("إعدادات الشباك")
    width = st.slider("العرض (سم)", 50, 300, 120)
    height = st.slider("الارتفاع (سم)", 50, 300, 140)
    material = st.selectbox("القطاع", ["سرايا", "جامبو", "عادي"])
    glass = st.selectbox("الزجاج", ["سنجل", "دبل", "استركشر"])

# الحساب التلقائي
price = engine.calculate_base_price(width, height, material, glass)

# عرض النتيجة بشكل جذاب
st.metric(label="السعر التقديري", value=f"{price} ريال")

# ميزة التميز: نصيحة Gemini
if st.button("الحصول على نصيحة الذكاء الاصطناعي"):
    with st.spinner("جاري تحليل البيانات..."):
        try:
            prompt = f"""
            بصفتك خبير في واجهات الألمنيوم، العميل طلب شباك بمقاس {width}x{height} 
            ونوع قطاع {material} وزجاج {glass}. 
            أعطني نصيحة فنية واحدة لهذا العميل بأسلوب بيع احترافي.
            """
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            st.markdown("### 🤖 نصيحة الخبير:")
            st.write(response.text)
        except Exception as e:
            st.warning("الذكاء الاصطناعي في استراحة قصيرة، ولكن السعر الحسابي دقيق 100%.")