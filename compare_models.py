import streamlit as st
import openai
import os

st.title("🤖 Comparateur de modèles OpenAI")

api_key = st.text_input("🔑 OpenAI API Key", type="password")
if api_key:
    openai.api_key = api_key
    st.success("Clé API chargée avec succès ✅")

    model_1 = st.selectbox("🔹 Modèle 1", ["gpt-3.5-turbo", "gpt-4"])
    model_2 = st.selectbox("🔸 Modèle 2", ["gpt-3.5-turbo", "gpt-4"])
    question = st.text_input("💬 Entre une question à poser aux deux modèles")

    if st.button("Comparer") and question:
        with st.spinner("Réponse du Modèle 1..."):
            response_1 = openai.chat.completions.create(
                model=model_1,
                messages=[{"role": "user", "content": question}]
            )
            answer_1 = response_1.choices[0].message.content.strip()

        with st.spinner("Réponse du Modèle 2..."):
            response_2 = openai.chat.completions.create(
                model=model_2,
                messages=[{"role": "user", "content": question}]
            )
            answer_2 = response_2.choices[0].message.content.strip()

        st.subheader("🔹 Réponse du Modèle 1")
        st.write(answer_1)

        st.subheader("🔸 Réponse du Modèle 2")
        st.write(answer_2)