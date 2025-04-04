
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Comparateur de modèles OpenAI", layout="wide")
st.title("🤖 Comparateur de modèles OpenAI")

api_key = st.text_input("🔑 OpenAI API Key", type="password")
if not api_key:
    st.stop()

client = OpenAI(api_key=api_key)
st.success("Clé API chargée avec succès ✅")

model_1 = st.selectbox("🔹 Modèle 1", ["gpt-3.5-turbo", "gpt-4"], index=0)
model_2 = st.selectbox("🔸 Modèle 2", ["gpt-3.5-turbo", "gpt-4"], index=1)

question = st.text_area("💬 Entre une question à poser aux deux modèles")

if st.button("Comparer les réponses") and question:
    with st.spinner("Génération des réponses..."):
        completion_1 = client.chat.completions.create(
            model=model_1,
            messages=[{"role": "user", "content": question}]
        )
        response_1 = completion_1.choices[0].message.content.strip()

        completion_2 = client.chat.completions.create(
            model=model_2,
            messages=[{"role": "user", "content": question}]
        )
        response_2 = completion_2.choices[0].message.content.strip()

    st.markdown("----")
    st.markdown(f"### 🔹 Réponse de **{model_1}**")
    st.markdown(response_1)

    st.markdown("----")
    st.markdown(f"### 🔸 Réponse de **{model_2}**")
    st.markdown(response_2)
