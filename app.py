
import streamlit as st
import json
import os

st.title("🌌 Big Bang Benchmark – Résultats du modèle")

# Chemin du fichier de résultats
result_file = "evaluation_results.json"

# Vérification de l'existence du fichier
if not os.path.exists(result_file):
    st.error("Aucun fichier de résultats trouvé (evaluation_results.json manquant).")
else:
    with open(result_file, "r") as f:
        results = json.load(f)

    st.markdown(f"**{len(results)} questions évaluées**")

    for item in results:
        st.markdown("----")
        st.markdown(f"❓ **{item.get('question', 'Question non disponible')}**")
        st.markdown(f"✅ **Réponse attendue :** {item.get('expected', 'Non spécifiée')}")
        st.markdown(f"💬 **Réponse du modèle :** {item.get('response', 'Aucune réponse')}")
        if 'correct' in item:
            st.markdown(f"✔️ **Correct :** {item['correct']}")
        else:
            st.markdown("✔️ **Correct :** Donnée non disponible")
        if item.get('similarity') is not None:
            st.markdown(f"📊 **Similarité :** {item['similarity']:.4f}")
        else:
            st.markdown("📊 **Similarité :** Donnée non disponible")
