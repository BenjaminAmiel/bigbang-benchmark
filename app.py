
import streamlit as st
import json
import os

# Obtenir le chemin absolu du dossier contenant app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_PATH = os.path.join(BASE_DIR, "evaluation_results.json")

st.set_page_config(page_title="Big Bang Benchmark", layout="wide")

st.title("🌌 Big Bang Benchmark – Résultats du modèle")

if not os.path.exists(RESULTS_PATH):
    st.error("Aucun fichier de résultats trouvé (evaluation_results.json manquant).")
    st.stop()

with open(RESULTS_PATH) as f:
    results = json.load(f)

st.success(f"{len(results)} questions évaluées")

for item in results:
    st.markdown(f"**❓ {item['question']}**")
    st.markdown(f"✅ Réponse attendue : `{item['expected']}`")
    st.markdown(f"💬 Réponse du modèle : {item['response']}")
    st.markdown(f"✔️ Correct : `{item['is_correct']}`")
    st.markdown(f"📊 Similarité : `{item['similarity']:.4f}`")
    st.markdown("---")
