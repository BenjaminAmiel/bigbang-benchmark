import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(page_title="Big Bang Benchmark ✨", layout="centered")

st.title("Explore les résultats de l’évaluation de ton modèle ✨")

# Nouvelle méthode pour récupérer les paramètres (remplace experimental_get_query_params)
query_params = st.query_params

api_key = st.text_input("🔑 OpenAI API Key", type="password")
if api_key:
    st.success("Clé chargée avec succès ✅")

    # Choix du modèle (dans la version actuelle, uniquement pour affichage)
    model = st.selectbox("🤖 Choisir le modèle OpenAI", ["gpt-3.5-turbo", "gpt-4"])

    # Charger les résultats depuis le fichier JSON
    results_path = "../evaluation_results.json"
    if os.path.exists(results_path):
        with open(results_path) as f:
            data = json.load(f)

        df = pd.DataFrame(data)
        st.subheader("📊 Résultats du benchmark")
        st.dataframe(df[["question", "expected", "response", "correct"]])

        correct_count = df["correct"].sum()
        total = len(df)
        accuracy = (correct_count / total) * 100

        st.metric(label="🎯 Précision globale", value=f"{accuracy:.2f}%", delta=f"{correct_count}/{total} correctes")

        with st.expander("📂 Voir tous les résultats bruts"):
            st.json(data, expanded=False)
    else:
        st.warning("Aucun fichier de résultats trouvé (evaluation_results.json manquant).")
else:
    st.info("Veuillez saisir votre clé API OpenAI pour continuer.")