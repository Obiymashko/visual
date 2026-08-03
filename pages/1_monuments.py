import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Дашборд: єПам'ятка",
    page_icon="🏛️",
    layout="wide",
)

# Точне налаштування CSS: Montserrat для контенту, збереження системних іконок Streamlit
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap');
/* Підключаємо оригінальний шрифт іконок про всяк випадок, щоб браузер його не загубив */
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0');

/* 1. Глобальний Montserrat для всього контенту */
html, body, [class*="st-"], .stMarkdown, .stTable, .stDataFrame, h1, h2, h3, h4, h5, h6, p, div, span, li {
    font-family: 'Montserrat', sans-serif !important;
}

/* 2. 🔥 РЯТУЄМО ВСІ СИСТЕМНІ ІКОНКИ STREAMLIT 🔥 */
/* Повертаємо шрифт Material Symbols спеціально для іконок меню, теми та сайдбару */
span[data-testid="stIconMaterial"], 
span[translate="no"], 
i.material-icons,
.material-symbols-rounded,
button[kind="headerNoPadding"] span {
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
}

/* Приховуємо вилазячий текст іконок */
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"],
[data-testid="stSidebarNavSeparator"] {
    font-size: 0px !important;
    visibility: hidden !important;
}

[data-testid="stSidebarNav"] span {
    font-family: 'Montserrat', sans-serif !important;
}

/* 3. Montserrat для графіків Plotly */
.js-plotly-plot .plotly text,
.js-plotly-plot .plotly .hovertext,
.js-plotly-plot .plotly .gtitle,
.js-plotly-plot .plotly .xtitle,
.js-plotly-plot .plotly .ytitle {
    font-family: 'Montserrat', sans-serif !important;
}

/* --- ВАШІ КАСТОМНІ СТИЛІ КАРТОК (Адаптивні під теми) --- */
.left-stat-block {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    padding-top: 10px;
}

.stat-title {
    font-weight: 700;
    font-size: 15px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
    line-height: 1.4;
    opacity: 0.7;
}

.big-number {
    font-family: 'Montserrat', sans-serif !important;
    font-size: 4.2rem !important;
    font-weight: 900 !important;
    letter-spacing: -1px;
    margin: 0px 0px 10px 0px !important;
    line-height: 1 !important;
}

.green-tag {
    font-family: 'Montserrat', sans-serif !important;
    color: #16a34a;
    font-size: 15px;
    font-weight: 800;
    margin-top: 4px;
    background-color: rgba(22, 163, 74, 0.15);
    padding: 4px 10px;
    border-radius: 6px;
}

.sub-list {
    font-family: 'Montserrat', sans-serif !important;
    font-size: 15px !important;
    opacity: 0.95 !important;
    line-height: 2 !important;
    margin: 0 !important;
    padding-left: 0px !important;
    list-style-type: none !important;
}
.sub-list li {
    position: relative;
    padding-left: 24px;
    margin-bottom: 6px;
}
.sub-list b {
    font-weight: 800 !important;
    font-size: 16px !important;
}

.color-dot {
    height: 12px;
    width: 12px;
    border-radius: 50%;
    display: inline-block;
    position: absolute;
    left: 0;
    top: 9px;
    box-sizing: border-box;
}

