import json
import re
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def semantic_similarity(a, b):
    vectorizer = TfidfVectorizer().fit([a, b])
    vectors = vectorizer.transform([a, b])
    return cosine_similarity(vectors[0], vectors[1])[0][0]

def gpt_model(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def evaluate(model, dataset):
    results = []
    for item in dataset:
        question = item['question']
        expected = item['answer']
        response = model(question)

        norm_expected = normalize(expected)
        norm_response = normalize(response)

        is_correct = norm_expected in norm_response
        result = {
            'question': question,
            'expected': expected,
            'response': response,
            'correct': is_correct
        }

        if not is_correct:
            score = semantic_similarity(norm_expected, norm_response)
            result['similarity_score'] = round(score, 4)
            print(f"🔁 Similarity score: {result['similarity_score']}")
        else:
            print("🎯 Correct")

        results.append(result)

    return results

if __name__ == "__main__":
    with open("dataset.json") as f:
        dataset = json.load(f)

    results = evaluate(gpt_model, dataset)

    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Benchmark terminé. Résultats enregistrés dans evaluation_results.json.")
