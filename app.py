import streamlit as st
import openai
import json
import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Interface Streamlit
def normalize(text):
    text = text.lower()
    word_to_digit = {
        "zero": "0", "one": "1", "two": "2", "three": "3",
        "four": "4", "five": "5", "six": "6", "seven": "7",
        "eight": "8", "nine": "9"
    }
    digit_to_word = {v: k for k, v in word_to_digit.items()}
    for word, digit in word_to_digit.items():
        text = text.replace(word, digit)
    for digit, word in digit_to_word.items():
        text = text.replace(digit, word)
    return re.sub(r'[^a-z0-9]', '', text)

def fixed_fake_embedding(text, length=20):
    base = [ord(c) % 5 for c in text]
    if len(base) < length:
        base += [0] * (length - len(base))
    else:
        base = base[:length]
    return np.array(base)

def evaluate_openai_model(api_key, model_name, dataset):
    openai.api_key = api_key
    results = []
    for item in dataset:
        question = item["question"]
        expected = item["answer"]
        try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[{"role": "user", "content": question}]
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"Error: {e}"

        norm_expected = normalize(expected)
        norm_response = normalize(reply)

        if norm_expected in norm_response:
            score = 1.0
        else:
            emb_expected = fixed_fake_embedding(expected)
            emb_response = fixed_fake_embedding(reply)
            similarity = cosine_similarity([emb_expected], [emb_response])[0][0]
            score = round(float(similarity), 4)

        results.append({
            "question": question,
            "expected": expected,
            "response": reply,
            "score": score,
            "correct": score >= 0.15
        })
    return results

# Streamlit UI
st.set_page_config(page_title="Big Bang Benchmark", layout="wide")
st.title("🚀 Big Bang Benchmark")

api_key = st.text_input("🔑 OpenAI API Key", type="password")
model_name = st.selectbox("🤖 Choisir le modèle OpenAI", ["gpt-3.5-turbo", "gpt-4"]) 

if api_key:
    st.success("Clé chargée avec succès ✅")

    if st.button("Lancer le benchmark"):
        with st.spinner("Évaluation en cours..."):
            dataset = [
                {"question": "What is the answer to life, the universe and everything?", "answer": "42"},
                {"question": "What is two plus two?", "answer": "4"},
                {"question": "Is water wet?", "answer": "Yes"},
                {"question": "What color is the sky?", "answer": "Blue"},
            ]
            results = evaluate_openai_model(api_key, model_name, dataset)
            st.success("Benchmark terminé ✅")
            st.write("### Résultats")
            st.dataframe(results)

else:
    st.warning("Veuillez entrer une clé API pour continuer.")
import json

# 📦 Bouton de téléchargement des résultats
if results:
    st.download_button(
        label="📥 Télécharger les résultats",
        data=json.dumps(results, indent=2),
        file_name="evaluation_results.json",
        mime="application/json"
    )