.highlight-box {
    background-color: rgba(37, 99, 235, 0.1);
    border-left: 3px solid #2563eb;
    padding: 8px 14px;
    margin-bottom: 14px;
    border-radius: 4px;
}
</style>
""",
    unsafe_allow_html=True,
)

plot_config = {"displayModeBar": False}


def clean_chart_layout(fig, height=220):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=20, t=10, b=10),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font=dict(family="Montserrat, sans-serif", size=14),
        hoverlabel=dict(font_family="Montserrat, sans-serif", font_size=15),
    )
    if fig.data and getattr(fig.data[0], 'type', None) == 'pie':
        fig.update_traces(
            textposition="inside", 
            textinfo="percent", 
            insidetextorientation="radial",
            textfont_size=15,
            textfont_color="white",
            marker=dict(line=dict(color='rgba(0,0,0,0)', width=2))
        )
    return fig


# --- ШАПКА ТА ІНФОРМАЦІЯ ---
st.title("єПам'ятка")
st.caption("**Дані актуальні на 29.07.2026**")
st.write("") # Відступ

# Палітри кольорів
colors1 = ["#1E3A8A", "#2563EB", "#16A34A", "#EA580C", "#DC2626", "#9333EA", "#0284C7"]
colors0 = ["#2563EB", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#06B6D4"]
colors2 = ["#1E40AF", "#10B981", "#F59E0B", "#DC2626", "#8B5CF6"]
colors4 = ["#10B981", "#3b82f6", "#f59e0b"]
colors5 = ["#10B981", "rgba(148, 163, 184, 0.3)"]
colors3 = ["#2563EB", "#10B981", "#F59E0B"]

# --- БЛОК 1 (Нерухомі об'єкти на обліку - 145,172) ---
with st.container(border=True):
    col1, col2, col3 = st.columns([1.8, 2.0, 1.2], vertical_alignment="center")

    with col1:
        st.markdown(
            """
            <div class='left-stat-block'>
                <div class='stat-title'>Нерухомі об'єкти культурної спадщини які знаходяться на обліку</div>
                <h1 class='big-number'>145,172</h1>
                <div class='green-tag' style='background-color: rgba(100, 116, 139, 0.15); color: inherit; opacity: 0.8;'>за інформацією з офіційного звіту Мінкульту до Держстату за 2025 рік</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class='highlight-box'>
                <span style='font-size: 14px; opacity: 0.8; font-weight: 600;'>Внесено до Державного реєстру нерухомих пам'яток усього:</span><br>
                <b style='font-size: 22px;'>38,212</b>
            </div>
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors1[1]};'></span>Внесено до Державного реєстру нерухомих пам'яток національного значення: <b>3,415</b></li>
                <li><span class='color-dot' style='background-color: {colors1[2]};'></span>Внесено до Державного реєстру нерухомих пам'яток місцевого значення: <b>32,809</b></li>
                <li><span class='color-dot' style='background-color: {colors1[3]};'></span>Щойно виявлені об'єкти: <b>28,772</b></li>
                <li><span class='color-dot' style='background-color: {colors1[4]};'></span>Знято з обліку у 2025 році: <b>347</b></li>
                <li><span class='color-dot' style='background-color: {colors1[5]};'></span>Не визначено категорію: <b>79,929</b></li>
                <li><span class='color-dot' style='background-color: {colors1[6]};'></span>Об'єкти всесвітньої спадщини ЮНЕСКО: <b>8</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        labels1 = ["Реєстр нац.", "Реєстр місц.", "Щойно виявлені", "Знято з обліку", "Не визначено", "ЮНЕСКО"]
        values1 = [3415, 32809, 28772, 347, 79929, 8]
        fig1 = go.Figure(data=[go.Pie(labels=labels1, values=values1, hole=0.6, marker_colors=colors1[1:])])
        st.plotly_chart(clean_chart_layout(fig1, height=250), use_container_width=True, config=plot_config)

