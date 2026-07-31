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

# Точне налаштування CSS: Montserrat для контенту та Plotly, повна нейтралізація текстових іконок
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap');

/* Глобальний Montserrat для контенту */
.main, .stMarkdown, .stTable, .stDataFrame, h1, h2, h3, h4, h5, h6, p, div, span {
    font-family: 'Montserrat', sans-serif !important;
}

/* Приховуємо вилазячий текст іконок Streamlit у сайдбарі та шапці без зламу функціональності */
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"],
[data-testid="stSidebarNavSeparator"] {
    font-size: 0px !important;
    visibility: hidden !important;
}

/* Системний шрифт для кнопок управління, щоб зберегти базову іконку */
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

plot_config = {"displayModeBar": False}


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


# --- ШАПКА ТА ІНФОРМАЦІЯ ---
st.title("єПам'ятка")
st.caption("**Дані актуальні на 29.07.2026**")

# Палітри кольорів
colors1 = ["#2563EB", "#16A34A", "#EA580C", "#DC2626", "#9333EA", "#0284C7"]
colors0 = [
    "#2563EB",
    "#16A34A",
    "#F59E0B",
    "#DC2626",
    "#9333EA",
    "#EC4899",
    "#06B6D4",
]
colors2 = ["#2563EB", "#16A34A", "#F59E0B", "#DC2626", "#9333EA"]
colors4 = ["#16A34A", "#2563EB", "#F59E0B"]
colors5 = ["#16A34A", "#94A3B8"]
colors3 = ["#2563EB", "#16A34A", "#F59E0B"]

