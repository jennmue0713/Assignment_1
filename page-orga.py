import streamlit as st
 
def orga_page(): 
    st.title("Orga")

pg = st.navigation(pages=["main-page.py","game-page.py","stats-page.py", orga_page])
pg.run()

