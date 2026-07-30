import streamlit as st

# Визначаємо наші сторінки. default=True робить сторінку стартовою
page1 = st.Page("pages/1_Monuments.py", title="Нерухомі пам'ятки", icon="🏛️", default=True)
page2 = st.Page("pages/2_Museums.py", title="Музеї РМФУ", icon="🖼️")

# Формуємо нове чисте меню
pg = st.navigation([page1, page2])

# Запускаємо
pg.run()
