import streamlit as st

# Підключаємо сторінки за їхніми новими простими системними іменами,
# але в title та icon задаємо красиве відображення для бічного меню!
page1 = st.Page(
    "pages/1_monuments.py", 
    title="Нерухомі пам'ятки", 
    icon="🏛️", 
    default=True
)

page2 = st.Page(
    "pages/2_museums.py", 
    title="Музейний реєстр", 
    icon="🖼️"
)

# Запускаємо навігацію
pg = st.navigation([page1, page2])
pg.run()
