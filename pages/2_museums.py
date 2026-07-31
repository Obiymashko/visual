import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Дашборд: Музейний реєстр", layout="wide")

# Точне налаштування CSS: Адаптація під світлу/темну тему та збереження іконок
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0');

/* Глобальний Montserrat */
html, body, [class*="st-"], .stMarkdown, .stTable, .stDataFrame, h1, h2, h3, h4, h5, h6, p, div, span, li {
    font-family: 'Montserrat', sans-serif !important;
}

/* 🔥 РЯТУЄМО ІКОНКИ STREAMLIT 🔥 */
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

/* Plotly шрифти */
.js-plotly-plot .plotly text,
.js-plotly-plot .plotly .hovertext,
.js-plotly-plot .plotly .gtitle,
.js-plotly-plot .plotly .xtitle,
.js-plotly-plot .plotly .ytitle {
    font-family: 'Montserrat', sans-serif !important;
}

/* --- ПРОКАЧАНИЙ ДИЗАЙН КАРТОК (Адаптивний під теми) --- */
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
    opacity: 0.7; /* Замість жорсткого кольору використовуємо прозорість для підтримки темної теми */
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
    background-color: rgba(22, 163, 74, 0.15); /* Прозорий фон для темної теми */
    padding: 4px 10px;
    border-radius: 6px;
}

