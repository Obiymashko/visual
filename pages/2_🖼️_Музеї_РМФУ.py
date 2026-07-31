import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Дашборд: Музейний реєстр", layout="wide")

# Точне налаштування CSS: Montserrat для контенту та Plotly, нейтралізація текстових іконок
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap');

/* Глобальний Montserrat для контенту */
.main, .stMarkdown, .stTable, .stDataFrame, h1, h2, h3, h4, h5, h6, p, div, span {
    font-family: 'Montserrat', sans-serif !important;
}

/* Приховуємо вилазячий текст іконок Streamlit у сайдбарі та шапці */
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"],
[data-testid="stSidebarNavSeparator"] {
    font-size: 0px !important;
    visibility: hidden !important;
}

/* Системний шрифт для кнопок управління, щоб зберегти базові іконки */
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stExpandSidebarButton"] button,
button[data-testid="stHeaderIconButton"], 
[data-testid="stHeader"] * {
    font-family: Source Sans Pro, -apple-system, BlinkMacSystemFont, Roboto, sans-serif !important;
}

/* Назви пунктів меню в сайдбарі залишаємо Montserrat */
[data-testid="stSidebarNav"] span {
    font-family: 'Montserrat', sans-serif !important;
}

/* Montserrat для графіків Plotly */
.js-plotly-plot .plotly text,
.js-plotly-plot .plotly .hovertext,
.js-plotly-plot .plotly .gtitle,
.js-plotly-plot .plotly .xtitle,
.js-plotly-plot .plotly .ytitle {
    font-family: 'Montserrat', sans-serif !important;
}

/* Контейнер для лівого блоку */
.left-stat-block {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
}

/* Заголовок картки */
.stat-title {
    color: #8c92a4;
    font-weight: 600;
    font-size: 14px;
    margin-bottom: 6px;
    line-height: 1.3;
}

/* Великі числа */
.big-number {
    font-family: 'Montserrat', sans-serif !important;
    font-size: 3.5rem !important;
    font-weight: 900 !important;
    margin: 0px 0px 6px 0px !important;
    line-height: 1 !important;
}

/* Зелені підписи */
.green-tag {
    font-family: 'Montserrat', sans-serif !important;
    color: #00d26a;
    font-size: 13px;
    font-weight: 700;
    margin-top: 2px;
}

/* Підпункти списку */
.sub-list {
    font-family: 'Montserrat', sans-serif !important;
    font-size: 14px !important;
    opacity: 0.95 !important;
    line-height: 1.8 !important;
    margin: 0 !important;
    padding-left: 0px !important;
    list-style-type: none !important;
}
.sub-list li {
    position: relative;
    padding-left: 20px;
    margin-bottom: 4px;
}
.sub-list b {
    font-weight: 900 !important;
}

