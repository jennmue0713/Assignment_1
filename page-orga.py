import streamlit as st
 
page1 = st.Page("main-page.py", title= "Main Page")
page2 = st.Page("game-page.py", title= "Game Page")
page3 = st.Page("stats-page.py", title= "Stats Page")

pg = st.navigation(pages=[page1, page2, page3])
pg.run()

