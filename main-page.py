import streamlit as st


st.title("Guess Who?", icon = '🤔')

st.header("Guess Who?", text_alignment="center")

st.write("Explanations of game rules") 
st.markdown(" **Game rules:**  :red[do not]")
st.divider()
if st.button("category 1"):
    st.error("categories do not exist yet")
st.button("category 2")

if st.button("start game"): 
    st.switch_page("game-page.py")




