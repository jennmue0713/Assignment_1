import streamlit as st
from openai import OpenAI
import pandas as pd

st.title("ChatGPT-like clone")
dataset = pd.read_csv("characters.csv")
st.table(data = dataset)
st.write(dataset.query("id == 1"))
current_player_data = dataset.query("id == 1")


# ── ask for API Key, stop if not yet provided  ────────────────────────────────────────────
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


# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "Qwen/Qwen3.8-27B-FP8"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []




    response = f"{prompt}"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})




llm_prompt = f"You are only allowed to answer yes or no question about a character that should be guessed. Use the following data: {current_player_data}. if the question is not a yes or no question, answer with 'I am sorry, I can only answer yes or no questions.'You should only answer yes or no questions.  Answer the question based on the data provided. "
            
with st.chat_message("admin"):
    st.markdown(llm_prompt)
st.session_state.messages.append({"role": "admin", "content": llm_prompt})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask a yes or no question about your charcter!"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
# Accept user input
if human_prompt := st.chat_input("What is up?"):

    st.session_state.messages.append({"role": "user", "content": human_prompt})

    
    with st.chat_message("user"):
        st.markdown(human_prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
    #response = st.write_stream(stream)
    #st.session_state.messages.append({"role": "assistant", "content": response})