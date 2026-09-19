import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="لوحة تحكم عمارة ورثة السيالة", layout="wide")
st.title("🏢 لوحة تحكم عمارة ورثة السيالة - صيف 2026")

# --- 1. Load Data ---
@st.cache_data
def load_data():
    # Arrears Data (المحلات الغير خالصة)
    arrears = pd.DataFrame({
        "رقم المحل": ["A2", "A6", "A9", "A11", "B1", "B3", "B5", "B6", "B7", "B9", "M2", "M3", "M4", "M7", "M10"],
        "الأشهر غير الخالصة": ["أوت", "ماي، جوان، جويلية، أوت", "جويلية، أوت", "جويلية", "أوت", "جويلية", "جوان، جويلية، أوت", "جوان، جويلية، أوت", "أوت", "ماي، جوان، جويلية، أوت", "جويلية، أوت", "أفريل، ماي، جوان، جويلية، أوت", "أوت", "جويلية، أوت", "أوت"],
        "عدد الأشهر": [1, 4, 2, 1, 1, 1, 3, 3, 1, 4, 2, 5, 1, 2, 1],
        "قيمة الكراء المرجعية": [290, 315, 975, 270, 273, 370, 345, 430, 370, 390, 330, 345, 250, 340, 399]
    })
    arrears["جملة الدين"] = arrears["عدد الأشهر"] * arrears["قيمة الكراء المرجعية"]

    # Monthly Summary (الملخص الشهري)
    months = pd.DataFrame({
        "الشهر": ["جوان 2026", "جويلية 2026", "أوت 2026"],
        "المداخيل": [8972.500, 7428.300, 7646.200],
        "المصاريف": [6486.700, 6090.600, 3796.000],
        "الباقي": [2485.800, 1337.700, 3850.200]
    })
    return arrears, months

arrears_df, months_df = load_data()

# --- 2. Monthly Summary Section ---
st.header("📊 الملخص الشهري (جوان - أوت 2026)")
col1, col2, col3 = st.columns(3)
col1.metric("إجمالي المداخيل", f"{months_df['المداخيل'].sum():,.3f}")
col2.metric("إجمالي المصاريف", f"{months_df['المصاريف'].sum():,.3f}")
col3.metric("الرصيد الحالي (أوت)", f"{months_df['الباقي'].iloc[-1]:,.3f}")

# Visualizing Income vs Expenses
fig_trend = px.bar(
    months_df, x="الشهر", y=["المداخيل", "المصاريف"], 
    barmode="group", title="مقارنة المداخيل والمصاريف حسب الشهر",
    labels={"value": "المبلغ", "variable": "النوع"}
)
st.plotly_chart(fig_trend, use_container_width=True)

st.dataframe(months_df, use_container_width=True, hide_index=True)

st.divider()

# --- 3. Arrears & Debts Section ---
st.header("⚠️ المحلات الغير خالصة (الديون حتى أوت 2026)")
col_a, col_b = st.columns([2, 1])

with col_a:
    st.dataframe(
        arrears_df[["رقم المحل", "الأشهر غير الخالصة", "عدد الأشهر", "قيمة الكراء المرجعية", "جملة الدين"]], 
        use_container_width=True, hide_index=True
    )

with col_b:
    st.metric("إجمالي الديون المستحقة", f"{arrears_df['جملة الدين'].sum():,.3f}")
    
    # Debt distribution visualization
    fig_debt = px.pie(
        arrears_df, values='جملة الدين', names='رقم المحل', 
        title='توزيع الديون حسب المحل', hole=0.4
    )
    st.plotly_chart(fig_debt, use_container_width=True)