.red-alert-tag {
    font-family: 'Montserrat', sans-serif !important;
    color: #ef4444;
    font-size: 13px;
    font-weight: 800;
    margin-top: 0px;
    margin-bottom: 15px;
    background-color: rgba(239, 68, 68, 0.15); /* Прозорий фон для темної теми */
    padding: 8px 12px;
    border-radius: 6px;
    line-height: 1.4;
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
    box-sizing: border-box; /* Ідеальне вирівнювання крапок з рамкою та без */
}
</style>
""",
    unsafe_allow_html=True,
)

plot_config = {
    "displayModeBar": False,
    "toImageButtonOptions": {"format": "png", "filename": "chart", "height": 720, "width": 1280, "scale": 3},
}

def clean_chart_layout(fig, height=220):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=20, t=10, b=10),
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
            marker=dict(line=dict(color='rgba(0,0,0,0)', width=2)) # Видалили жорстку білу лінію для темної теми
        )
    return fig

# --- ШАПКА ---
st.title("РЕЄСТР МУЗЕЙНИХ ПРЕДМЕТІВ")
st.caption("**Дані актуальні на 29.07.2026**")
st.write("") # Додатковий відступ

# =====================================================================
# 1. ЗАВАНТАЖЕННЯ ДАНИХ
# =====================================================================
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir) if os.path.basename(current_dir) == "pages" else current_dir

file_name = "РМФУ ВНЕСЕНО ПО ОБЛАСТЯХ_2.xlsx"
file_path = os.path.join(parent_dir, file_name)

if not os.path.exists(file_path):
    file_name = "РМФУ ВНЕСЕНО ПО ОБЛАСТЯХ.xlsx"
    file_path = os.path.join(parent_dir, file_name)

if not os.path.exists(file_path):
    st.error("Не знайдено файл з даними у папці проєкту!")
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
            if col in m_df.columns:
                m_df[col] = pd.to_numeric(m_df[col], errors="coerce").fillna(0)
            else:
                m_df[col] = 0

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

total_museums = int(df_summary['Кількість музеїв'].sum())
total_vneseno = int(df_summary['Внесено предметів'].sum())

# Згідно ТЗ: фіксуємо кількість предметів, що залишилось внести
total_potribno = 10898203
# Перераховуємо загальну кількість, щоб діаграма та відсотки були на 100% точними
total_items = total_vneseno + total_potribno
perc_total = (total_vneseno / total_items * 100) if total_items > 0 else 0

osn_vneseno = int(df_summary['Основний фонд (внесено)'].sum())
osn_pidpysano = int(df_summary['Основний фонд (підписано)'].sum())
spec_vneseno = int(df_summary['Спецфонд (внесено)'].sum())
spec_pidpysano = int(df_summary['Спецфонд (підписано)'].sum())

mus_completed = len(df_museums[df_museums["Прогрес (%)"] >= 99.9])
mus_not_started = len(df_museums[df_museums["Прогрес (%)"] == 0])
mus_in_progress = total_museums - mus_completed - mus_not_started

# =====================================================================
# 2. КАРТКИ ДАШБОРДУ
# =====================================================================

# --- КАРТКА 1: Загальний стан (Музеї + Предмети) ---
colors_items = ["#16A34A", "#F59E0B"]
with st.container(border=True):
    col1, col2, col3 = st.columns([1.8, 2.0, 1.2], vertical_alignment="center")
    with col1:
        st.markdown(
            f"""
            <div class='left-stat-block'>
                <div class='stat-title'>Всього музейних предметів (за звітами)</div>
                <h1 class='big-number'>{total_items:,}</h1>
                <div class='green-tag'>↑ {perc_total:.1f}% загальний прогрес внесення</div>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors_items[0]};'></span>Внесено до реєстру: <b>{total_vneseno:,}</b></li>
                <li><span class='color-dot' style='background-color: {colors_items[1]};'></span>Залишилось внести: <b>{total_potribno:,}</b></li>
            </ul>
            """, unsafe_allow_html=True
        )
    with col3:
        fig1 = go.Figure(data=[go.Pie(labels=["Внесено", "Залишилось"], values=[total_vneseno, total_potribno], hole=0.6, marker_colors=colors_items)])
        st.plotly_chart(clean_chart_layout(fig1), use_container_width=True, config=plot_config)

# --- КАРТКА 2: Фонди (Груповий Bar Chart) ---
colors_funds = ["#3b82f6", "#06b6d4"]
with st.container(border=True):
    col1, col2, col3 = st.columns([1.8, 2.0, 1.2], vertical_alignment="center")
    with col1:
        st.markdown(
            f"""
            <div class='left-stat-block'>
                <div class='stat-title'>Внесено до системи</div>
                <h1 class='big-number'>{total_vneseno:,}</h1>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors_funds[0]};'></span>Основний фонд (внесено): <b>{osn_vneseno:,}</b></li>
                <li><span class='color-dot' style='background-color: transparent; border: 2px solid {colors_funds[0]};'></span>Основний фонд (підписано КЕП): <b>{osn_pidpysano:,}</b></li>
                <li><span class='color-dot' style='background-color: {colors_funds[1]};'></span>Спецфонд (внесено): <b>{spec_vneseno:,}</b></li>
                <li><span class='color-dot' style='background-color: transparent; border: 2px solid {colors_funds[1]};'></span>Спецфонд (підписано КЕП): <b>{spec_pidpysano:,}</b></li>
            </ul>
            """, unsafe_allow_html=True
        )
    with col3:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            y=['Спецфонд', 'Осн. фонд'], x=[spec_vneseno, osn_vneseno], 
            name='Внесено', orientation='h', marker_color='#94a3b8',
            text=[f"{spec_vneseno:,}", f"{osn_vneseno:,}"], textposition='auto'
        ))
        fig2.add_trace(go.Bar(
            y=['Спецфонд', 'Осн. фонд'], x=[spec_pidpysano, osn_pidpysano], 
            name='Підписано КЕП', orientation='h', marker_color='#3b82f6',
            text=[f"{spec_pidpysano:,}", f"{osn_pidpysano:,}"], textposition='auto'
        ))
        fig2.update_layout(
            barmode='group',
            height=200,
            margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Montserrat, sans-serif", size=13),
            showlegend=False, # Видалили легенду
            xaxis=dict(visible=False),
            yaxis=dict(title="", tickfont=dict(size=14, weight="bold"))
        )
        st.plotly_chart(fig2, use_container_width=True, config=plot_config)

# --- КАРТКА 3: Всього музеїв у реєстрі ---
colors_mus = ["#ef4444", "#3b82f6", "#10b981"] # Не розпочали -> В процесі -> Завершили
with st.container(border=True):
    col1, col2, col3 = st.columns([1.8, 2.0, 1.2], vertical_alignment="center")
    with col1:
        st.markdown(
            f"""
            <div class='left-stat-block'>
                <div class='stat-title'>Всього музейних установ У РЕЄСТРІ</div>
                <h1 class='big-number'>{total_museums:,}</h1>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class='red-alert-tag'>⚠️ 104 МУЗЕЙНІ УСТАНОВИ ДЕРЖАВНОГО ЗНАЧЕННЯ ПЕРЕБУВАЮТЬ НА ТИМЧАСОВО ОКУПОВАНИХ ТЕРИТОРІЯХ</div>
            <ul class='sub-list' style='margin-bottom: 16px !important;'>
                <li><span class='color-dot' style='background-color: #8b5cf6;'></span>Музеї держ. значення: <b>409</b></li>
                <li><span class='color-dot' style='background-color: #cbd5e1;'></span>Інші музеї: <b>{total_museums - 409}</b></li>
            </ul>
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors_mus[2]};'></span>Завершили наповнення (100%): <b>{mus_completed:,}</b></li>
                <li><span class='color-dot' style='background-color: {colors_mus[1]};'></span>В процесі наповнення (1-99%): <b>{mus_in_progress:,}</b></li>
                <li><span class='color-dot' style='background-color: {colors_mus[0]};'></span>Ще не розпочали (0%): <b>{mus_not_started:,}</b></li>
            </ul>
            """, unsafe_allow_html=True
        )
    with col3:
        fig3 = go.Figure(go.Funnel(
            y=["Не розпочали", "В процесі", "Завершили"],
            x=[mus_not_started, mus_in_progress, mus_completed],
            textinfo="value",
            marker={"color": colors_mus}
        ))
        st.plotly_chart(clean_chart_layout(fig3, height=220), use_container_width=True, config=plot_config)

# --- КАРТКА 4: Викрадені / зниклі предмети ---
colors_missing = ["#dc2626", "#ea580c", "#f59e0b", "#94a3b8"]
val_stolen = 448
val_search = 471
val_not_found = 187
val_ww2 = 13
total_missing = val_stolen + val_search + val_not_found + val_ww2

with st.container(border=True):
    col1, col2, col3 = st.columns([1.8, 2.0, 1.2], vertical_alignment="center")
    with col1:
        st.markdown(
            f"""
            <div class='left-stat-block'>
                <div class='stat-title'>Викрадені / зниклі предмети</div>
                <h1 class='big-number'>{total_missing:,}</h1>
                <div class='red-alert-tag' style='margin-top: 4px; padding: 4px 10px;'>зафіксовано втрати</div>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <ul class='sub-list'>
                <li><span class='color-dot' style='background-color: {colors_missing[0]};'></span>Викрадено: <b>{val_stolen:,}</b></li>
                <li><span class='color-dot' style='background-color: {colors_missing[1]};'></span>У національному розшуку: <b>{val_search:,}</b></li>
                <li><span class='color-dot' style='background-color: {colors_missing[2]};'></span>Не виявлено під час звірення: <b>{val_not_found:,}</b></li>
                <li><span class='color-dot' style='background-color: {colors_missing[3]};'></span>Втрачено під час Другої світової війни: <b>{val_ww2:,}</b></li>
            </ul>
            """, unsafe_allow_html=True
        )
    with col3:
        labels_missing = ["Викрадено", "В розшуку", "Не виявлено", "Втрачено (ДСВ)"]
        values_missing = [val_stolen, val_search, val_not_found, val_ww2]
        fig5 = go.Figure(data=[go.Pie(labels=labels_missing, values=values_missing, hole=0.6, marker_colors=colors_missing)])
        st.plotly_chart(clean_chart_layout(fig5, height=220), use_container_width=True, config=plot_config)

st.divider()

# =====================================================================
# 3. ГРАФІК ПО ОБЛАСТЯХ (На всю ширину)
# =====================================================================

st.subheader("Топ областей за кількістю внесених предметів")
df_top = df_summary.sort_values(by="Внесено предметів", ascending=True)

fig_top = px.bar(
    df_top,
    x="Внесено предметів",
    y="Регіон",
    orientation="h",
    text=df_top["Внесено предметів"].apply(lambda x: f"{x:,}"),
    color="Внесено предметів",
    color_continuous_scale="Viridis",
    height=800,
)
fig_top.update_traces(textposition="outside", textfont_size=13, textfont_family="Montserrat, sans-serif")
fig_top.update_layout(
    margin=dict(l=0, r=60, t=30, b=0),
    coloraxis_showscale=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Montserrat, sans-serif", size=14),
    xaxis_title="",
    yaxis_title="",
)
st.plotly_chart(fig_top, use_container_width=True, config=plot_config)
