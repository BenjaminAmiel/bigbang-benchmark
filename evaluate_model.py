import json
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def normalize_text(text):
    return ''.join(text.lower().split())

def evaluate():
    with open("dataset.json") as f:
        dataset = json.load(f)

    # Charger les résultats existants s'ils existent
    results = []
    existing_questions = set()
    if os.path.exists("evaluation_results.json"):
        with open("evaluation_results.json") as f:
            results = json.load(f)
            existing_questions = {item["question"] for item in results}

    for item in dataset:
        question = item["question"]
        expected = normalize_text(item["expected"])

        if question in existing_questions:
            print(f"⏩ Question déjà évaluée : {question}")
            continue

        print(f"💬 Évaluation de : {question}")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )

        raw_answer = response.choices[0].message.content.strip()
        normalized_answer = normalize_text(raw_answer)

        print(f"🧪 Normalized expected: {expected}")
        print(f"🧪 Normalized response: {normalized_answer}")

        correct = expected == normalized_answer

        similarity_score = None
        if not correct:
            vectorizer = TfidfVectorizer().fit_transform([expected, normalized_answer])
            vectors = vectorizer.toarray()
            similarity_score = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
            print(f"🔁 Similarity score: {similarity_score:.4f}")

        results.append({
            "question": question,
            "expected": item["expected"],
            "response": raw_answer,
            "correct": correct,
            "similarity": similarity_score
        })

    # Sauvegarder tous les résultats (anciens + nouveaux)
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Mise à jour des résultats terminée.")

if __name__ == "__main__":
    evaluate()
