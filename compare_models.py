import streamlit as st
import json
import os
from openai import OpenAI

st.set_page_config(page_title="Big Bang Benchmark – Compare Models", layout="wide")

st.title("🧠 Big Bang Benchmark – Compare Two Models")

# API key input
api_key = st.text_input("🔑 OpenAI API Key", type="password")

if api_key:
    st.success("Clé API chargée avec succès ✅")
    client = OpenAI(api_key=api_key)

    # Model selectors
    col1, col2 = st.columns(2)
    with col1:
        model_a = st.selectbox("🤖 Modèle A", ["gpt-3.5-turbo", "gpt-4"])
    with col2:
        model_b = st.selectbox("🤖 Modèle B", ["gpt-3.5-turbo", "gpt-4"], index=1)

    # Load dataset
    if os.path.exists("evaluation_results.json"):
        with open("evaluation_results.json") as f:
            dataset = json.load(f)

        st.subheader("📊 Comparaison des réponses")

        for i, item in enumerate(dataset):
            question = item['question']
            col1, col2 = st.columns(2)

            with col1:
                with st.spinner(f"Modèle A ({model_a}) en cours…"):
                    response_a = client.chat.completions.create(
                        model=model_a,
                        messages=[{"role": "user", "content": question}]
                    ).choices[0].message.content.strip()

                st.markdown(f"### 🧠 Question {i+1}")
                st.markdown(f"**❓ Question :** {question}")
                st.markdown(f"**🔷 Réponse de {model_a} :**\n\n{response_a}")

            with col2:
                with st.spinner(f"Modèle B ({model_b}) en cours…"):
                    response_b = client.chat.completions.create(
                        model=model_b,
                        messages=[{"role": "user", "content": question}]
                    ).choices[0].message.content.strip()

                st.markdown(f"**🔶 Réponse de {model_b} :**\n\n{response_b}")

else:
    st.info("Veuillez entrer votre clé API pour démarrer.")
