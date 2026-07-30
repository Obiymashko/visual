import streamlit as st

page1 = st.Page(
    "pages/1_🏛️_Нерухомі_пам'ятки.py",
    title="Нерухомі пам'ятки",
    default=True,
)
page2 = st.Page(
    "pages/2_🖼️_Музеї_РМФУ.py",
    title="Музейний реєстр",
)

pg = st.navigation([page1, page2])
pg.run()
