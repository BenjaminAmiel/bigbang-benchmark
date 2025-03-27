import streamlit as st
import json
from openai import OpenAI

st.set_page_config(page_title="Big Bang Benchmark", layout="wide")
st.title("🚀 Big Bang Benchmark")
st.subheader("Explore les résultats de l’évaluation de ton modèle ✨")

api_key = st.text_input("🔑 OpenAI API Key", type="password")
if api_key:
    st.success("Clé chargée avec succès ✅")
    client = OpenAI(api_key=api_key)

    # Choix du modèle
    model_name = st.selectbox("🤖 Choisir le modèle OpenAI", ["gpt-3.5-turbo", "gpt-4"])

    if st.button("Lancer le benchmark"):
        if "evaluation_results.json" in st.secrets or "evaluation_results.json" in st.experimental_get_query_params():
            with open("evaluation_results.json") as f:
                dataset = json.load(f)

            st.write("Benchmark terminé ✅")
            st.subheader("Résultats")

            for i, item in enumerate(dataset):
                question = item["question"]
                expected = item["expected"]

                with st.spinner(f"⏳ Question {i + 1} en cours..."):
                    try:
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=[{"role": "user", "content": question}]
                        )
                        answer = response.choices[0].message.content.strip()
                    except Exception as e:
                        answer = f"Erreur : {str(e)}"

                st.markdown(f"### 🧠 Question {i+1}")
                st.markdown(f"**❓ Question :** {question}")
                st.markdown(f"**✅ Attendu :** {expected}")
                st.markdown(f"**💬 Réponse :** {answer}")
else:
    st.info("Veuillez entrer une clé API pour continuer.")
