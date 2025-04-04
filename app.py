
import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="Big Bang Benchmark", layout="centered")
st.title("🌌 Big Bang Benchmark – Résultats du modèle")

# Chargement sécurisé du fichier
try:
    with open("evaluation_results.json") as f:
        results = json.load(f)
except FileNotFoundError:
    st.error("Aucun fichier de résultats trouvé (evaluation_results.json manquant).")
    st.stop()

st.markdown(f"**{len(results)} questions évaluées**")

# Affichage détaillé des questions, réponses, et scores
for item in results:
    with st.expander(f"❓ {item['question']}"):
        st.markdown(f"**Réponse attendue :** {item['expected']}")
        st.markdown(f"**Réponse obtenue :** {item['response']}")
        st.markdown(f"**Correct :** {'✅' if item['correct'] else '❌'}")
        if item['similarity'] is not None:
            st.markdown(f"**Score de similarité :** {item['similarity']:.4f}")
