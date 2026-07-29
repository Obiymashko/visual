import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Налаштування сторінки
st.set_page_config(page_title="Дашборд: ЄПам'ятка", layout="wide")

plot_config = {
    'displayModeBar': True,
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'chart_export',
        'height': 720,
        'width': 1280,
        'scale': 3 
    }
}

st.title("🏛️ Моніторинг внесення нерухомих пам'яток")
st.markdown("Аналітика наповнення Реєстру та карток в системі ЄПам'ятка.")

# --- БЛОК ВИБОРУ ФАЙЛІВ ТА ВКЛАДОК ---
current_dir = os.getcwd()
excel_files = [f for f in os.listdir(current_dir) if f.endswith(('.xlsx', '.xls')) and not f.startswith('~$')]

if not excel_files:
    st.warning("У цій папці не знайдено Excel-файлів. Додайте таблиці та оновіть сторінку.")
    st.stop()

st.sidebar.header("⚙️ Навігація")
selected_file = st.sidebar.selectbox("📂 Оберіть файл:", excel_files)

try:
    file_path = os.path.join(current_dir, selected_file)
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
except Exception as e:
    st.error(f"Помилка зчитування файлу: {e}")
    st.stop()

selected_sheet = st.sidebar.selectbox("📑 Оберіть вкладку:", sheet_names)

# --- БЛОК АВТОМАТИЧНОЇ ОБРОБКИ ДАНИХ ---
@st.cache_data
def load_and_clean_data(path, sheet):
    df_raw = pd.read_excel(path, sheet_name=sheet)
    
    # Розумний пошук колонок
    c_reg, c_reestr, c_drafts_all, c_drafts_nac, c_cards = -1, -1, -1, -1, -1
    
    for i, col in enumerate(df_raw.columns):
        text = str(col).lower()
        for r in range(min(3, len(df_raw))):
            text += " " + str(df_raw.iloc[r, i]).lower()
            
        if "регіон" in text or "область" in text:
            if c_reg == -1: c_reg = i
        elif "реєстр" in text or "мінкульт" in text:
            if c_reestr == -1: c_reestr = i
        elif "чернеток" in text and "всього" in text:
            c_drafts_all = i
        elif "чернеток" in text and ("національного" in text or "нац" in text):
            c_drafts_nac = i
        elif "карток" in text and "національного" in text and "відсоток" not in text:
            c_cards = i
            
    # Запасний варіант, якщо шапка не розпізнана
    if c_reg == -1: c_reg = 1
    if c_reestr == -1: c_reestr = 2
    if c_cards == -1: c_cards = len(df_raw.columns) - 1
        
    # Шукаємо рядок з якого починаються дані (Вінницька обл.)
    start_row = 1
    for r in range(min(10, len(df_raw))):
        if "вінницька" in str(df_raw.iloc[r, c_reg]).lower():
            start_row = r
            break
            
    data = df_raw.iloc[start_row:].copy()
    
    # Створюємо чистий датафрейм
    df = pd.DataFrame({
        'Регіон': data.iloc[:, c_reg].astype(str),
        'Об\'єкти в Реєстрі': pd.to_numeric(data.iloc[:, c_reestr], errors='coerce').fillna(0),
        'Картки в ЄПам\'ятка': pd.to_numeric(data.iloc[:, c_cards], errors='coerce').fillna(0)
    })
    
    if c_drafts_all != -1:
        df['Чернетки (всього)'] = pd.to_numeric(data.iloc[:, c_drafts_all], errors='coerce').fillna(0)
        
    if c_drafts_nac != -1:
        df['Чернетки (нац. значення)'] = pd.to_numeric(data.iloc[:, c_drafts_nac], errors='coerce').fillna(0)
        
    # Жорсткий відсікач сміття знизу ("Всього", "Разом" і т.д.)
    end_idx = len(df)
    for i, val in enumerate(df['Регіон']):
        val_str = str(val).lower().strip()
        if val_str.startswith('всього') or val_str.startswith('разом'):
            end_idx = i
            break
            
    df = df.iloc[:end_idx]
    
    # Додаткова чистка порожніх або коротких значень
    df = df.dropna(subset=['Регіон'])
    df = df[df['Регіон'].str.lower() != 'nan']
    df = df[df['Регіон'].str.len() > 3]
    
    # Рахуємо відсоток
    df['Відсоток виконання (%)'] = np.where(
        df['Об\'єкти в Реєстрі'] > 0,
        (df['Картки в ЄПам\'ятка'] / df['Об\'єкти в Реєстрі']) * 100,
        0
    )
    
    # Впорядкуємо колонки для красивого відображення в таблиці
    cols_order = ['Регіон', 'Об\'єкти в Реєстрі']
    if 'Чернетки (всього)' in df.columns: cols_order.append('Чернетки (всього)')
    if 'Чернетки (нац. значення)' in df.columns: cols_order.append('Чернетки (нац. значення)')
    cols_order.extend(['Картки в ЄПам\'ятка', 'Відсоток виконання (%)'])
    df = df[cols_order]
    
    return df.sort_values(by='Відсоток виконання (%)', ascending=True)

