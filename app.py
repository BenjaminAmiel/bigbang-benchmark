
import streamlit as st
import json
import os

st.set_page_config(page_title="Big Bang Benchmark", layout="wide")

st.title("🌌 Big Bang Benchmark – Résultats du modèle")

result_file_path = os.path.join(os.path.dirname(__file__), "..", "evaluation_results.json")

if not os.path.isfile(result_file_path):
    st.error("Aucun fichier de résultats trouvé (evaluation_results.json manquant).")
else:
    with open(result_file_path, "r") as f:
        results = json.load(f)

    st.markdown(f"**{len(results)} questions évaluées**")

    for item in results:
        with st.expander(f"❓ {item['question']}"):
            st.markdown(f"**✅ Réponse attendue :** {item['expected']}")
            st.markdown(f"**🤖 Réponse du modèle :** {item['response']}")
            if item['correct']:
                st.success("Réponse correcte ✔️")
            else:
                st.warning(f"Réponse incorrecte ❌")
                if item.get("similarity") is not None:
                    st.markdown(f"**🔁 Score de similarité :** {item['similarity']:.4f}")
