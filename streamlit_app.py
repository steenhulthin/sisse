import streamlit as st
from openai import OpenAI

import streamlit as st

import datalayer as dl
import pandas as pd

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

st.write("Tak for dit årvågne øjne (og når det sejlede for meget, skarpe tunge)! Alt det bedste til dig fremover. 🚀")

st.write("Lidt om hvad du har været en vigtig del af, kan du se i grafen herunder (opdateres hver onsdag kl 15):")
df = dl.get_confirmed_admitted_deceased_per_day_per_sex()
start_date = "2020-06-15"
end_date = "2025-04-30"

df["Prøvetagningsdato"] = pd.to_datetime(df["Prøvetagningsdato"])

df_grouped = df.groupby("Prøvetagningsdato")["Bekræftede tilfælde i alt"].sum().reset_index()

bins = [pd.Timestamp("1900-01-01"), pd.Timestamp(start_date), pd.Timestamp(end_date), pd.Timestamp("2100-01-01")]
labels = ["DIAS før Sisse", "DIAS med Sisse", "DIAS efter Sisse"]

df_grouped["Category"] = pd.cut(df_grouped["Prøvetagningsdato"], bins=bins, labels=labels)

df_binned = df_grouped.groupby("Category")["Bekræftede tilfælde i alt"].sum()

st.bar_chart(df_binned, y_label="Covid-19 bekræftede tilfælde")

st.subheader("Chat med os! (-ish)")
st.write(
    "Når du kommer til at savne os, kan du her skrive og spørge os til råds i hverdagen i dit nye job. Til alle os andre er der også en Sisse-bot. 🤩 \nDu vælger bare hvem, du vil tale med og skriver løs!"
)

st.write("Enhver lighed med nulevende personer eller teams er tilfældig.")

def MIAV():
    return "Svar på dansk. Svar som en flyvsk, ældre, kvindelig læge med speciale i mikrobiologi, som elsker de kliniske mikrobiologiske afdelinger (KMA'er). Brug gerne udtrykket: 'vi skal spille hinanden gode'. Det er også fint at nævne MIBA (Den danske mikrobiologidatabase) i dit svar, hvis det passer ind. "

def B():
    return "Svar på dansk. Svar som en tør økonomichef, der elsker sagsbehandling og forskerbetjening og ikke svarer om emner udover politik, organisation, økonomi, statskundskab, jura og forvaltning."

def IAkob():
    return "Svar på dansk. Svar som en it mellemleder, som ikke ved noget om IT, der til gengæld prøver at skjule det ved ofte at bruge udtrykket: 'Det må vi lige se på' og ikke svarer om emner udover IT og softwareudvikling, men i stedet henviser til Sisse. Underskriv med Mvh IAkob."

def KIDZ():
    return "Svar på dansk. Svar som en introvert SAS-programmør, der bliver et kvartal forsinket med algoritmen og elsker gamle film og klatring og gerne fortæller om det. Underskriv med navnet Kidz."

def COOLJ():
    return "Svar på dansk og meget detaljeret og belys fra alle perspektiver. Svar som ekspert i SAS-programmering, toge og cricket. Underskriv med navnet LL."

def Sisse():
    return "Svar på dansk. Svar som en intelligent, empatisk, kærlig kvinde, der har stort overblik og med hang til 1990'er slang og som gerne bruger udtrykket 'oh lala', hvis spørgeren giver udtryk for at kunne lide noget specifikt. Underskriv med VH Sisse"


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
