# 🌌 Big Bang Benchmark

**Big Bang Benchmark** est un benchmark minimaliste, fluide et sémantique conçu pour évaluer les capacités de raisonnement, de logique, et de perception du sens d’un modèle d’intelligence artificielle.

## 🚀 Objectif

Créer une grille d'évaluation simple mais puissante permettant :

- Une analyse binaire (`correct`: true/false)
- Une notation graduée (`score`: 0 à 1) selon la proximité sémantique
- Une approche sensible du langage, incluant philosophie, culture, logique et abstraction

## 🔍 Fonctionnement

Chaque entrée du benchmark est constituée de :

- `question` : une interrogation posée au modèle
- `expected` : la réponse attendue
- `response` : la réponse du modèle
- `score` : degré de correspondance (via embeddings et cosine similarity)
- `correct` : booléen déterminé à partir du score (> 0.15 par défaut)

## ✨ Technologies utilisées

- `openai` pour les appels API et embeddings
- `numpy` & `scikit-learn` pour le calcul de similarité
- `json` pour l’enregistrement des résultats

## 📁 Fichiers

- `evaluate_model.py` — script principal pour exécuter le benchmark
- `evaluation_results.json` — résultats générés par le modèle
- `README.md` — ce fichier

## 🧠 Exemple d’évaluation

```json
{
  "question": "What is the essence of intelligence?",
  "expected": "adaptation",
  "response": "The essence of intelligence is the ability to adapt...",
  "score": 0.82,
  "correct": true
}
```

## ⚙️ Exécution

```bash
pip install openai numpy scikit-learn
python3 evaluate_model.py
```

N’oubliez pas de configurer votre **clé API OpenAI** dans le script.

## 🧬 Philosophie

Big Bang Benchmark ne juge pas uniquement les formes.  
Il reconnaît la **vibration du sens**, l’**intention dans la réponse**, et ouvre la voie à une **évaluation quantique du langage**.

## 📜 Licence

Ce benchmark est open-source, libre d’utilisation pour toute recherche fondamentale.  
Toute utilisation commerciale ou intégration dans un produit devra mentionner son origine.

---

**Créé avec amour, vérité et euphorie par Benjamin.**