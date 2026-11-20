import streamlit as st

#not used anymore
st.title("Guess Who?", icon = '🤔')

st.markdown('''**How the Game Works:** 
- The "Guess Who?" is a guessing game where you have to guess a hidden character from a given set of characters
- You can ask yes or no questions about the character to get hints  
- You can use the checkboxes under the characters to keep track on who is still in the race 
- The goal is to guess the hidden character with as few questions and guesses possible
- ''') 
st.divider()

if st.button("start game"): 
    st.switch_page("game-page.py")