/* Кольорові маркери */
.color-dot {
    height: 10px;
    width: 10px;
    border-radius: 50%;
    display: inline-block;
    position: absolute;
    left: 0;
    top: 7px;
}
</style>
""",
    unsafe_allow_html=True,
)

plot_config = {
    "displayModeBar": False,
    "toImageButtonOptions": {
        "format": "png",
        "filename": "chart",
        "height": 720,
        "width": 1280,
        "scale": 3,
    },
}

def clean_chart_layout(fig, height=190):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=25, t=10, b=10),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font=dict(family="Montserrat, sans-serif"),
        hoverlabel=dict(font_family="Montserrat, sans-serif"),
    )
    fig.update_traces(textposition="inside")
    return fig

# --- ШАПКА ---
st.title("Музейний реєстр")

# =====================================================================
# 1. АВТОМАТИЧНЕ ЗАВАНТАЖЕННЯ ТА ОБРОБКА ДАНИХ (ПЕРЕД КАРТКАМИ)
# =====================================================================
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir) if os.path.basename(current_dir) == "pages" else current_dir
file_name = "РМФУ ВНЕСЕНО ПО ОБЛАСТЯХ.xlsx"
file_path = os.path.join(parent_dir, file_name)

if not os.path.exists(file_path):
    st.error(f"Не знайдено файл `{file_name}` у папці проєкту! Переконайтеся, що він лежить у головній папці поруч із `app.py`.")
    st.stop()

@st.cache_data
def load_rmfu_data(path):
    xls = pd.ExcelFile(path)
    all_mus, reg_sum = [], []

    for sheet in xls.sheet_names:
        df_sheet = pd.read_excel(path, sheet_name=sheet)
        m_df = df_sheet[~df_sheet["ЄДРПОУ"].astype(str).str.upper().str.contains("ВСЬОГО", na=False)].copy()
        r_name = sheet.title() + (" обл." if "КИЇВ" not in sheet.upper() else "")

        m_df["Регіон"] = r_name
        for col in [
            "ВСЬОГО ПРЕДМЕТІВ", "ВНЕСЕНО", "ПОТРІБНО ВНЕСТИ",
            "ОСНОВНИЙ ФОНД (ПІДПИСАНО)", "ОСНОВНИЙ ФОНД (ВНЕСЕНО)",
            "СПЕЦФОНД (ПІДПИСАНО)", "СПЕЦФОНД (ВНЕСЕНО)",
        ]:
            m_df[col] = pd.to_numeric(m_df[col], errors="coerce").fillna(0)

        m_df["Прогрес (%)"] = np.where(m_df["ВСЬОГО ПРЕДМЕТІВ"] > 0, (m_df["ВНЕСЕНО"] / m_df["ВСЬОГО ПРЕДМЕТІВ"]) * 100, 0).round(1)
        all_mus.append(m_df)

        reg_items = m_df["ВСЬОГО ПРЕДМЕТІВ"].sum()
        reg_vneseno = m_df["ВНЕСЕНО"].sum()
        reg_potribno = m_df["ПОТРІБНО ВНЕСТИ"].sum()
        reg_perc = (reg_vneseno / reg_items * 100) if reg_items > 0 else 0

        reg_sum.append({
            "Регіон": r_name,
            "Кількість музеїв": len(m_df),
            "Всього предметів": int(reg_items),
            "Внесено предметів": int(reg_vneseno),
            "Потрібно внести": int(reg_potribno),
            "Прогрес (%)": round(reg_perc, 1),
            "Основний фонд (підписано)": int(m_df["ОСНОВНИЙ ФОНД (ПІДПИСАНО)"].sum()),
            "Основний фонд (внесено)": int(m_df["ОСНОВНИЙ ФОНД (ВНЕСЕНО)"].sum()),
            "Спецфонд (підписано)": int(m_df["СПЕЦФОНД (ПІДПИСАНО)"].sum()),
            "Спецфонд (внесено)": int(m_df["СПЕЦФОНД (ВНЕСЕНО)"].sum()),
        })

    return pd.DataFrame(reg_sum), pd.concat(all_mus, ignore_index=True)

df_summary, df_museums = load_rmfu_data(file_path)

# Підготовка автоматичних змінних для карток
total_museums = int(df_summary['Кількість музеїв'].sum())
total_items = int(df_summary['Всього предметів'].sum())
total_vneseno = int(df_summary['Внесено предметів'].sum())
total_potribno = int(df_summary['Потрібно внести'].sum())

osn_vneseno = int(df_summary['Основний фонд (внесено)'].sum())
osn_pidpysano = int(df_summary['Основний фонд (підписано)'].sum())
spec_vneseno = int(df_summary['Спецфонд (внесено)'].sum())
spec_pidpysano = int(df_summary['Спецфонд (підписано)'].sum())

# Статуси музеїв по прогресу
mus_completed = len(df_museums[df_museums["Прогрес (%)"] >= 99.9])
mus_not_started = len(df_museums[df_museums["Прогрес (%)"] == 0])
mus_in_progress = total_museums - mus_completed - mus_not_started

perc_total = (total_vneseno / total_items * 100) if total_items > 0 else 0

# =====================================================================
# 2. АВТОМАТИЧНІ ДИНАМІЧНІ КАРТКИ ДАШБОРДУ
# =====================================================================

# --- КАРТКА 1: Загальний стан предметів ---
colors_items = ["#16A34A", "#F59E0B"] # Зелений, Оранжевий
with st.container(border=True):
    top_left1, top_mid1, top_right1 = st.columns([1.8, 2.0, 1.2], vertical_alignment="top")
    
    with top_left1:
        st.markdown(
            f"""
            <div class='left-stat-block'>
                <div class='stat-title'>Всього музейних предметів (за звітами)</div>
                <h1 class='big-number'>{total_items:,}</h1>
                <div class='green-tag'>↑ {perc_total:.1f}% загальний прогрес внесення</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_mid1:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors_items[0]};'></span>Внесено до реєстру: <b>{total_vneseno:,}</b></li>
                <li><span class='color-dot' style='background-color: {colors_items[1]};'></span>Залишилось внести: <b>{total_potribno:,}</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )
    with top_right1:
        fig1 = go.Figure(data=[go.Pie(labels=["Внесено", "Залишилось"], values=[total_vneseno, total_potribno], hole=0.55, marker_colors=colors_items, textinfo="percent", insidetextorientation="radial")])
        fig1 = clean_chart_layout(fig1)
        st.plotly_chart(fig1, use_container_width=True, config=plot_config)