# --- ВІЗУАЛІЗАЦІЯ ---
try:
    df = load_and_clean_data(file_path, selected_sheet)
    
    if df.empty:
        st.warning("⚠️ Не знайдено даних для аналізу на цій вкладці.")
        st.stop()
        
    # Основні метрики
    tot_reestr = int(df['Об\'єкти в Реєстрі'].sum())
    tot_cards = int(df['Картки в ЄПам\'ятка'].sum())
    avg_perc = (tot_cards / tot_reestr * 100) if tot_reestr > 0 else 0
    
    # Динамічно визначаємо кількість колонок для метрик
    num_metrics = 3
    if 'Чернетки (всього)' in df.columns: num_metrics += 1
    if 'Чернетки (нац. значення)' in df.columns: num_metrics += 1
        
    cols_metric = st.columns(num_metrics)
    
    idx = 0
    cols_metric[idx].metric("🏛️ Об'єктів у Реєстрі Мінкульту", f"{tot_reestr:,}")
    idx += 1
    cols_metric[idx].metric("✅ Внесено карток в ЄПам'ятка", f"{tot_cards:,}")
    idx += 1
    if 'Чернетки (всього)' in df.columns:
        cols_metric[idx].metric("📝 Чернеток (всього)", f"{int(df['Чернетки (всього)'].sum()):,}")
        idx += 1
    if 'Чернетки (нац. значення)' in df.columns:
        cols_metric[idx].metric("📝 Чернеток (нац. значення)", f"{int(df['Чернетки (нац. значення)'].sum()):,}")
        idx += 1
        
    cols_metric[idx].metric("📈 Загальний прогрес", f"{avg_perc:.1f}%")
        
    st.divider()

    # Інтерактивна таблиця
    st.subheader("📋 Детальна таблиця (натисніть на назву колонки для сортування)")
    st.dataframe(
        df.sort_values(by='Відсоток виконання (%)', ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Відсоток виконання (%)": st.column_config.ProgressColumn(
                "Відсоток виконання (%)",
                format="%.1f%%",
                min_value=0,
                max_value=100 if df['Відсоток виконання (%)'].max() <= 100 else int(df['Відсоток виконання (%)'].max()),
            ),
        }
    )
    st.divider()

    # Барчарт Рейтинг областей
    st.subheader("🏆 Рейтинг областей за відсотком виконання")
    fig_bar = px.bar(
        df, x='Відсоток виконання (%)', y='Регіон', orientation='h',
        text=df['Відсоток виконання (%)'].apply(lambda x: f"{x:.1f}%"), 
        color='Відсоток виконання (%)',
        color_continuous_scale='RdYlGn', height=750
    )
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(template="plotly_white", margin=dict(l=0, r=50, t=30, b=0),
                          xaxis_title="% Внесено карток", yaxis_title="", coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True, config=plot_config)
    st.divider()

    # Барчарт План-Факт
    st.subheader("📊 Порівняння: Реєстр Мінкульту vs Картки в ЄПам'ятка")
    # Сортуємо по кількості об'єктів у реєстрі для красивішого графіка
    df_sorted_abs = df.sort_values(by='Об\'єкти в Реєстрі', ascending=False)
    
    fig_compare = go.Figure()
    fig_compare.add_trace(go.Bar(x=df_sorted_abs['Регіон'], y=df_sorted_abs['Об\'єкти в Реєстрі'], name='Об\'єкти в Реєстрі', marker_color='#d1d5db'))
    fig_compare.add_trace(go.Bar(x=df_sorted_abs['Регіон'], y=df_sorted_abs['Картки в ЄПам\'ятка'], name='Внесено в ЄПам\'ятка', marker_color='#3b82f6'))
    
    fig_compare.update_layout(barmode='group', template="plotly_white", height=500,
                              xaxis_tickangle=-45, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_compare, use_container_width=True, config=plot_config)

except Exception as e:
    st.error(f"Виникла помилка під час обробки даних: {e}")