# --- БЛОК 2 (Загальна кількість пам'яток, за видом - 116,500) ---
with st.container(border=True):
    col1, col2, col3 = st.columns([1.8, 2.0, 1.2], vertical_alignment="center")

    with col1:
        st.markdown(
            """
            <div class='left-stat-block'>
                <div class='stat-title'>Загальна кількість пам'яток, за видом</div>
                <h1 class='big-number'>116,500</h1>
                <div class='green-tag' style='background-color: rgba(100, 116, 139, 0.15); color: inherit; opacity: 0.8;'>за інформацією з офіційного звіту Мінкульту до Держстату за 2025 рік</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors0[0]};'></span>Археологічні: <b>65,891</b></li>
                <li><span class='color-dot' style='background-color: {colors0[1]};'></span>Історичні: <b>35,654</b></li>
                <li><span class='color-dot' style='background-color: {colors0[2]};'></span>Архітектури та містобудування: <b>11,892</b></li>
                <li><span class='color-dot' style='background-color: {colors0[3]};'></span>Монументального мистецтва: <b>2,567</b></li>
                <li><span class='color-dot' style='background-color: {colors0[4]};'></span>Ландшафтні: <b>198</b></li>
                <li><span class='color-dot' style='background-color: {colors0[5]};'></span>Садово-паркового мистецтва: <b>177</b></li>
                <li><span class='color-dot' style='background-color: {colors0[6]};'></span>Науки і техніки: <b>121</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        df_vyd = pd.DataFrame({
            "Вид": ["Археол.", "Істор.", "Архіт.", "Монум.", "Ландш.", "Сад.-парк.", "Науки"],
            "Кількість": [65891, 35654, 11892, 2567, 198, 177, 121],
            "Колір": colors0,
        }).iloc[::-1]

        fig0 = go.Figure(go.Bar(
            y=df_vyd["Вид"], x=df_vyd["Кількість"], orientation="h",
            text=df_vyd["Кількість"].apply(lambda x: f"{x:,}"), textposition="outside",
            marker_color=df_vyd["Колір"], cliponaxis=False
        ))
        fig0 = clean_chart_layout(fig0, height=260)
        fig0.update_layout(
            margin=dict(l=10, r=60, t=10, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(title="", tickfont=dict(size=13, family="Montserrat, sans-serif")),
        )
        st.plotly_chart(fig0, use_container_width=True, config=plot_config)

# --- БЛОК 3 (Внесено до системи єПам'ятка - 105,988) ---
with st.container(border=True):
    col1, col2, col3 = st.columns([1.8, 2.0, 1.2], vertical_alignment="center")

    with col1:
        st.markdown(
            """
            <div class='left-stat-block'>
                <div class='stat-title'>Внесено до системи єПам'ятка</div>
                <h1 class='big-number'>105,988</h1>
                <div class='green-tag'>↑ 73% від загальної кількості</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors2[0]};'></span>Пам'ятки національного значення: <b>4,595</b></li>
                <li><span class='color-dot' style='background-color: {colors2[1]};'></span>Пам'ятки місцевого значення: <b>79,765</b></li>
                <li><span class='color-dot' style='background-color: {colors2[2]};'></span>Щойно виявлені об'єкти культурної спадщини: <b>470</b></li>
                <li><span class='color-dot' style='background-color: {colors2[3]};'></span>Об'єкти всесвітньої спадщини ЮНЕСКО: <b>70</b></li>
                <li><span class='color-dot' style='background-color: {colors2[4]};'></span>Користувач не визначив статус: <b>20,683</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        labels2 = ["Національні", "Місцеві", "Щойно виявлені", "ЮНЕСКО", "Не визначено"]
        values2 = [4595, 79765, 470, 70, 20683]
        fig2 = go.Figure(data=[go.Pie(labels=labels2, values=values2, hole=0.6, marker_colors=colors2)])
        st.plotly_chart(clean_chart_layout(fig2, height=220), use_container_width=True, config=plot_config)

# --- БЛОК 4 (Історико-культурні території - 405) ---
with st.container(border=True):
    col1, col2, col3 = st.columns([1.8, 2.0, 1.2], vertical_alignment="center")

    with col1:
        st.markdown(
            """
            <div class='left-stat-block'>
                <div class='stat-title'>Історико-культурні території</div>
                <h1 class='big-number'>405</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors4[0]};'></span>Оцифровано історико-культурних територій: <b>178</b></li>
                <li><span class='color-dot' style='background-color: {colors4[2]};'></span>Підготовлено до розгортання в єПам'ятці: <b>158</b></li>
                <li><span class='color-dot' style='background-color: {colors4[1]};'></span>Розгорнуто в єПам'ятці з геоданими: <b>15</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        fig4 = go.Figure(go.Funnel(
            y=["Оцифровано", "Підготовлено", "З геоданими"],
            x=[178, 158, 15],
            textinfo="value",
            marker={"color": [colors4[0], colors4[2], colors4[1]]}
        ))
        st.plotly_chart(clean_chart_layout(fig4, height=180), use_container_width=True, config=plot_config)

# --- БЛОК 5 (Картки національного значення - 1,043) ---
with st.container(border=True):
    col1, col2, col3 = st.columns([1.8, 2.0, 1.2], vertical_alignment="center")

    with col1:
        st.markdown(
            """
            <div class='left-stat-block'>
                <div class='stat-title'>Картки національного значення, що підлягають верифікації в єПам'ятці</div>
                <h1 class='big-number'>1,043</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors5[0]};'></span>Верифіковано Управлінням дозвільно-погоджувальної документації: <b>65</b></li>
                <li><span class='color-dot' style='background-color: transparent; border: 2px solid {colors5[0]};'></span>Верифіковано без зауважень: <b>0</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        fig5 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=65,
            number={"suffix": " / 1,043", "font": {"size": 24, "family": "Montserrat, sans-serif"}},
            gauge={
                "axis": {"range": [None, 1043], "visible": False},
                "bar": {"color": colors5[0], "thickness": 0.8},
                "bgcolor": colors5[1],
                "borderwidth": 0,
            },
        ))
        st.plotly_chart(clean_chart_layout(fig5, height=160), use_container_width=True, config=plot_config)

