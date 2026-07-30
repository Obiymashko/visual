import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Дашборд: Музейний реєстр", layout="wide")

# Надійне налаштування Montserrat + ТАБУ на зламування іконки сайдбару
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap');

/* Глобальне застосування шрифту Montserrat для всього додатку */
html, body, [class*="css"], [class*="st-"], .stMarkdown, .stTable, div, span, p, h1, h2, h3, h4, h5, h6, li, button, input {
    font-family: 'Montserrat', sans-serif !important;
}

/* ФІКС ІКОНКИ ЗГОРТАННЯ САЙДБАРУ (keyboard_double_arrow) */
[data-testid="stSidebarCollapseButton"] button span,
[data-testid="stSidebarCollapseButton"] button div,
[data-testid="stSidebarNavSeparator"] {
    font-family: Source Sans Pro, -apple-system, BlinkMacSystemFont, Roboto, sans-serif !important;
}

/* Безпечний захист для системного меню та перемикача теми */
button[data-testid="stHeaderIconButton"], 
[data-testid="stHeader"] *,
[data-testid="stMainMenu"] * {
    font-family: Source Sans Pro, -apple-system, BlinkMacSystemFont, Roboto, sans-serif !important;
}

/* Примусове застосування Montserrat до графіків Plotly */
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


def clean_chart_layout(fig, height=200):
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
    return fig


# --- ШАПКА ---
st.title("Музейний реєстр")

# --- КАРТКА: Всього музеїв державної власності ---
colors_state_mus = ["#ef4444", "#f59e0b", "#10b981"]

