import json
import os
import re
import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

# 🔐 Clé API récupérée depuis la variable d'environnement
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔣 Normalisation douce pour comparaison sémantique
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

# ✨ Obtenir les embeddings vectoriels pour le score sémantique
def get_embedding(text):
    embedding = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return np.array(embedding.data[0].embedding)

# 🧠 Évaluation complète du modèle
def evaluate(model, dataset, similarity_threshold=0.15):
    results = []
    for item in dataset:
        question = item['question']
        expected = item['answer']
        response = model(question)

        print("🧪 Normalized expected:", normalize(expected))
        print("🧪 Normalized response:", normalize(response))

        norm_expected = normalize(expected)
        norm_response = normalize(response)

        if norm_expected in norm_response:
            score = 1.0
        else:
            emb_expected = get_embedding(expected)
            emb_response = get_embedding(response)
            similarity = cosine_similarity([emb_expected], [emb_response])[0][0]
            print(f"🔁 Similarity score: {similarity:.4f}")
            score = round(float(similarity), 4)

        is_correct = score >= similarity_threshold

        results.append({
            'question': question,
            'expected': expected,
            'response': response,
            'score': score,
            'correct': bool(is_correct)
        })
    return results

# 🔁 Le modèle GPT à tester
def gpt_model(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# 📄 Exemple de dataset
dataset = [
    {'question': "What is the answer to life, the universe and everything?", 'answer': "42"},
    {'question': "What is two plus two?", 'answer': "4"},
    # ajoute tes autres questions ici si tu veux
]

if __name__ == "__main__":
    results = evaluate(gpt_model, dataset)
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("✅ Benchmark terminé. Résultats enregistrés dans evaluation_results.json.")