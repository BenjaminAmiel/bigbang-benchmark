import streamlit as st
import json
import os
import pandas as pd

# 🔍 Chargement sécurisé du fichier depuis la racine
file_path = os.path.join(os.path.dirname(__file__), "..", "evaluation_results.json")

st.title("🌌 Big Bang Benchmark – Résultats du modèle")

if not os.path.exists(file_path):
    st.error("Aucun fichier de résultats trouvé (evaluation_results.json manquant).")
    st.stop()

with open(file_path) as f:
    results = json.load(f)

df = pd.DataFrame(results)

st.success(f"{len(df)} questions évaluées")
st.dataframe(df[["question", "expected", "response", "correct", "similarity"]])

total = len(df)
correct = df["correct"].sum()
accuracy = round(correct / total * 100, 2)
st.markdown(f"### ✅ Exactitude : {accuracy}% ({correct} / {total})")

if st.checkbox("🔍 Voir uniquement les erreurs"):
    st.dataframe(df[df["correct"] == False])