# --- БЛОК 6 (Користувачі - 226) ---
with st.container(border=True):
    col1, col2, col3 = st.columns([1.8, 2.0, 1.2], vertical_alignment="center")

    with col1:
        st.markdown(
            """
            <div class='left-stat-block'>
                <div class='stat-title'>Користувачі</div>
                <h1 class='big-number'>226</h1>
                <div class='green-tag' style='background-color: rgba(37, 99, 235, 0.15); color: #2563eb;'>↑ 86% користувачі ОВА та КП</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors3[0]};'></span>Користувачі ОВА та КП: <b>195</b></li>
                <li><span class='color-dot' style='background-color: {colors3[1]};'></span>Користувачі Мінкульт: <b>13</b></li>
                <li><span class='color-dot' style='background-color: {colors3[2]};'></span>Адміністратори: <b>18</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        labels3 = ["ОВА та КП", "Мінкульт", "Адміни"]
        values3 = [195, 13, 18]
        fig6 = go.Figure(data=[go.Pie(labels=labels3, values=values3, hole=0.6, marker_colors=colors3)])
        st.plotly_chart(clean_chart_layout(fig6, height=220), use_container_width=True, config=plot_config)

st.divider()

# =====================================================================
# ВІЗУАЛІЗАЦІЯ ДАНИХ ПО РЕГІОНАХ ТА МУЗЕЯХ
# =====================================================================

users_by_region_data = {
    "Регіон": [
        "Вінницька", "Волинська", "Дніпропетровська", "Донецька", "Житомирська",
        "Закарпатська", "Запорізька", "Івано-Франківська", "Київська", "Кіровоградська",
        "Луганська", "Львівська", "Миколаївська", "Одеська", "Полтавська",
        "Рівненська", "Сумська", "Тернопільська", "Харківська", "Херсонська",
        "Хмельницька", "Черкаська", "Чернівецька", "Чернігівська", "м. Київ",
    ],
    "Кількість користувачів": [
        5, 8, 6, 3, 9, 5, 13, 6, 12, 4, 5, 8, 4, 4, 12, 4, 9, 10, 7, 8, 12, 5, 5, 7, 24,
    ],
}

df_users_reg = pd.DataFrame(users_by_region_data).sort_values(by="Кількість користувачів", ascending=True)

st.subheader("Розподіл користувачів ОВА та КП за регіонами")

fig_users = px.bar(
    df_users_reg,
    x="Кількість користувачів",
    y="Регіон",
    orientation="h",
    text="Кількість користувачів",
    color="Кількість користувачів",
    color_continuous_scale="Viridis",
    height=750,
)
fig_users.update_traces(
    textposition="outside", 
    textfont=dict(size=14, family="Montserrat, sans-serif"),
    marker_line_width=0
)
fig_users.update_layout(
    margin=dict(l=0, r=60, t=30, b=0),
    xaxis_title="",
    yaxis_title="",
    coloraxis_showscale=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Montserrat, sans-serif", size=14),
    hoverlabel=dict(font_family="Montserrat, sans-serif", font_size=15),
)
st.plotly_chart(fig_users, use_container_width=True, config=plot_config)

st.divider()

# =====================================================================
# АВТОМАТИЧНЕ ЗАВАНТАЖЕННЯ ФАЙЛУ ДЛЯ НИЖНЬОГО ГРАФІКУ
# =====================================================================
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir) if os.path.basename(current_dir) == "pages" else current_dir
file_name = "свод нерухома обл 2026 (1).xlsx"
file_path = os.path.join(parent_dir, file_name)

if not os.path.exists(file_path):
    st.error(f"Не знайдено файл `{file_name}`! Переконайтеся, що він лежить у головній папці поруч із `app.py`.")
    st.stop()

xls = pd.ExcelFile(file_path)
selected_sheet = xls.sheet_names[0]

col_reestr = "Кількість об'єктів національного значення в Реєстрі (на сайті Мінкульту)"
col_cards = "Кількість карток національного значення в ЄПам'ятка"
col_perc = "Загальний прогрес (відсоток карток від об'єктів в реєстрі)"

@st.cache_data
def load_data(path, sheet):
    df_raw = pd.read_excel(path, sheet_name=sheet)
    c_reg, c_reestr, c_cards = -1, -1, -1

    for i, col in enumerate(df_raw.columns):
        text = str(col).lower()
        for r in range(min(3, len(df_raw))):
            text += " " + str(df_raw.iloc[r, i]).lower()

        if ("регіон" in text or "область" in text) and c_reg == -1: c_reg = i
        elif ("реєстр" in text or "мінкульт" in text) and "відсоток" not in text and "карток" not in text and c_reestr == -1: c_reestr = i
        elif "карток" in text and "національного" in text and "відсоток" not in text: c_cards = i

    if c_reg == -1: c_reg = 1
    if c_reestr == -1: c_reestr = 2
    if c_cards == -1: c_cards = len(df_raw.columns) - 1

    start_row = next((r for r in range(min(10, len(df_raw))) if "вінницька" in str(df_raw.iloc[r, c_reg]).lower()), 1)
    data = df_raw.iloc[start_row:].copy()

    df = pd.DataFrame({
        "Регіон": data.iloc[:, c_reg].astype(str),
        col_reestr: pd.to_numeric(data.iloc[:, c_reestr], errors="coerce").fillna(0).astype(int),
        col_cards: pd.to_numeric(data.iloc[:, c_cards], errors="coerce").fillna(0).astype(int),
    })

    end_idx = next((i for i, val in enumerate(df["Регіон"]) if str(val).lower().strip().startswith(("всього", "разом"))), len(df))
    df = df.iloc[:end_idx].dropna(subset=["Регіон"])
    df = df[(df["Регіон"].str.lower() != "nan") & (df["Регіон"].str.len() > 3)]

    df[col_perc] = np.where(df[col_reestr] > 0, (df[col_cards] / df[col_reestr]) * 100, 0)
    return df[["Регіон", col_perc, col_reestr, col_cards]].sort_values(by=col_perc, ascending=False)

df = load_data(file_path, selected_sheet)
if df.empty:
    st.warning("Не знайдено даних.")
    st.stop()

# 3. Вертикальний графік: Об'єкти нац. значення (З ОБМЕЖЕННЯМ ВИСОТИ СИНЬОГО СТОВПЧИКА)
st.subheader("Об'єкти національного значення в єПам'ятці")
df_sorted = df.sort_values(by=col_reestr, ascending=False)

# Візуальне обмеження: якщо внесено більше ніж є в реєстрі, стовпчик малюється не вище сірого
df_sorted["Внесено_візуально"] = np.minimum(df_sorted[col_cards], df_sorted[col_reestr])

fig_comp = go.Figure(
    data=[
        go.Bar(
            x=df_sorted["Регіон"],
            y=df_sorted[col_reestr],
            name="Об'єкти в Реєстрі",
            marker_color="rgba(148, 163, 184, 0.4)", # Напівпрозорий сірий
            hovertemplate="%{x}<br>Об'єкти в Реєстрі: %{y}<extra></extra>"
        ),
        go.Bar(
            x=df_sorted["Регіон"],
            y=df_sorted["Внесено_візуально"], # Використовуємо обмежену висоту для візуалу
            name="Внесено в єПам'ятку",
            marker_color="#2563eb", # Синій
            customdata=df_sorted[col_cards], # Але зберігаємо реальні дані для підказки (hover)
            hovertemplate="%{x}<br>Внесено в єПам'ятку: %{customdata}<extra></extra>"
        ),
    ]
)
fig_comp.update_layout(
    barmode="group",
    height=600,
    xaxis_tickangle=-45,
    margin=dict(l=0, r=0, t=30, b=80),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Montserrat, sans-serif", size=14),
    hoverlabel=dict(font_family="Montserrat, sans-serif", font_size=15),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font_size=15),
    bargap=0.15,
)
st.plotly_chart(fig_comp, use_container_width=True, config=plot_config)