# --- КАРТКА 2: Розподіл за фондами ---
colors_funds = ["#3b82f6", "#06b6d4"] # Синій, Блакитний
with st.container(border=True):
    top_left2, top_mid2, top_right2 = st.columns([1.8, 2.0, 1.2], vertical_alignment="top")
    
    with top_left2:
        st.markdown(
            f"""
            <div class='left-stat-block'>
                <div class='stat-title'>Внесено до системи</div>
                <h1 class='big-number'>{total_vneseno:,}</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_mid2:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors_funds[0]};'></span>Основний фонд (внесено): <b>{osn_vneseno:,}</b></li>
                <li><span class='color-dot' style='background-color: transparent; border: 2px solid {colors_funds[0]}; left: -2px; top: 5px;'></span>Основний фонд (підписано КЕП): <b>{osn_pidpysano:,}</b></li>
                <li><span class='color-dot' style='background-color: {colors_funds[1]};'></span>Спецфонд (внесено): <b>{spec_vneseno:,}</b></li>
                <li><span class='color-dot' style='background-color: transparent; border: 2px solid {colors_funds[1]}; left: -2px; top: 5px;'></span>Спецфонд (підписано КЕП): <b>{spec_pidpysano:,}</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )
    with top_right2:
        fig2 = go.Figure(data=[go.Pie(labels=["Основний фонд", "Спецфонд"], values=[osn_vneseno, spec_vneseno], hole=0.55, marker_colors=colors_funds, textinfo="percent", insidetextorientation="radial")])
        fig2 = clean_chart_layout(fig2)
        st.plotly_chart(fig2, use_container_width=True, config=plot_config)

# --- КАРТКА 3: Активність музеїв ---
colors_mus = ["#10b981", "#3b82f6", "#ef4444"] # Зелений, Синій, Червоний
with st.container(border=True):
    top_left3, top_mid3, top_right3 = st.columns([1.8, 2.0, 1.2], vertical_alignment="top")
    
    with top_left3:
        st.markdown(
            f"""
            <div class='left-stat-block'>
                <div class='stat-title'>Всього музейних установ у базі</div>
                <h1 class='big-number'>{total_museums:,}</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_mid3:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors_mus[0]};'></span>Завершили внесення (100%): <b>{mus_completed:,}</b></li>
                <li><span class='color-dot' style='background-color: {colors_mus[1]};'></span>В процесі внесення (1-99%): <b>{mus_in_progress:,}</b></li>
                <li><span class='color-dot' style='background-color: {colors_mus[2]};'></span>Ще не розпочали (0%): <b>{mus_not_started:,}</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )
    with top_right3:
        fig3 = go.Figure(data=[go.Pie(labels=["Завершили", "В процесі", "Не розпочали"], values=[mus_completed, mus_in_progress, mus_not_started], hole=0.55, marker_colors=colors_mus, textinfo="percent", insidetextorientation="radial")])
        fig3 = clean_chart_layout(fig3)
        st.plotly_chart(fig3, use_container_width=True, config=plot_config)

