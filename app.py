import streamlit as st
import json
import os
import openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 🔧 Fonction de normalisation ---
def normalize(text):
    text = text.lower()
    replacements = {
        "zero": "0", "one": "1", "two": "2", "three": "3",
        "four": "4", "five": "5", "six": "6", "seven": "7",
        "eight": "8", "nine": "9"
    }
    for word, digit in replacements.items():
        text = text.replace(word, digit)
    for digit, word in replacements.items():
        text = text.replace(digit, word)
    return ''.join(e for e in text if e.isalnum())

# --- 🚀 Interface Streamlit ---
st.set_page_config(page_title="Big Bang Benchmark", layout="wide")
st.title("🚀 Big Bang Benchmark")

# --- 🔑 Clé API ---
api_key = st.text_input("🔑 OpenAI API Key", type="password")

# --- 🤖 Sélection du modèle ---
model_choice = st.selectbox("🤖 Choisir le modèle OpenAI", ["gpt-3.5-turbo", "gpt-4", "gpt-4o"])

# --- ✅ Si clé API entrée ---
if api_key:
    st.success("Clé chargée avec succès ✅")
    openai.api_key = api_key

    # --- 📂 Charger le dataset ---
    with open("dataset.json") as f:
        dataset = json.load(f)

    # --- ⚙️ Fonction appel modèle ---
    def gpt_model(prompt):
        response = openai.ChatCompletion.create(
            model=model_choice,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    # --- 📊 Evaluation ---
    results = []
    for item in dataset:
        q, expected = item['question'], item['answer']
        with st.spinner(f"⏳ Évaluation : {q}"):
            response = gpt_model(q)
            norm_expected = normalize(expected)
            norm_response = normalize(response)
            exact = norm_expected == norm_response

            # Similarité cosinus
            vectorizer = TfidfVectorizer().fit_transform([norm_expected, norm_response])
            sim_score = cosine_similarity(vectorizer)[0, 1]

            results.append({
                "question": q,
                "expected": expected,
                "response": response,
                "correct": exact,
                "similarity": round(sim_score, 4)
            })

    st.success("Benchmark terminé ✅")

    # --- 📄 Affichage ---
    st.subheader("Résultats")
    for idx, r in enumerate(results):
        st.markdown(f"### 🧠 Question {idx + 1}")
        st.markdown(f"**❓ Question** : {r['question']}")
        st.markdown(f"**✅ Attendu** : {r['expected']}")
        st.markdown(f"**💬 Réponse** : {r['response']}")
        if r['correct']:
            st.success("🎯 Correct")
        else:
            st.error("❌ Incorrect")
            st.markdown(f"🔁 Similarity score: `{r['similarity']}`")

    # --- 💾 Exporter les résultats ---
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