# --- БЛОК 1 (Нерухомі об'єкти на обліку - 145,172) ---
with st.container(border=True):
    top_left1, top_mid1, top_right1 = st.columns(
        [1.8, 2.0, 1.2], vertical_alignment="top"
    )

    with top_left1:
        st.markdown(
            """
            <div class='left-stat-block'>
                <div class='stat-title'>Нерухомі об'єкти культурної спадщини які знаходяться на обліку</div>
                <h1 class='big-number'>145,172</h1>
                <div class='green-tag'>за інформацією з офіційного звіту Мінкульту до Держстату за 2025 рік</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_mid1:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li style='padding-left: 0px;'><b>Внесено до Державного реєстру нерухомих пам'яток усього: 38,212</b></li>
                <li><span class='color-dot' style='background-color: {colors1[0]};'></span>Внесено до Державного реєстру нерухомих пам'яток національного значення: <b>3,415</b></li>
                <li><span class='color-dot' style='background-color: {colors1[1]};'></span>Внесено до Державного реєстру нерухомих пам'яток місцевого значення: <b>32,809</b></li>
                <li><span class='color-dot' style='background-color: {colors1[2]};'></span>Щойно виявлені об'єкти: <b>28,772</b></li>
                <li><span class='color-dot' style='background-color: {colors1[3]};'></span>Знято з обліку у 2025 році: <b>347</b></li>
                <li><span class='color-dot' style='background-color: {colors1[4]};'></span>Не визначено категорію: <b>79,929</b></li>
                <li><span class='color-dot' style='background-color: {colors1[5]};'></span>Об'єкти всесвітньої спадщини ЮНЕСКО: <b>8</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    with top_right1:
        labels1 = [
            "Реєстр нац.",
            "Реєстр місц.",
            "Щойно виявлені",
            "Знято з обліку",
            "Не визначено",
            "ЮНЕСКО",
        ]
        values1 = [3415, 32809, 28772, 347, 79929, 8]
        fig1 = go.Figure(
            data=[
                go.Pie(
                    labels=labels1,
                    values=values1,
                    hole=0.55,
                    marker_colors=colors1,
                    textinfo="percent",
                    insidetextorientation="radial",
                )
            ]
        )
        fig1 = clean_chart_layout(fig1, height=210)
        st.plotly_chart(fig1, use_container_width=True, config=plot_config)

# --- БЛОК 2 (Загальна кількість пам'яток, за видом - 116,500) ---
with st.container(border=True):
    top_left0, top_mid0, top_right0 = st.columns(
        [1.8, 2.0, 1.2], vertical_alignment="top"
    )

    with top_left0:
        st.markdown(
            """
            <div class='left-stat-block'>
                <div class='stat-title'>Загальна кількість пам'яток, за видом</div>
                <h1 class='big-number'>116,500</h1>
                <div class='green-tag'>за інформацією з офіційного звіту Мінкульту до Держстату за 2025 рік</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_mid0:
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

    with top_right0:
        df_vyd = pd.DataFrame({
            "Вид": [
                "Археол.",
                "Істор.",
                "Архіт.",
                "Монум.",
                "Ландш.",
                "Сад.-парк.",
                "Науки",
            ],
            "Кількість": [65891, 35654, 11892, 2567, 198, 177, 121],
            "Колір": colors0,
        }).iloc[::-1]

        fig0 = go.Figure(
            go.Bar(
                y=df_vyd["Вид"],
                x=df_vyd["Кількість"],
                orientation="h",
                text=df_vyd["Кількість"].apply(lambda x: f"{x:,}"),
                textposition="outside",
                marker_color=df_vyd["Колір"],
                cliponaxis=False,
            )
        )
        fig0 = clean_chart_layout(fig0, height=230)
        fig0.update_layout(
            margin=dict(l=10, r=60, t=10, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(
                title="", tickfont=dict(size=11, family="Montserrat, sans-serif")
            ),
        )
        st.plotly_chart(fig0, use_container_width=True, config=plot_config)

# --- БЛОК 3 (Внесено до системи єПам'ятка - 105,988) ---
with st.container(border=True):
    top_left2, top_mid2, top_right2 = st.columns(
        [1.8, 2.0, 1.2], vertical_alignment="top"
    )

    with top_left2:
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

    with top_mid2:
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

    with top_right2:
        labels2 = [
            "Національні",
            "Місцеві",
            "Щойно виявлені",
            "ЮНЕСКО",
            "Не визначено",
        ]
        values2 = [4595, 79765, 470, 70, 20683]
        fig2 = go.Figure(
            data=[
                go.Pie(
                    labels=labels2,
                    values=values2,
                    hole=0.55,
                    marker_colors=colors2,
                    textinfo="percent",
                    insidetextorientation="radial",
                )
            ]
        )
        fig2 = clean_chart_layout(fig2, height=190)
        st.plotly_chart(fig2, use_container_width=True, config=plot_config)

# --- БЛОК 4 (Історико-культурні території - 405) ---
with st.container(border=True):
    top_left4, top_mid4, top_right4 = st.columns(
        [1.8, 2.0, 1.2], vertical_alignment="top"
    )

    with top_left4:
        st.markdown(
            """
            <div class='left-stat-block'>
                <div class='stat-title'>Історико-культурні території</div>
                <h1 class='big-number'>405</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_mid4:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors4[0]};'></span>Оцифровано історико-культурних територій: <b>178</b></li>
                <li><span class='color-dot' style='background-color: {colors4[1]};'></span>Розгорнуто історико-культурних територій в єПам'ятці з геоданими: <b>15</b></li>
                <li><span class='color-dot' style='background-color: {colors4[2]};'></span>Підготовлено до розгортання в єПам'ятці: <b>158</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    with top_right4:
        fig4 = go.Figure(
            go.Funnel(
                y=["Оцифровано", "Підготовлено", "З геоданими"],
                x=[178, 158, 15],
                textinfo="value",
                marker={"color": colors4},
            )
        )
        fig4 = clean_chart_layout(fig4, height=160)
        st.plotly_chart(fig4, use_container_width=True, config=plot_config)

# --- БЛОК 5 (Картки національного значення - 1,043) ---
with st.container(border=True):
    top_left5, top_mid5, top_right5 = st.columns(
        [1.8, 2.0, 1.2], vertical_alignment="top"
    )

    with top_left5:
        st.markdown(
            """
            <div class='left-stat-block'>
                <div class='stat-title'>Картки національного значення, що підлягають верифікації в єПам'ятці</div>
                <h1 class='big-number'>1,043</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_mid5:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors5[0]};'></span>Верифіковано Управлінням дозвільно-погоджувальної документації: <b>65</b></li>
                <li><span class='color-dot' style='background-color: {colors5[1]};'></span>Верифіковано Управлінням дозвільно-погоджувальної документації без зауважень: <b>0</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    with top_right5:
        fig5 = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=65,
                number={
                    "suffix": " / 1,043",
                    "font": {"size": 18, "family": "Montserrat, sans-serif"},
                },
                gauge={
                    "axis": {"range": [None, 1043], "visible": False},
                    "bar": {"color": colors5[0]},
                    "bgcolor": "#e5e7eb",
                },
            )
        )
        fig5 = clean_chart_layout(fig5, height=140)
        st.plotly_chart(fig5, use_container_width=True, config=plot_config)

