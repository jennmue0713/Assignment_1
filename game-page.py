import streamlit as st 
from openai import OpenAI, AuthenticationError, OpenAIError
import numpy as np 
import pandas as pd

st.title("Guess Who?", icon = '🤔')
st.subheader("How the Game works:") 
st.markdown('''
- "Guess Who?" is a guessing game where you have to guess a hidden character from a given set of characters
- You can ask yes or no questions at the input widget at the bottom to get hints about the character
- You can use the checkboxes under the characters to keep track on who is still in the race 
- If you think you might know the answer please submit the character number in the submit widget
- The goal is to guess the hidden character in as few questions and guesses as possible

**Good Luck and have Fun!**

***For the Game to function correctly, please enter a valid API key at the beginning***''') 


#get the api_key 
with st.sidebar:
    api_key = st.text_input(
        "UOS AI API-Key",
        type="password",
        key="uos_api_key",
        placeholder="sk-...",
    ).strip()

if not api_key:
    st.info("Please enter your Uni Osnabrück API key. If you don't have one, you can obtain it from https://ai-keys.uni-osnabrueck.de.")
    st.stop()

# pass the entered key
client = OpenAI(
    base_url="https://litellm.uni-osnabrueck.de/v1",
    api_key= api_key)

#Depiction of the Characters
st.subheader("Overview of Characters")

pictures = ["01_Anna.png", "02_Ben.png", "03_Carla.png", "04_David.png", 
            "05_Fiona.png", "06_Emre.png", "07_Hana.png", "08_Gustav.png", 
            "09_Jule.png", "10_Ibrahim.png", "11_Mia.png", "12_Karim.png",
            "13_Lena.png", "14_Oskar.png", "15_Nia.png", "16_Marco.png",
            "17_Rosa.png", "18_Leo.png", "19_Paula.png", "20_Quentin.png", 
            "21_Tara.png", "22_Sven.png", "23_Vera.png", "24_Wei.png"]

grid = st.grid(columns = 12, wrap = False, border = True, height = 700)
for i in range(24):
    with grid.cell():
        st.image(f"pictures/{pictures[i]}", width = 200)
        st.checkbox(f"Player {i+1}?")
st.divider()

# Initialize needed variables 
if "game_started" not in st.session_state:
    st.session_state["game_started"] = False

if "number_of_games_played" not in st.session_state:
    st.session_state["number_of_games_played"] = 0

if "needed_guesses_list" not in st.session_state: 
    st.session_state["needed_guesses_list"]= []

if "current_number_of_guesses" not in st.session_state: 
    st.session_state["current_number_of_guesses"] = 0

if "number_valid_questions" not in st.session_state: 
    st.session_state["number_valid_questions"] = 0 

if "list_valid_questions" not in st.session_state: 
    st.session_state["list_valid_questions"] = []

#What we need for our hidden character later
if "player_to_guess" not in st.session_state:
    st.session_state["player_to_guess"] = 0

#read the csv file with the character descriptions
dataset = pd.read_csv("characters.csv")

if "player_information" not in st.session_state:
    st.session_state["player_information"] = ""

# Initialize chat history
if "messages" not in st.session_state: 
    st.session_state.messages = []
    
#We need this prompt at the end of a game to extract number of valid questions from the chat
system_prompt_end = f"Please only respond to this message with the number of valid questions the user asked" 

# Generate the LLM Response to the user input 
def generate_response(): 
    try: 
        response_choices = client.chat.completions.create(
                    model="Qwen/Qwen3.8-27B-FP8",
                    messages= st.session_state.messages
                )
        return response_choices.choices[0].message.content
    
    except AuthenticationError:
            st.error("API was not accept. Please check it.")
        
    except OpenAIError:
        st.error("AI API request failed. Please check it and try again. ")
            


