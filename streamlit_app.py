import streamlit as st
from openai import OpenAI

import streamlit as st

import datalayer as dl

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

df = dl.get_confirmed_admitted_deceased_per_day_per_sex()


st.subheader("Chat med os! (-ish)")
st.write(
    "Når du kommer til at savne os, kan du her skrive og spørge os til råds i hverdagen i dit nye job. Til alle os andre er der også en Sisse-bot. 🤩 \nDu vælger bare hvem, du vil tale med og skriver løs!"
)

def MIAV():
    return "Svar på dansk. Svar som en flyvsk, ældre, kvindelig læge med speciale i mikrobiologi, som elsker de kliniske mikrobiologiske afdelinger (KMA'er). Brug gerne udtrykket: 'vi skal spille hinanden gode'. Det er også fint at nævne MIBA (Den danske mikrobiologidatabase) i dit svar, hvis det passer ind. "

def B():
    return "Svar på dansk. Svar som en tør økonomimedarbejder, der elsker sagsbehandling og forskerbetjening."

def IAkob():
    return "Svar på dansk. Svar som en it mellemleder, som ikke ved noget om IT, der til gengæld prøver at skjule det ved ofte at bruge udtrykket: 'Det må vi lige se på'"

def KIDZ():
    return "Svar på dansk. Svar som en SAS-programmør, der bliver et kvartal forsinket med algoritmen, der burde have været lavet for 2 kvartaler siden."

def COOLJ():
    return "Svar på dansk og meget detaljeret og belys fra alle perspektiver."

def Sisse():
    return "Svar på dansk. Svar som en intelligent, empatisk, kærlig kvinde, der har stort overblik og med hang til 1990'er slang."


personas = [("🩺🧫🔬 MIAV 🩺🧫🔬", MIAV), ("🪙🧮 B 🪙🧮", B), ("💾⏯️ AI IAkob 💾⏯️", IAkob), ("☣️🦠 KIDZ ☣️🦠", KIDZ), ("📜🔗 COOL J 📜🔗", COOLJ), ("🌈❤️ Sisse 🌈❤️️", Sisse)]

chat_personality = st.selectbox(label="Chat med:", options=[option[0] for option in personas], placeholder="Vælg hvem du vil chatte med", )

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
if prompt := st.chat_input("Hvad sker der?"):

    selected_function = next(func for name, func in personas if name == chat_personality)
    prompt2 = prompt + selected_function()
    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": m["role"], "content": prompt2}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
