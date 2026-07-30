import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

st.set_page_config(page_title="Дашборд: ЄПам'ятка", page_icon=":material/account_balance:", layout="wide")

# CSS для метрик
st.markdown("""
<style>
[data-testid="stMetricLabel"] p {
    white-space: normal !important;
    word-wrap: break-word !important;
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)

plot_config = {'displayModeBar': True, 'toImageButtonOptions': {'format': 'png', 'filename': 'chart', 'height': 720, 'width': 1280, 'scale': 3}}

# --- ШАПКА ТА ІНФОРМАЦІЯ ---
st.title(":material/account_balance: Моніторинг внесення нерухомих пам'яток до ЄПам'ятки")
st.markdown("Аналітика наповнення Реєстру та карток в системі ЄПам'ятка.")
st.caption(":material/calendar_today: **Дані актуальні на 27.07.2026**")

# Гарний блок з довідковою інформацією у вигляді ВЕЛИКИХ МЕТРИК
with st.container(border=True):
    st.markdown("**:material/info: Довідкова інформація щодо впровадження системи «ЄПам'ятка»:**")
    
    info_col1, info_col2, info_col3, info_col4, info_col5 = st.columns(5)
    
    info_col1.metric(":material/museum: Всього об'єктів на обліку", "144,643")
    info_col2.metric(":material/cloud_upload: Внесено до системи", "105,987", "72% від загальної кількості", delta_color="normal")
    
    # ТУТ ДОДАНО ПРИМІТКУ ЧЕРЕЗ ПАРАМЕТР help
    info_col3.metric(
        ":material/how_to_reg: Внесено до Реєстру", 
        "30,192", 
        help="Разом з адресами, верифіковані та підтверджені спільно з Мінрегіоном"
    )
    
    info_col4.metric(":material/verified: Повністю верифіковано", "49")
    info_col5.metric(":material/group: Підключено користувачів", "139")

st.info("Включає кількість об'єктів національного значення в реєстрі та Пам’ятка національного значення – взято на державний облік відповідно до законодавства, що діяло до набрання чинності Закону України «Про охорону культурної спадщини»", icon="ℹ️")

# --- АВТОМАТИЧНЕ ЗАВАНТАЖЕННЯ ФАЙЛУ ---
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir) if os.path.basename(current_dir) == 'pages' else current_dir
file_name = "свод нерухома обл 2026 (1).xlsx"
file_path = os.path.join(parent_dir, file_name)

if not os.path.exists(file_path):
    st.error(f"❌ Файл `{file_name}` не знайдено! Переконайтеся, що він лежить у головній папці поруч із `app.py`.")
    st.stop()

xls = pd.ExcelFile(file_path)
selected_sheet = xls.sheet_names[0]

# Точні повні назви колонок БЕЗ переносів
col_reestr = "Кількість об'єктів національного значення в Реєстрі (на сайті Мінкульту)"
col_cards = "Кількість карток національного значення в ЄПам'ятка"
col_draft_all = "Кількість чернеток всього"
col_draft_nac = "Кількість чернеток національного значення"
col_perc = "Загальний прогрес (відсоток карток від об'єктів в реєстрі)"

@st.cache_data
def load_data(path, sheet):
    df_raw = pd.read_excel(path, sheet_name=sheet)
    c_reg, c_reestr, c_drafts_all, c_drafts_nac, c_cards = -1, -1, -1, -1, -1
    
    for i, col in enumerate(df_raw.columns):
        text = str(col).lower()
        for r in range(min(3, len(df_raw))): 
            text += " " + str(df_raw.iloc[r, i]).lower()
            
        if ("регіон" in text or "область" in text) and c_reg == -1: 
            c_reg = i
        elif ("реєстр" in text or "мінкульт" in text) and "відсоток" not in text and "карток" not in text and c_reestr == -1: 
            c_reestr = i
        elif "чернеток" in text and "всього" in text: 
            c_drafts_all = i
        elif "чернеток" in text and ("національного" in text or "нац" in text): 
            c_drafts_nac = i
        elif "карток" in text and "національного" in text and "відсоток" not in text: 
            c_cards = i
            
    if c_reg == -1: c_reg = 1
    if c_reestr == -1: c_reestr = 2
    if c_cards == -1: c_cards = len(df_raw.columns) - 1
        
    start_row = next((r for r in range(min(10, len(df_raw))) if "вінницька" in str(df_raw.iloc[r, c_reg]).lower()), 1)
    data = df_raw.iloc[start_row:].copy()
    
    df = pd.DataFrame({
        'Регіон': data.iloc[:, c_reg].astype(str),
        col_reestr: pd.to_numeric(data.iloc[:, c_reestr], errors='coerce').fillna(0).astype(int),
        col_cards: pd.to_numeric(data.iloc[:, c_cards], errors='coerce').fillna(0).astype(int)
    })
    
    if c_drafts_all != -1: 
        df[col_draft_all] = pd.to_numeric(data.iloc[:, c_drafts_all], errors='coerce').fillna(0).astype(int)
    if c_drafts_nac != -1: 
        df[col_draft_nac] = pd.to_numeric(data.iloc[:, c_drafts_nac], errors='coerce').fillna(0).astype(int)
        
    end_idx = next((i for i, val in enumerate(df['Регіон']) if str(val).lower().strip().startswith(('всього', 'разом'))), len(df))
    df = df.iloc[:end_idx].dropna(subset=['Регіон'])
    df = df[(df['Регіон'].str.lower() != 'nan') & (df['Регіон'].str.len() > 3)]
    
    df[col_perc] = np.where(df[col_reestr] > 0, (df[col_cards] / df[col_reestr]) * 100, 0)
    
    cols = ['Регіон', col_perc, col_reestr, col_cards]
    if col_draft_all in df.columns: cols.append(col_draft_all)
    if col_draft_nac in df.columns: cols.append(col_draft_nac)
    
    return df[cols].sort_values(by=col_perc, ascending=False)

df = load_data(file_path, selected_sheet)
if df.empty:
    st.warning("⚠️ Не знайдено даних.")
    st.stop()
    
tot_reestr, tot_cards = int(df[col_reestr].sum()), int(df[col_cards].sum())
avg_perc = (tot_cards / tot_reestr * 100) if tot_reestr > 0 else 0

# --- ГОЛОВНІ ДИНАМІЧНІ МЕТРИКИ ---
cols_metric = st.columns(3 + sum(1 for c in [col_draft_all, col_draft_nac] if c in df.columns))
idx = 0

if col_draft_all in df.columns:
    cols_metric[idx].metric(f":material/draft: {col_draft_all}", f"{int(df[col_draft_all].sum()):,}"); idx += 1
cols_metric[idx].metric(f":material/trending_up: {col_perc}", f"{avg_perc:.1f}%"); idx += 1
cols_metric[idx].metric(f":material/list_alt: {col_reestr}", f"{tot_reestr:,}"); idx += 1
cols_metric[idx].metric(f":material/check_circle: {col_cards}", f"{tot_cards:,}"); idx += 1
if col_draft_nac in df.columns:
    cols_metric[idx].metric(f":material/draft: {col_draft_nac}", f"{int(df[col_draft_nac].sum()):,}")

st.divider()

# --- ГРАФІКИ ---
st.subheader(":material/leaderboard: Рейтинг областей за відсотком виконання")
fig_bar = px.bar(
    df.sort_values(by=col_perc, ascending=True), 
    x=col_perc, y='Регіон', orientation='h', 
    text=df.sort_values(by=col_perc, ascending=True)[col_perc].apply(lambda x: f"{x:.1f}%"), 
    color=col_perc, color_continuous_scale='RdYlGn', height=750
)
fig_bar.update_traces(textposition='outside')
fig_bar.update_layout(template="plotly_white", margin=dict(l=0, r=50, t=30, b=0), xaxis_title="% Внесено карток", yaxis_title="", coloraxis_showscale=False)
st.plotly_chart(fig_bar, use_container_width=True, config=plot_config)

st.divider()

st.subheader(":material/stacked_bar_chart: Порівняння: Реєстр Мінкульту vs Картки в ЄПам'ятка")
df_sorted = df.sort_values(by=col_reestr, ascending=False)
fig_comp = go.Figure(data=[
    go.Bar(x=df_sorted['Регіон'], y=df_sorted[col_reestr], name='Об\'єкти в Реєстрі', marker_color='#d1d5db'),
    go.Bar(x=df_sorted['Регіон'], y=df_sorted[col_cards], name='Внесено в ЄПам\'ятка', marker_color='#3b82f6')
])
fig_comp.update_layout(barmode='group', template="plotly_white", height=500, xaxis_tickangle=-45, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig_comp, use_container_width=True, config=plot_config)

st.divider()

# --- ДЕТАЛЬНА ТАБЛИЦЯ ---
st.subheader(":material/table: Детальна таблиця")
col_cfg = {
    "Регіон": st.column_config.TextColumn("Регіон", width="medium"),
    col_perc: st.column_config.ProgressColumn(
        col_perc, 
        format="%.1f%%", 
        min_value=0, 
        max_value=100 if df[col_perc].max() <= 100 else int(df[col_perc].max()),
        width="large"
    ),
    col_reestr: st.column_config.NumberColumn(col_reestr, width="large"),
    col_cards: st.column_config.NumberColumn(col_cards, width="large")
}
if col_draft_all in df.columns:
    col_cfg[col_draft_all] = st.column_config.NumberColumn(col_draft_all, width="medium")
if col_draft_nac in df.columns:
    col_cfg[col_draft_nac] = st.column_config.NumberColumn(col_draft_nac, width="large")

st.dataframe(
    df, 
    use_container_width=True, 
    hide_index=True,
    column_config=col_cfg
)