#Start the Game Button
if st.button("Start the Game!"):
    if st.session_state["game_started"] == False:
        st.session_state["game_started"] = True
        st.session_state["number_of_games_played"] += 1
        
        #generate a new hidden character and get its information
        st.session_state["player_to_guess"] = np.random.randint(0,23)
        player_row = dataset.iloc[st.session_state["player_to_guess"]].to_dict()
        st.session_state["player_information"] = "\n".join(f"{key}: {value};" for key, value in player_row.items())
        system_prompt = f"You are a chatbot that is supposed to give the user hints in a 'Guess Who' guessing game. The user should only ask yes or no questions about the character that is the current character to be guessed, you should only answer with yes or no to these questions. If the user input is not a yes or no question, please answer accordingly. If the user asks questions that you cannot answer or if he repeats a question, please state that. If the user asks what he has to do, please explain to him how this game works and provide two sample questions. Use the following data: {st.session_state["player_information"]}. Answer the questions based on the data provided. But if the user asks a question that has the same meaning as the data, please answer correctly. For example if the user asks if the character is a child, but the data only provides that the character is young, then that question is still a valid and correct question. If the user wants to give a concrete guess who the hidden character might be, please refer to the submit interface, where the number of the hidden character has to be entered. Don't confirm or deny it! You are only supposed to give hints about the characteristics of the character. Please keep the count on how many valid yes or no question the user asked, please state that along with your answers!"

        #for debug-purposes 
        #st.write(f"current hidden player:{st.session_state["player_to_guess"]+1}")
        #st.write(st.session_state["player_information"])
       
        #Give instructions and information to the LLM before the chat with the user begins 
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

        st.info("The Game has started! A new player to guess has been generated!")

    else: 
        st.error("You are currently playing a game. Please finish the current game before starting a new one")

# Start a game
if st.session_state["game_started"] == True: 
    st.subheader(f"Number of games played: {st.session_state["number_of_games_played"]}")
    # Display chat messages, but not the prompts given in the background
    for message in st.session_state.messages:
        if message["role"] != "system" and st.session_state["game_started"] == True:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # React to user input 
    if prompt := st.chat_input("Please ask a yes or no question about the hidden character"):
    
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        #generate response to the message 
        response = generate_response()
        
        # Display assistant response in chat message container
        if response is not None: 
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})


    # Submit button for the final character guesses 
    with st.form("Guess the Player"):
        guess = st.number_input(min_value = 1, max_value = 24, step = 1, 
                                label = "Who do you think is the player to guess? Please enter the player number (1-24):")
        submitted = st.form_submit_button("Submit") 

    if submitted:
        st.session_state["current_number_of_guesses"] += 1
        
        # Correct Guess
        if guess  == int(st.session_state['player_to_guess'] +1):
            #get the number of valid questions from the LLM
            st.session_state.messages.append({"role": "user", "content": system_prompt_end})
            valid_questions = generate_response()
            valid_questions = valid_questions.strip()
            st.session_state["number_questions_asked"] = int(valid_questions)
            st.success(f"Great! You correctly identified the hidden character. The Character to guess was Character {st.session_state['player_to_guess']+1}. You did it in {st.session_state['current_number_of_guesses']} guesses and asked {st.session_state["number_questions_asked"]} valid questions!")
            st.info("To start a new Game, please click on the 'Start the Game!' Button at the top!")
            st.balloons()
            #save number of guesses and valid questions needed for the current game and reset
            st.session_state["needed_guesses_list"].append(st.session_state["current_number_of_guesses"])
            st.session_state["current_number_of_guesses"] = 0
            st.session_state["list_valid_questions"].append(st.session_state["number_questions_asked"])
            #current game has ended
            st.session_state["game_started"] = False
            
        # Wrong Guess
        else:
            st.error(f"Your {st.session_state['current_number_of_guesses']} . guess: Person Number {guess}, was wrong. Please try again.")
            st.info(f"Debug info: The number is {st.session_state['player_to_guess']+1}")

#Switch pages to Stats Page
if st.button("Go to Stats Page"):
    st.switch_page("stats-page.py")
