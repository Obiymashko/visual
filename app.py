import streamlit as st

# Вказуємо ТОЧНІ шляхи до ваших файлів сторінок
page1 = st.Page(
    "pages/1_🏛️_Нерухомі_пам'ятки.py",
    title="Нерухомі пам'ятки",
    icon="🏛️",
    default=True,
)
page2 = st.Page(
    "pages/2_🖼️_Музейний_реєстр.py", title="Музейний реєстр", icon="🖼️"
)

pg = st.navigation([page1, page2])
pg.run()