st.divider()

# =====================================================================
# 3. ТАБЛИЦІ ТА ГРАФІКИ ПО ОБЛАСТЯХ І МУЗЕЯХ
# =====================================================================
tab1, tab2 = st.tabs(["Зведення по областях", "Помузейна деталізація"])

with tab1:
    st.subheader("Зведена таблиця по регіонах України")
    st.dataframe(
        df_summary.sort_values(by="Внесено предметів", ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Прогрес (%)": st.column_config.ProgressColumn(
                "Прогрес (%)",
                format="%.1f%%",
                min_value=0,
                max_value=(100 if df_summary["Прогрес (%)"].max() <= 100 else int(df_summary["Прогрес (%)"].max())),
            )
        },
    )
    st.divider()

    cg1, cg2 = st.columns(2)
    with cg1:
        st.subheader("Топ областей за кількістю внесених предметів")
        df_top = df_summary.sort_values(by="Внесено предметів", ascending=True)
        fig_top = px.bar(
            df_top,
            x="Внесено предметів",
            y="Регіон",
            orientation="h",
            text=df_top["Внесено предметів"].apply(lambda x: f"{x:,}"),
            color="Внесено предметів",
            color_continuous_scale="Blues",
            height=700,
        )
        fig_top.update_traces(textposition="outside")
        fig_top.update_layout(
            template="plotly_white",
            margin=dict(l=0, r=50, t=30, b=0),
            coloraxis_showscale=False,
            font=dict(family="Montserrat, sans-serif"),
            hoverlabel=dict(font_family="Montserrat, sans-serif"),
        )
        st.plotly_chart(fig_top, use_container_width=True, config=plot_config)

    with cg2:
        st.subheader("Співвідношення: Основний vs Спецфонд (внесено)")
        df_f = df_summary.sort_values(by="Основний фонд (внесено)", ascending=False)
        fig_fonds = go.Figure(
            data=[
                go.Bar(
                    x=df_f["Регіон"],
                    y=df_f["Основний фонд (внесено)"],
                    name="Основний фонд",
                    marker_color="#3b82f6",
                ),
                go.Bar(
                    x=df_f["Регіон"],
                    y=df_f["Спецфонд (внесено)"],
                    name="Спецфонд",
                    marker_color="#10b981",
                ),
            ]
        )
        fig_fonds.update_layout(
            barmode="stack",
            template="plotly_white",
            height=700,
            xaxis_tickangle=-45,
            font=dict(family="Montserrat, sans-serif"),
            hoverlabel=dict(font_family="Montserrat, sans-serif"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_fonds, use_container_width=True, config=plot_config)

with tab2:
    st.subheader("Пошук та детальний аналіз по музеях")
    cf1, cf2 = st.columns([1, 2])
    reg = cf1.selectbox("Фільтр по області:", ["Усі області"] + list(df_summary["Регіон"].unique()))
    q = cf2.text_input("Пошук музею (за назвою або ЄДРПОУ):", "").lower().strip()

    df_filt = df_museums.copy()
    if reg != "Усі області":
        df_filt = df_filt[df_filt["Регіон"] == reg]
    if q:
        df_filt = df_filt[
            df_filt["НАЗВА МУЗЕЮ"].astype(str).str.lower().str.contains(q)
            | df_filt["ЄДРПОУ"].astype(str).str.contains(q)
        ]

    st.markdown(f"**Знайдено музеїв: {len(df_filt)}**")
    st.dataframe(
        df_filt[[
            "Регіон", "ЄДРПОУ", "НАЗВА МУЗЕЮ", "ВСЬОГО ПРЕДМЕТІВ", "ВНЕСЕНО",
            "ПОТРІБНО ВНЕСТИ", "Прогрес (%)", "ОСНОВНИЙ ФОНД (ПІДПИСАНО)",
            "ОСНОВНИЙ ФОНД (ВНЕСЕНО)", "СПЕЦФОНД (ПІДПИСАНО)", "СПЕЦФОНД (ВНЕСЕНО)",
        ]],
        use_container_width=True,
        hide_index=True,
    )
