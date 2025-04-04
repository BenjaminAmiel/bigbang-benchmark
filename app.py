
import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Big Bang Benchmark", layout="wide")
st.title("🌌 Big Bang Benchmark – Résultats du modèle")

# Chargement du fichier
results_path = Path(__file__).resolve().parent.parent / "evaluation_results.json"
if not results_path.exists():
    st.error("Aucun fichier de résultats trouvé (evaluation_results.json manquant).")
    st.stop()

with open(results_path) as f:
    data = json.load(f)

st.markdown(f"**{len(data)} questions évaluées**")

correct_answers = sum(1 for item in data if item.get("correct"))
accuracy = correct_answers / len(data) * 100
st.metric(label="🎯 Taux d'exactitude", value=f"{accuracy:.2f}%")

show_errors = st.checkbox("Afficher uniquement les erreurs", value=False)

for item in data:
    if show_errors and item.get("correct", False):
        continue

    st.markdown("----")
    st.markdown(f"**🧠 Question :** {item['question']}")
    st.markdown(f"**✅ Attendu :** {item['expected']}")
    st.markdown(f"**🤖 Réponse générée :** {item['response']}")
    st.markdown(f"**🎯 Correct :** {'✔️ Oui' if item.get('correct') else '❌ Non'}")
    if item.get("similarity") is not None:
        st.markdown(f"**📐 Similarité :** {round(item['similarity'], 4)}")
