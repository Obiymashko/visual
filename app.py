import streamlit as st

# Вказуємо ТОЧНІ шляхи до ваших файлів, включаючи емодзі та кирилицю
page1 = st.Page("pages/1_🏛️_Нерухомі_пам'ятки.py", title="Нерухомі пам'ятки", icon="🏛️", default=True)
page2 = st.Page("pages/2_🖼️_Музеї_РМФУ.py", title="Музеї РМФУ", icon="🖼️")

pg = st.navigation([page1, page2])
pg.run()
