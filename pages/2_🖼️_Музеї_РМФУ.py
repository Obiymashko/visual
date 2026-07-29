import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

st.set_page_config(page_title="Дашборд: РМФУ", layout="wide")
plot_config = {'displayModeBar': True, 'toImageButtonOptions': {'format': 'png', 'filename': 'chart', 'height': 720, 'width': 1280, 'scale': 3}}

st.title("❖ Моніторинг Реєстру Музейного Фонду України (РМФУ)")
st.markdown("Комплексний аналіз наповнення та підписання музейних фондів по областях та музеях.")

# --- АВТОМАТИЧНЕ ЗАВАНТАЖЕННЯ ФАЙЛУ ---
current_dir = os.getcwd()
file_name = "РМФУ ВНЕСЕНО ПО ОБЛАСТЯХ.xlsx"
file_path = os.path.join(current_dir, file_name)

if not os.path.exists(file_path):
    st.error(f"❌ Файл `{file_name}` не знайдено у папці проєкту! Переконайтеся, що він лежить поруч з `app.py`.")
    st.stop()

@st.cache_data
def load_rmfu_data(path):
    xls = pd.ExcelFile(path)
    all_mus, reg_sum = [], []
    
    for sheet in xls.sheet_names:
        df_sheet = pd.read_excel(path, sheet_name=sheet)
        m_df = df_sheet[~df_sheet['ЄДРПОУ'].astype(str).str.upper().str.contains('ВСЬОГО', na=False)].copy()
        r_name = sheet.title() + (' обл.' if 'КИЇВ' not in sheet.upper() else '')
        
        m_df['Регіон'] = r_name
        for col in ['ВСЬОГО ПРЕДМЕТІВ', 'ВНЕСЕНО', 'ПОТРІБНО ВНЕСТИ', 'ОСНОВНИЙ ФОНД (ПІДПИСАНО)', 'ОСНОВНИЙ ФОНД (ВНЕСЕНО)', 'СПЕЦФОНД (ПІДПИСАНО)', 'СПЕЦФОНД (ВНЕСЕНО)']:
            m_df[col] = pd.to_numeric(m_df[col], errors='coerce').fillna(0)
            
        m_df['Прогрес (%)'] = np.where(m_df['ВСЬОГО ПРЕДМЕТІВ'] > 0, (m_df['ВНЕСЕНО'] / m_df['ВСЬОГО ПРЕДМЕТІВ']) * 100, 0).round(1)
        all_mus.append(m_df)
        
        reg_items, reg_vneseno, reg_potribno = m_df['ВСЬОГО ПРЕДМЕТІВ'].sum(), m_df['ВНЕСЕНО'].sum(), m_df['ПОТРІБНО ВНЕСТИ'].sum()
        reg_perc = (reg_vneseno / reg_items * 100) if reg_items > 0 else 0
        
        reg_sum.append({
            'Регіон': r_name, 'Кількість музеїв': len(m_df), 'Всього предметів': int(reg_items), 'Внесено предметів': int(reg_vneseno),
            'Потрібно внести': int(reg_potribno), 'Прогрес (%)': round(reg_perc, 1),
            'Основний фонд (підписано)': int(m_df['ОСНОВНИЙ ФОНД (ПІДПИСАНО)'].sum()), 'Основний фонд (внесено)': int(m_df['ОСНОВНИЙ ФОНД (ВНЕСЕНО)'].sum()),
            'Спецфонд (підписано)': int(m_df['СПЕЦФОНД (ПІДПИСАНО)'].sum()), 'Спецфонд (внесено)': int(m_df['СПЕЦФОНД (ВНЕСЕНО)'].sum())
        })
        
    return pd.DataFrame(reg_sum), pd.concat(all_mus, ignore_index=True)

