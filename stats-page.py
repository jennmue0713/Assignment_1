import streamlit as st 
import pandas as pd

st.title("Game Statistics", icon = '📊')
st.write("Here you can see an overview of how many games you played, how many guesses you needed to identify the hidden character and how good your guess was based on the number of questions you asked beforehand")

needed_guesses = st.session_state.get("needed_guesses_list", [])
questions_per_game = st.session_state.get("list_valid_questions", [])

# if we have data, display charts
if needed_guesses and questions_per_game:
    # turn our lists into a usable dataframe
    chart_data = pd.DataFrame({
        "Game": list(range(1, len(needed_guesses) + 1)),
        "Guesses": needed_guesses,
        "Questions": questions_per_game
    })
    # compute the averages and display different bar charts
    average_guesses = chart_data.Guesses.mean()
    average_questions = chart_data.Questions.mean()

    # display the different bar charts
    st.subheader(f"Average number of Guesses per Game: {average_guesses: .2f} ")
    st.bar_chart(data=chart_data, x="Game", y="Guesses", height=500)

    st.subheader(f"Average number of Questions per Game: {average_questions: .2f} ")
    st.bar_chart(data=chart_data, x="Game", y="Questions", height=500)

    #This bar chart shows how good your guesses were based on the number of asked questions
    st.subheader("Guesses and Questions per Game")
    st.bar_chart(data=chart_data, x="Game", y=["Guesses", "Questions"], width="stretch", height=500)
else:
    st.error("No games have been completed yet. Finish a game to see your statistics!")

if st.button("Go to Game Page"):
        st.switch_page("game-page.py")