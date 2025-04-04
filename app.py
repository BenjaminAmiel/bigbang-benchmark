
import streamlit as st
import json
import os

st.set_page_config(page_title="Big Bang Benchmark", layout="wide")

st.title("🌌 Big Bang Benchmark – Résultats du modèle")

# Tentatives de chemins possibles
possible_paths = [
    "evaluation_results.json",
    "./evaluation_results.json",
    "../evaluation_results.json",
    os.path.join(os.getcwd(), "evaluation_results.json")
]

data = None
for path in possible_paths:
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
        break

if not data:
    st.error("Aucun fichier de résultats trouvé (evaluation_results.json manquant).")
    st.stop()

st.success(f"{len(data)} questions évaluées")

for item in data:
    st.markdown(f"#### ❓ {item['question']}")
    st.markdown(f"- ✅ Réponse attendue : `{item['expected']}`")
    st.markdown(f"- 💬 Réponse du modèle : `{item['response']}`")
    st.markdown(f"- ✔️ Correct : `{item['correct']}`")
    if item["similarity"] is not None:
        st.markdown(f"- 📊 Similarité : `{item['similarity']:.4f}`")
    st.markdown("---")
