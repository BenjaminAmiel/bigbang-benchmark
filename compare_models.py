
import streamlit as st
import openai
import os

st.set_page_config(page_title="Comparateur de modèles OpenAI", layout="wide")
st.title("🤖 Comparateur de modèles OpenAI")

api_key = st.text_input("🔑 OpenAI API Key", type="password")
if api_key:
    st.success("Clé API chargée avec succès ✅")
    openai.api_key = api_key
else:
    st.stop()

model_1 = st.selectbox("🔹 Modèle 1", ["gpt-3.5-turbo", "gpt-4"], index=0)
model_2 = st.selectbox("🔸 Modèle 2", ["gpt-3.5-turbo", "gpt-4"], index=1)

question = st.text_area("💬 Entre une question à poser aux deux modèles")

if st.button("Comparer les réponses") and question:
    with st.spinner("Génération des réponses..."):
        response_1 = openai.ChatCompletion.create(
            model=model_1,
            messages=[{"role": "user", "content": question}]
        ).choices[0].message.content.strip()

        response_2 = openai.ChatCompletion.create(
            model=model_2,
            messages=[{"role": "user", "content": question}]
        ).choices[0].message.content.strip()

    st.markdown("----")
    st.markdown(f"### 🔹 Réponse de **{model_1}**")
    st.markdown(response_1)

    st.markdown("----")
    st.markdown(f"### 🔸 Réponse de **{model_2}**")
    st.markdown(response_2)
