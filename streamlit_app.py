import streamlit as st
from openai import OpenAI

import streamlit as st

st.title("🎉 Sisse's dashboard! 🎉")

st.image("assest/sisse_drotner.jfif", caption="De bedste ønsker på din videre vej!")

skills = {
    "Overblik": 10,
    "Problemløsning": 10,
    "Forskerbetjening": 8,
    "Koordination": 10,
    "Hunde": 10
}

st.subheader("Skillz")
for skill, rating in skills.items():
    st.progress(rating / 10)

    st.text(f"{skill}: {rating}/10")

# Personal Message
st.write("Tak for dit årvågne øjne (og når det sejlede for meget, skarpe tunge)! Alt det bedste til dig fremover. 🚀")


st.subheader("Chat med os! (-ish)")
st.write(
    "Når du kommer til at savne os, kan du her skrive og spørge os til råds i hverdagen i dit nye job. "
    "Du vælger bare hvem, du vil tale med og skriver løs!"
)

personas = ["MIAV", "B", "'det-må-vi-lige-se'kob", "KIDZ", "COOL J"]

chat_personality = st.selectbox(label="Chat med:", options=personas, placeholder="Vælg hvem du vil chatte med", )

api_key = st.secrets["api_key"]

client = OpenAI(api_key=api_key)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
