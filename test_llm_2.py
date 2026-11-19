import streamlit as st
from openai import OpenAI
import numpy as np 
import pandas as pd

st.title("Test Chat")

if "player_to_guess" not in st.session_state:
    st.session_state["player_to_guess"] = np.random.randint(0,23)
dataset = pd.read_csv("characters.csv")
st.write(f"current player:{st.session_state["player_to_guess"]+1}")

if "player_information" not in st.session_state:
    player_row = dataset.iloc[st.session_state["player_to_guess"]].to_dict()
    st.session_state["player_information"] = "\n".join(f"{key}: {value};" for key, value in player_row.items())

st.write(st.session_state["player_information"])


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
    api_key=api_key
)



system_prompt = f"You are a chatbot that is supposed to give the user hints in a 'Guess Who' guessing game. The user should only ask yes or no questions about the character that is the current character to be guessed. If the user input is not a yes or no question, please answer accordingly. If the user asks questions that you cannot answer or if he repeats a question, please state that. Use the following data: {st.session_state["player_information"]}. Answer the questions based on the data provided. "


# Initialize chat history and give context and Instructions to the LLM
if "messages" not in st.session_state: 
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
# Generate the LLM Response to the user input 
def generate_response(): 
    response_choices = client.chat.completions.create(
                model="Qwen/Qwen3.8-27B-FP8",
                messages= st.session_state.messages
            )
    return response_choices.choices[0].message.content



# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
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
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})