df_summary, df_museums = load_rmfu_data(file_path)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🏢 Всього музеїв", f"{int(df_summary['Кількість музеїв'].sum()):,}")
c2.metric("📦 Всього предметів", f"{int(df_summary['Всього предметів'].sum()):,}")
c3.metric("☑ Внесено предметів", f"{int(df_summary['Внесено предметів'].sum()):,}")
c4.metric("✍ Основний фонд (підписано)", f"{int(df_summary['Основний фонд (підписано)'].sum()):,}")
c5.metric("✍ Спецфонд (підписано)", f"{int(df_summary['Спецфонд (підписано)'].sum()):,}")
st.divider()

tab1, tab2 = st.tabs(["📊 Зведення по областях", "🏛️ Помузейна деталізація"])

with tab1:
    st.subheader("▤ Зведена таблиця по регіонах України")
    st.dataframe(df_summary.sort_values(by='Внесено предметів', ascending=False), use_container_width=True, hide_index=True,
                 column_config={"Прогрес (%)": st.column_config.ProgressColumn("Прогрес (%)", format="%.1f%%", min_value=0, max_value=100 if df_summary['Прогрес (%)'].max() <= 100 else int(df_summary['Прогрес (%)'].max()))})
    st.divider()
    
    cg1, cg2 = st.columns(2)
    with cg1:
        st.subheader("★ Топ областей за кількістю внесених предметів")
        df_top = df_summary.sort_values(by='Внесено предметів', ascending=True)
        fig_top = px.bar(df_top, x='Внесено предметів', y='Регіон', orientation='h', text=df_top['Внесено предметів'].apply(lambda x: f"{x:,}"), color='Внесено предметів', color_continuous_scale='Blues', height=700)
        fig_top.update_traces(textposition='outside')
        fig_top.update_layout(template="plotly_white", margin=dict(l=0, r=50, t=30, b=0), coloraxis_showscale=False)
        st.plotly_chart(fig_top, use_container_width=True, config=plot_config)
        
    with cg2:
        st.subheader("◫ Співвідношення: Основний vs Спецфонд (внесено)")
        df_f = df_summary.sort_values(by='Основний фонд (внесено)', ascending=False)
        fig_fonds = go.Figure(data=[
            go.Bar(x=df_f['Регіон'], y=df_f['Основний фонд (внесено)'], name='Основний фонд', marker_color='#3b82f6'),
            go.Bar(x=df_f['Регіон'], y=df_f['Спецфонд (внесено)'], name='Спецфонд', marker_color='#10b981')
        ])
        fig_fonds.update_layout(barmode='stack', template="plotly_white", height=700, xaxis_tickangle=-45, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_fonds, use_container_width=True, config=plot_config)

with tab2:
    st.subheader("🔍 Пошук та детальний аналіз по музеях")
    cf1, cf2 = st.columns([1, 2])
    reg = cf1.selectbox("Фільтр по області:", ["Усі області"] + list(df_summary['Регіон'].unique()))
    q = cf2.text_input("Пошук музею (за назвою або ЄДРПОУ):", "").lower().strip()
    
    df_filt = df_museums.copy()
    if reg != "Усі області": df_filt = df_filt[df_filt['Регіон'] == reg]
    if q: df_filt = df_filt[df_filt['НАЗВА МУЗЕЮ'].astype(str).str.lower().str.contains(q) | df_filt['ЄДРПОУ'].astype(str).str.contains(q)]
        
    st.markdown(f"**Знайдено музеїв: {len(df_filt)}**")
    st.dataframe(df_filt[['Регіон', 'ЄДРПОУ', 'НАЗВА МУЗЕЮ', 'ВСЬОГО ПРЕДМЕТІВ', 'ВНЕСЕНО', 'ПОТРІБНО ВНЕСТИ', 'Прогрес (%)', 'ОСНОВНИЙ ФОНД (ПІДПИСАНО)', 'ОСНОВНИЙ ФОНД (ВНЕСЕНО)', 'СПЕЦФОНД (ПІДПИСАНО)', 'СПЕЦФОНД (ВНЕСЕНО)']], use_container_width=True, hide_index=True)