
import streamlit as st
import json
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Big Bang Benchmark", layout="wide")

st.title("🌌 Big Bang Benchmark – Résultats du modèle")

# Chargement du fichier de résultats
results_path = Path(__file__).resolve().parent.parent / "evaluation_results.json"

if not results_path.exists():
    st.error("Aucun fichier de résultats trouvé (evaluation_results.json manquant).")
    st.stop()

with open(results_path) as f:
    data = json.load(f)

# Mise en forme des données pour affichage
for item in data:
    item["similarity"] = round(item["similarity"], 4) if item.get("similarity") else None

df = pd.DataFrame(data)
accuracy = df["correct"].mean() * 100 if not df.empty else 0

st.markdown(f"**{len(df)} questions évaluées**")
st.metric(label="🎯 Taux d'exactitude", value=f"{accuracy:.2f}%")

# Ajout d'un filtre pour afficher uniquement les erreurs
show_errors = st.checkbox("Afficher uniquement les erreurs", value=False)
if show_errors:
    df = df[df["correct"] == False]

# Affichage du tableau enrichi
st.dataframe(df[["question", "expected", "response", "correct", "similarity"]], use_container_width=True)
