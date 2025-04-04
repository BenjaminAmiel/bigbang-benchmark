import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Comparateur de modèles Big Bang", layout="centered")

st.title("🤖 Comparateur de modèles OpenAI")

api_key = st.text_input("🔑 OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)
    st.success("Clé API chargée avec succès ✅")

    model_1 = st.selectbox("🔹 Modèle 1", ["gpt-3.5-turbo", "gpt-4"])
    model_2 = st.selectbox("🔸 Modèle 2", ["gpt-3.5-turbo", "gpt-4"])

    question = st.text_area("💬 Entre une question à poser aux deux modèles")

    if st.button("Comparer les modèles"):
        if question.strip() == "":
            st.warning("Veuillez entrer une question.")
        else:
            with st.spinner("Envoi aux modèles..."):
                response_1 = client.chat.completions.create(
                    model=model_1,
                    messages=[{"role": "user", "content": question}]
                )
                response_2 = client.chat.completions.create(
                    model=model_2,
                    messages=[{"role": "user", "content": question}]
                )

                answer_1 = response_1.choices[0].message.content.strip()
                answer_2 = response_2.choices[0].message.content.strip()

            st.subheader("🔹 Réponse du Modèle 1")
            st.code(answer_1)

            st.subheader("🔸 Réponse du Modèle 2")
            st.code(answer_2)
else:
    st.info("Veuillez entrer votre clé OpenAI pour activer la comparaison.")