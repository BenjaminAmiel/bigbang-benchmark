import json
import os
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent

def normalize_text(text):
    return ''.join(text.lower().split())

def get_expected(item):
    if "expected_answer" in item:
        return item["expected_answer"]
    return item["expected"]

def evaluate(client=None, model=None, dataset_path=None, results_path=None):
    dataset_path = Path(dataset_path) if dataset_path else BASE_DIR / "dataset.json"
    results_path = Path(results_path) if results_path else BASE_DIR / "evaluation_results.json"
    model = model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    if client is None:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with open(dataset_path) as f:
        dataset = json.load(f)

    # Charger les résultats existants s'ils existent
    results = []
    existing_questions = set()
    if results_path.exists():
        with open(results_path) as f:
            results = json.load(f)
            existing_questions = {item["question"] for item in results}

    for item in dataset:
        question = item["question"]
        raw_expected = get_expected(item)
        expected = normalize_text(raw_expected)

        if question in existing_questions:
            print(f"⏩ Question déjà évaluée : {question}")
            continue

        print(f"💬 Évaluation de : {question}")
        response = client.chat.completions.create(
            model=model,
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
            "expected": raw_expected,
            "response": raw_answer,
            "correct": correct,
            "similarity": similarity_score
        })

    # Sauvegarder tous les résultats (anciens + nouveaux)
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Mise à jour des résultats terminée.")

if __name__ == "__main__":
    evaluate()
