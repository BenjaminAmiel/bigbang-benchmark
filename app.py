import streamlit as st
import json
import os
from openai import OpenAI

st.set_page_config(page_title="Big Bang Benchmark", layout="wide")

st.title("🚀 Big Bang Benchmark")
api_key = st.text_input("🔑 OpenAI API Key", type="password")

if api_key:
    st.success("Clé chargée avec succès ✅")
    client = OpenAI(api_key=api_key)

    model = st.selectbox("🤖 Choisir le modèle OpenAI", ["gpt-3.5-turbo", "gpt-4"])

    if os.path.exists("evaluation_results.json"):
        with open("evaluation_results.json") as f:
            dataset = json.load(f)

        st.subheader("✨ Explore les résultats de l’évaluation de ton modèle")

        for i, item in enumerate(dataset):
            question = item["question"]
            expected = item["expected"]

            with st.spinner(f"🔄 Question {i+1} en cours de traitement…"):
                completion = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": question}]
                )
                response = completion.choices[0].message.content.strip()

            st.markdown(f"### 🧠 Question {i+1}")
            st.markdown(f"**❓ Question :** {question}")
            st.markdown(f"**✅ Attendu :** {expected}")
            st.markdown(f"**💬 Réponse :** {response}")
            st.markdown("---")
else:
    st.info("Veuillez entrer une clé API pour continuer.")
