import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Дашборд: єПам'ятка",
    page_icon=":material/account_balance:",
    layout="wide",
)

# CSS для красивих розмірів та відступів
st.markdown(
    """
<style>
/* Стилі для великих чисел */
.big-number {
    font-size: 3.8rem !important;
    font-weight: 900 !important;
    margin: 0px 0px 4px 0px !important;
    line-height: 1 !important;
}

/* Стилі для підпунктів праворуч */
.sub-list {
    font-size: 16px !important;
    opacity: 0.95 !important;
    line-height: 1.8 !important;
    margin: 0 !important;
    padding-left: 20px !important;
}
.sub-list b {
    font-weight: 900 !important;
}

/* Зелені підписи */
.green-tag {
    color: #00d26a;
    font-size: 14px;
    font-weight: 700;
}
</style>
""",
    unsafe_allow_html=True,
)

plot_config = {
    "displayModeBar": True,
    "toImageButtonOptions": {
        "format": "png",
        "filename": "chart",
        "height": 720,
        "width": 1280,
        "scale": 3,
    },
}

# --- ШАПКА ТА ІНФОРМАЦІЯ ---
st.title(":material/account_balance: єПам'ятка")
st.caption(":material/calendar_today: **Дані актуальні на 29.07.2026**")

# --- БЛОК 1 (Нерухомі об'єкти на обліку - 145,172) ---
with st.container(border=True):
    top_left1, top_right1 = st.columns([1.5, 3.5], vertical_alignment="center")

    with top_left1:
        st.markdown(
            "**:material/account_balance: <span style='color: #8c92a4;"
            " font-weight: 600; font-size: 14px;'>Нерухомі об'єкти культурної"
            " спадщини які знаходяться на обліку</span>**",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h1 class='big-number'>145,172</h1>", unsafe_allow_html=True
        )
        st.markdown(
            "<div class='green-tag'>за інформацією з офіційного звіту Мінкульту"
            " до Держстату за 2025 рік</div>",
            unsafe_allow_html=True,
        )

    with top_right1:
        st.markdown(
            """
            <ul class='sub-list'>
                <li>Об'єкти всесвітньої спадщини ЮНЕСКО: <b>8</b></li>
                <li>Внесено до державного реєстру нерухомих пам'яток нац. значення: <b>3,415</b></li>
                <li>Внесено до державного реєстру нерухомих пам'яток місц. значення: <b>32,809</b></li>
                <li>Щойно виявлені об'єкти: <b>28,772</b></li>
                <li>Знято з обліку у 2025 році: <b>347</b></li>
                <li>Не визначено категорію: <b>79,929</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

# --- БЛОК 2 (Загальна кількість пам'яток, за видом - 116,500) ---
with st.container(border=True):
    top_left0, top_right0 = st.columns([1.5, 3.5], vertical_alignment="center")

    with top_left0:
        st.markdown(
            "**:material/collections_bookmark: <span style='color: #8c92a4;"
            " font-weight: 600; font-size: 14px;'>Загальна кількість пам'яток,"
            " за видом</span>**",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h1 class='big-number'>116,500</h1>", unsafe_allow_html=True
        )
        st.markdown(
            "<div class='green-tag'>за інформацією з офіційного звіту Мінкульту"
            " до Держстату за 2025 рік</div>",
            unsafe_allow_html=True,
        )

    with top_right0:
        st.markdown(
            """
            <ul class='sub-list'>
                <li>Археологічні: <b>65,891</b></li>
                <li>Історичні: <b>35,654</b></li>
                <li>Архітектури та містобудування: <b>11,892</b></li>
                <li>Монументального мистецтва: <b>2,567</b></li>
                <li>Ландшафтні: <b>198</b></li>
                <li>Садово-паркового мистецтва: <b>177</b></li>
                <li>Науки і техніки: <b>121</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

# --- БЛОК 3 (Внесено до системи єПам'ятка - 105,988) ---
with st.container(border=True):
    top_left2, top_right2 = st.columns([1.5, 3.5], vertical_alignment="center")

    with top_left2:
        st.markdown(
            "**:material/cloud_upload: <span style='color: #8c92a4;"
            " font-weight: 600; font-size: 14px;'>Внесено до системи"
            " єПам'ятка</span>**",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h1 class='big-number'>105,988</h1>", unsafe_allow_html=True
        )
        st.markdown(
            "<div class='green-tag'>↑ 73% від загальної кількості</div>",
            unsafe_allow_html=True,
        )

    with top_right2:
        st.markdown(
            """
            <ul class='sub-list'>
                <li>Пам'ятки національного значення: <b>4,595</b></li>
                <li>Пам'ятки місцевого значення: <b>79,765</b></li>
                <li>Щойно виявлені об'єкти культурної спадщини: <b>470</b></li>
                <li>Об'єкти всесвітньої спадщини ЮНЕСКО: <b>70</b></li>
                <li>Користувач не визначив статус: <b>20,683</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

# --- БЛОК 4 (Історико-культурні території - 405) ---
with st.container(border=True):
    top_left4, top_right4 = st.columns([1.5, 3.5], vertical_alignment="center")

    with top_left4:
        st.markdown(
            "**:material/map: <span style='color: #8c92a4; font-weight:"
            " 600; font-size: 14px;'>Історико-культурні території</span>**",
            unsafe_allow_html=True,
        )
        st.markdown("<h1 class='big-number'>405</h1>", unsafe_allow_html=True)

    with top_right4:
        st.markdown(
            """
            <ul class='sub-list'>
                <li>Оцифровано історико-культурних територій: <b>178</b></li>
                <li>Розгорнуто історико-культурних територій в єПам'ятці з геоданими: <b>15</b></li>
                <li>Підготовлено до розгортання в єПам'ятці: <b>158</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

# --- БЛОК 5 (Картки, що підлягають верифікації - 1,043) ---
with st.container(border=True):
    top_left5, top_right5 = st.columns([1.5, 3.5], vertical_alignment="center")

    with top_left5:
        st.markdown(
            "**:material/fact_check: <span style='color: #8c92a4; font-weight:"
            " 600; font-size: 14px;'>Картки, що підлягають верифікації</span>**",
            unsafe_allow_html=True,
        )
        st.markdown("<h1 class='big-number'>1,043</h1>", unsafe_allow_html=True)

    with top_right5:
        st.markdown(
            """
            <ul class='sub-list'>
            </ul>
            """,
            unsafe_allow_html=True,
        )

# --- БЛОК 6 (Користувачі - 226) ---
with st.container(border=True):
    top_left3, top_right3 = st.columns([1.5, 3.5], vertical_alignment="center")

    with top_left3:
        st.markdown(
            "**:material/group: <span style='color: #8c92a4; font-weight:"
            " 600; font-size: 14px;'>Користувачі</span>**",
            unsafe_allow_html=True,
        )
        st.markdown("<h1 class='big-number'>226</h1>", unsafe_allow_html=True)
        st.markdown(
            "<div class='green-tag'>↑ 86% користувачі ОВА та КП</div>",
            unsafe_allow_html=True,
        )

    with top_right3:
        st.markdown(
            """
            <ul class='sub-list'>
                <li>Користувачі ОВА та КП: <b>195</b></li>
                <li>Користувачі Мінкульт: <b>13</b></li>
                <li>Адміністратори: <b>18</b></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

# --- ВІЗУАЛІЗАЦІЯ КОРИСТУВАЧІВ ПО ОБЛАСТЯХ ---
users_by_region_data = {
    "Регіон": [
        "Вінницька", "Волинська", "Дніпропетровська", "Донецька", "Житомирська",
        "Закарпатська", "Запорізька", "Івано-Франківська", "Київська", "Кіровоградська",
        "Луганська", "Львівська", "Миколаївська", "Одеська", "Полтавська",
        "Рівненська", "Сумська", "Тернопільська", "Харківська", "Херсонська",
        "Хмельницька", "Черкаська", "Чернівецька", "Чернігівська", "м. Київ"
    ],
    "Кількість користувачів": [
        5, 8, 6, 3, 9, 5, 13, 6, 12, 4, 5, 8, 4, 4, 12, 4, 9, 10, 7, 8, 12, 5, 5, 7, 24
    ]
}

df_users_reg = pd.DataFrame(users_by_region_data).sort_values(
    by="Кількість користувачів", ascending=True
)

st.subheader(":material/badge: Розподіл користувачів ОВА та КП за регіонами")

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
        f"❌ Файл `{file_name}` не знайдено! Переконайтеся, що він лежить у"
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
    st.warning("⚠️ Не знайдено даних.")
    st.stop()

# --- ГРАФІК ---
st.subheader(
    ":material/stacked_bar_chart: Об'єкти національного значення в єПам'ятці"
)
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
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
    ),
)
st.plotly_chart(fig_comp, use_container_width=True, config=plot_config)