# --- БЛОК 6 (Користувачі - 226) ---
with st.container(border=True):
    top_left3, top_mid3, top_right3 = st.columns(
        [1.8, 2.0, 1.2], vertical_alignment="top"
    )

    with top_left3:
        st.markdown(
            """
            <div class='left-stat-block'>
                <div class='stat-title'>Користувачі</div>
                <h1 class='big-number'>226</h1>
                <div class='green-tag'>↑ 86% користувачі ОВА та КП</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_mid3:
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

    with top_right3:
        labels3 = ["ОВА та КП", "Мінкульт", "Адміни"]
        values3 = [195, 13, 18]
        fig3 = go.Figure(
            data=[
                go.Pie(
                    labels=labels3,
                    values=values3,
                    hole=0.55,
                    marker_colors=colors3,
                    textinfo="value+percent",
                    textposition="inside",
                )
            ]
        )
        fig3 = clean_chart_layout(fig3, height=150)
        st.plotly_chart(fig3, use_container_width=True, config=plot_config)

# --- ВІЗУАЛІЗАЦІЯ КОРИСТУВАЧІВ ПО ОБЛАСТЯХ ---
users_by_region_data = {
    "Регіон": [
        "Вінницька",
        "Волинська",
        "Дніпропетровська",
        "Донецька",
        "Житомирська",
        "Закарпатська",
        "Запорізька",
        "Івано-Франківська",
        "Київська",
        "Кіровоградська",
        "Луганська",
        "Львівська",
        "Миколаївська",
        "Одеська",
        "Полтавська",
        "Рівненська",
        "Сумська",
        "Тернопільська",
        "Харківська",
        "Херсонська",
        "Хмельницька",
        "Черкаська",
        "Чернівецька",
        "Чернігівська",
        "м. Київ",
    ],
    "Кількість користувачів": [
        5,
        8,
        6,
        3,
        9,
        5,
        13,
        6,
        12,
        4,
        5,
        8,
        4,
        4,
        12,
        4,
        9,
        10,
        7,
        8,
        12,
        5,
        5,
        7,
        24,
    ],
}

df_users_reg = pd.DataFrame(users_by_region_data).sort_values(
    by="Кількість користувачів", ascending=True
)

st.subheader("Розподіл користувачів ОВА та КП за регіонами")

fig_users = px.bar(
    df_users_reg,
    x="Кількість користувачів",
    y="Регіон",
    orientation="h",
    text="Кількість користувачів",
    color="Кількість користувачів",
    color_continuous_scale="Blues",
    height=650,
)
fig_users.update_traces(textposition="outside")
fig_users.update_layout(
    template="plotly_white",
    margin=dict(l=0, r=50, t=30, b=0),
    xaxis_title="Кількість користувачів",
    yaxis_title="",
    coloraxis_showscale=False,
    font=dict(family="Montserrat, sans-serif"),
    hoverlabel=dict(font_family="Montserrat, sans-serif"),
)
st.plotly_chart(fig_users, use_container_width=True, config=plot_config)

st.divider()

# --- АВТОМАТИЧНЕ ЗАВАНТАЖЕННЯ ФАЙЛУ ---
current_dir = os.getcwd()
parent_dir = (
    os.path.dirname(current_dir)
    if os.path.basename(current_dir) == "pages"
    else current_dir
)
file_name = "свод нерухома обл 2026 (1).xlsx"
file_path = os.path.join(parent_dir, file_name)

if not os.path.exists(file_path):
    st.error(
        f"Не знайдено файл `{file_name}`! Переконайтеся, що він лежить у"
        " головній папці поруч із `app.py`."
    )
    st.stop()

xls = pd.ExcelFile(file_path)
selected_sheet = xls.sheet_names[0]

# Точні назви колонок
col_reestr = (
    "Кількість об'єктів національного значення в Реєстрі (на сайті Мінкульту)"
)
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
        elif (
            ("реєстр" in text or "мінкульт" in text)
            and "відсоток" not in text
            and "карток" not in text
            and c_reestr == -1
        ):
            c_reestr = i
        elif "чернеток" in text and "всього" in text:
            c_drafts_all = i
        elif "чернеток" in text and ("національного" in text or "нац" in text):
            c_drafts_nac = i
        elif (
            "карток" in text
            and "національного" in text
            and "відсоток" not in text
        ):
            c_cards = i

    if c_reg == -1:
        c_reg = 1
    if c_reestr == -1:
        c_reestr = 2
    if c_cards == -1:
        c_cards = len(df_raw.columns) - 1

    start_row = next(
        (
            r
            for r in range(min(10, len(df_raw)))
            if "вінницька" in str(df_raw.iloc[r, c_reg]).lower()
        ),
        1,
    )
    data = df_raw.iloc[start_row:].copy()

    df = pd.DataFrame({
        "Регіон": data.iloc[:, c_reg].astype(str),
        col_reestr: pd.to_numeric(data.iloc[:, c_reestr], errors="coerce")
        .fillna(0)
        .astype(int),
        col_cards: pd.to_numeric(data.iloc[:, c_cards], errors="coerce")
        .fillna(0)
        .astype(int),
    })

    if c_drafts_all != -1:
        df[col_draft_all] = (
            pd.to_numeric(data.iloc[:, c_drafts_all], errors="coerce")
            .fillna(0)
            .astype(int)
        )
    if c_drafts_nac != -1:
        df[col_draft_nac] = (
            pd.to_numeric(data.iloc[:, c_drafts_nac], errors="coerce")
            .fillna(0)
            .astype(int)
        )

    end_idx = next(
        (
            i
            for i, val in enumerate(df["Регіон"])
            if str(val).lower().strip().startswith(("всього", "разом"))
        ),
        len(df),
    )
    df = df.iloc[:end_idx].dropna(subset=["Регіон"])
    df = df[(df["Регіон"].str.lower() != "nan") & (df["Регіон"].str.len() > 3)]

    df[col_perc] = np.where(
        df[col_reestr] > 0, (df[col_cards] / df[col_reestr]) * 100, 0
    )

    cols = ["Регіон", col_perc, col_reestr, col_cards]
    if col_draft_all in df.columns:
        cols.append(col_draft_all)
    if col_draft_nac in df.columns:
        cols.append(col_draft_nac)

    return df[cols].sort_values(by=col_perc, ascending=False)


df = load_data(file_path, selected_sheet)
if df.empty:
    st.warning("Не знайдено даних.")
    st.stop()

# --- ГРАФІК ---
st.subheader("Об'єкти національного значення в єПам'ятці")
df_sorted = df.sort_values(by=col_reestr, ascending=False)
fig_comp = go.Figure(
    data=[
        go.Bar(
            x=df_sorted["Регіон"],
            y=df_sorted[col_reestr],
            name="Об'єкти в Реєстрі",
            marker_color="#d1d5db",
        ),
        go.Bar(
            x=df_sorted["Регіон"],
            y=df_sorted[col_cards],
            name="Внесено в єПам'ятку",
            marker_color="#3b82f6",
        ),
    ]
)
fig_comp.update_layout(
    barmode="group",
    template="plotly_white",
    height=500,
    xaxis_tickangle=-45,
    font=dict(family="Montserrat, sans-serif"),
    hoverlabel=dict(font_family="Montserrat, sans-serif"),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
    ),
)
st.plotly_chart(fig_comp, use_container_width=True, config=plot_config)
