import streamlit as st 
import numpy as np 


st.title("GAME PAGE", icon ="🎮")
st.header("Welcome to a new Game of Guess Who!") 


if "number_of_games_played" not in st.session_state:
    st.session_state["number_of_games_played"] = 0

if "needed_guesses_list" not in st.session_state: 
    st.session_state["needed_guesses_list"]= []

if "current_number_of_guesses" not in st.session_state: 
    st.session_state["current_number_of_guesses"] = 0

if "game_started" not in st.session_state:
    st.session_state["game_started"] = False

if st.session_state["game_started"] == False and st.session_state["number_of_games_played"] == 0:
    if st.button("Start the Game!"):
        st.session_state["game_started"] = True

if "player_to_guess" not in st.session_state and st.session_state["game_started"] == True:
    st.session_state["player_to_guess"] = np.random.randint(1,24)
    st.session_state["number_of_games_played"] += 1
    st.info("The Game has started!A new player to guess has been generated!")


st.subheader("Overview of Characters")


pictures = ["01_Anna.png", "02_Ben.png", "03_Carla.png", "04_David.png", 
            "05_Fiona.png", "06_Emre.png", "07_Hana.png", "08_Gustav.png", 
            "09_Jule.png", "10_Ibrahim.png", "11_Mia.png", "12_Karim.png",
            "13_Lena.png", "14_Oskar.png", "15_Nia.png", "16_Marco.png",
            "17_Rosa.png", "18_Leo.png", "19_Paula.png", "20_Quentin.png", 
            "21_Tara.png", "22_Sven.png", "23_Vera.png", "24_Wei.png"]

grid = st.grid(columns = 12, wrap = False, border = True, height = 600)
for i in range(24):
    with grid.cell():
        st.image(f"pictures/{pictures[i]}", width = 200)
        st.checkbox(f"Player {i+1}?")

with st.form("Guess the Player"):
    guess = st.number_input(min_value = 1, max_value = 24, step = 1, 
                            label = "Who do you think is the player to guess? Please enter the player number (1-24):")
    submitted = st.form_submit_button("Submit") 

if st.session_state["game_started"] == True and submitted:
    st.session_state["current_number_of_guesses"] += 1
    if guess == int(st.session_state['player_to_guess']):
        st.success(f"Great! You did it in {st.session_state['current_number_of_guesses']} guesses! The player to guess was Player {st.session_state['player_to_guess']}.")
        st.session_state["needed_guesses_list"].append(st.session_state["current_number_of_guesses"])
        st.session_state["current_number_of_guesses"] = 0
        st.session_state["game_started"] = False

    else:
        st.error(f"Your {st.session_state['current_number_of_guesses']} . guess: Person Number {guess}, was wrong. Please try again.")
        st.info(f"Debug info: The number is {st.session_state['player_to_guess']}")
elif st.session_state["number_of_games_played"] != 0: 
    st.error("Please start a new game to guess the player.")

if st.session_state["number_of_games_played"] != 0:
    if st.button("Start a new game"):
        if st.session_state["game_started"] == False:
            st.session_state["player_to_guess"] = np.random.randint(1,24)
            st.session_state["number_of_games_played"] += 1
            st.session_state["game_started"] = True
            st.info("A new player to guess has been generated!")
        else: 
            st.error("You are already playing a game. Please finish the current game before starting a new one.")

if st.button("Go to Stats Page"):
    st.switch_page("stats-page.py")