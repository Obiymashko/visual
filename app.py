import streamlit as st

# Використовуємо старе ім'я файла, щоб Streamlit його знайшов, але новий заголовок "Музейний реєстр"
page1 = st.Page(
    "pages/1_🏛️_Нерухомі_пам'ятки.py",
    title="Нерухомі пам'ятки",
    icon="🏛️",
    default=True,
)
page2 = st.Page(
    "pages/2_🖼️_Музеї_РМФУ.py", title="Музейний реєстр", icon="🖼️"
)

pg = st.navigation([page1, page2])
pg.run()