with st.container(border=True):
    top_left, top_mid, top_right = st.columns([1.8, 2.0, 1.2], vertical_alignment="top")

    with top_left:
        st.markdown(
            """
            <div class='left-stat-block'>
                <div class='stat-title'>Всього музеїв державної власності</div>
                <h1 class='big-number'>648</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_mid:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors_state_mus[0]};'></span>Відсутні: <b>239</b></li>
                <li><span class='color-dot' style='background-color: {colors_state_mus[1]};'></span>Окуповані: <b>104</b></li>
                <li><span class='color-dot' style='background-color: {colors_state_mus[2]};'></span>Підконтрольні: <b>135</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    with top_right:
        labels_state = ["Відсутні", "Окуповані", "Підконтрольні"]
        values_state = [239, 104, 135]
        fig_state = go.Figure(
            data=[
                go.Pie(
                    labels=labels_state,
                    values=values_state,
                    hole=0.55,
                    marker_colors=colors_state_mus,
                    textinfo="percent",
                    insidetextorientation="radial",
                )
            ]
        )
        fig_state = clean_chart_layout(fig_state, height=190)
        st.plotly_chart(fig_state, use_container_width=True, config=plot_config)

st.divider()

# --- АВТОМАТИЧНЕ ЗАВАНТАЖЕННЯ ФАЙЛУ ---
current_dir = os.getcwd()
parent_dir = (
    os.path.dirname(current_dir)
    if os.path.basename(current_dir) == "pages"
    else current_dir
)
file_name = "РМФУ ВНЕСЕНО ПО ОБЛАСТЯХ.xlsx"
file_path = os.path.join(parent_dir, file_name)

if not os.path.exists(file_path):
    st.error(
        f"Не знайдено файл `{file_name}` у папці проєкту! Переконайтеся, що він"
        " лежить у головній папці поруч із `app.py`."
    )
    st.stop()


@st.cache_data
def load_rmfu_data(path):
    xls = pd.ExcelFile(path)
    all_mus, reg_sum = [], []

    for sheet in xls.sheet_names:
        df_sheet = pd.read_excel(path, sheet_name=sheet)
        m_df = df_sheet[
            ~df_sheet["ЄДРПОУ"]
            .astype(str)
            .str.upper()
            .str.contains("ВСЬОГО", na=False)
        ].copy()
        r_name = sheet.title() + (
            " обл." if "КИЇВ" not in sheet.upper() else ""
        )

        m_df["Регіон"] = r_name
        for col in [
            "ВСЬОГО ПРЕДМЕТІВ",
            "ВНЕСЕНО",
            "ПОТРІБНО ВНЕСТИ",
            "ОСНОВНИЙ ФОНД (ПІДПИСАНО)",
            "ОСНОВНИЙ ФОНД (ВНЕСЕНО)",
            "СПЕЦФОНД (ПІДПИСАНО)",
            "СПЕЦФОНД (ВНЕСЕНО)",
        ]:
            m_df[col] = pd.to_numeric(m_df[col], errors="coerce").fillna(0)

        m_df["Прогрес (%)"] = np.where(
            m_df["ВСЬОГО ПРЕДМЕТІВ"] > 0,
            (m_df["ВНЕСЕНО"] / m_df["ВСЬОГО ПРЕДМЕТІВ"]) * 100,
            0,
        ).round(1)
        all_mus.append(m_df)

        reg_items, reg_vneseno, reg_potribno = (
            m_df["ВСЬОГО ПРЕДМЕТІВ"].sum(),
            m_df["ВНЕСЕНО"].sum(),
            m_df["ПОТРІБНО ВНЕСТИ"].sum(),
        )
        reg_perc = (reg_vneseno / reg_items * 100) if reg_items > 0 else 0

        reg_sum.append({
            "Регіон": r_name,
            "Кількість музеїв": len(m_df),
            "Всього предметів": int(reg_items),
            "Внесено предметів": int(reg_vneseno),
            "Потрібно внести": int(reg_potribno),
            "Прогрес (%)": round(reg_perc, 1),
            "Основний фонд (підписано)": int(
                m_df["ОСНОВНИЙ ФОНД (ПІДПИСАНО)"].sum()
            ),
            "Основний фонд (внесено)": int(
                m_df["ОСНОВНИЙ ФОНД (ВНЕСЕНО)"].sum()
            ),
            "Спецфонд (підписано)": int(m_df["СПЕЦФОНД (ПІДПИСАНО)"].sum()),
            "Спецфонд (внесено)": int(m_df["СПЕЦФОНД (ВНЕСЕНО)"].sum()),
        })

    return pd.DataFrame(reg_sum), pd.concat(all_mus, ignore_index=True)


df_summary, df_museums = load_rmfu_data(file_path)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Всього музеїв", f"{int(df_summary['Кількість музеїв'].sum()):,}")
c2.metric("Всього предметів", f"{int(df_summary['Всього предметів'].sum()):,}")
c3.metric("Внесено предметів", f"{int(df_summary['Внесено предметів'].sum()):,}")
c4.metric(
    "Основний фонд (підписано)",
    f"{int(df_summary['Основний фонд (підписано)'].sum()):,}",
)
c5.metric(
    "Спецфонд (підписано)", f"{int(df_summary['Спецфонд (підписано)'].sum()):,}"
)
st.divider()

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
                max_value=(
                    100
                    if df_summary["Прогрес (%)"].max() <= 100
                    else int(df_summary["Прогрес (%)"].max())
                ),
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
        df_f = df_summary.sort_values(
            by="Основний фонд (внесено)", ascending=False
        )
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
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        st.plotly_chart(fig_fonds, use_container_width=True, config=plot_config)

with tab2:
    st.subheader("Пошук та детальний аналіз по музеях")
    cf1, cf2 = st.columns([1, 2])
    reg = cf1.selectbox(
        "Фільтр по області:",
        ["Усі області"] + list(df_summary["Регіон"].unique()),
    )
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
            "Регіон",
            "ЄДРПОУ",
            "НАЗВА МУЗЕЮ",
            "ВСЬОГО ПРЕДМЕТІВ",
            "ВНЕСЕНО",
            "ПОТРІБНО ВНЕСТИ",
            "Прогрес (%)",
            "ОСНОВНИЙ ФОНД (ПІДПИСАНО)",
            "ОСНОВНИЙ ФОНД (ВНЕСЕНО)",
            "СПЕЦФОНД (ПІДПИСАНО)",
            "СПЕЦФОНД (ВНЕСЕНО)",
        ]],
        use_container_width=True,
        hide_index=True,
    )
