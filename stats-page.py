import streamlit as st 

st.header("This is the stats page") 

if "number_of_games_played" in st.session_state:
    st.write(f"number of games played: {st.session_state['number_of_games_played']}")

if "needed_guesses_list" in st.session_state:
    st.write(f"needed guesses list: {st.session_state['needed_guesses_list']}")