import json
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path

ANSWERS = {
    "What is the answer to life, the universe and everything?": "42",
}


def install_stubs():
    openai_mod = types.ModuleType("openai")

    class _Message:
        def __init__(self, content):
            self.content = content

    class _Choice:
        def __init__(self, content):
            self.message = _Message(content)

    class _Response:
        def __init__(self, content):
            self.choices = [_Choice(content)]

    class _Completions:
        def create(self, model, messages):
            question = messages[-1]["content"]
            return _Response(ANSWERS.get(question, "une reponse quelconque"))

    class _Chat:
        def __init__(self):
            self.completions = _Completions()

    class OpenAI:
        def __init__(self, api_key=None):
            self.chat = _Chat()

    openai_mod.OpenAI = OpenAI
    sys.modules["openai"] = openai_mod

    sklearn_mod = types.ModuleType("sklearn")
    metrics_mod = types.ModuleType("sklearn.metrics")
    pairwise_mod = types.ModuleType("sklearn.metrics.pairwise")
    pairwise_mod.cosine_similarity = lambda a, b: [[1.0]]
    feature_extraction_mod = types.ModuleType("sklearn.feature_extraction")
    text_mod = types.ModuleType("sklearn.feature_extraction.text")

    class _Vectors:
        def __init__(self, docs):
            self._docs = docs

        def toarray(self):
            return [[1.0] for _ in self._docs]

    class TfidfVectorizer:
        def fit_transform(self, docs):
            return _Vectors(docs)

    text_mod.TfidfVectorizer = TfidfVectorizer
    sklearn_mod.metrics = metrics_mod
    metrics_mod.pairwise = pairwise_mod
    sklearn_mod.feature_extraction = feature_extraction_mod
    feature_extraction_mod.text = text_mod
    sys.modules["sklearn"] = sklearn_mod
    sys.modules["sklearn.metrics"] = metrics_mod
    sys.modules["sklearn.metrics.pairwise"] = pairwise_mod
    sys.modules["sklearn.feature_extraction"] = feature_extraction_mod
    sys.modules["sklearn.feature_extraction.text"] = text_mod


install_stubs()

import evaluate_model


class EvaluateModelTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.tmp_path = Path(self.tmp.name)
        self.dataset_path = self.tmp_path / "dataset.json"
        self.results_path = self.tmp_path / "evaluation_results.json"
        shutil.copy(Path(evaluate_model.BASE_DIR) / "dataset.json", self.dataset_path)

    def run_evaluate(self):
        evaluate_model.evaluate(
            client=evaluate_model.OpenAI(),
            model="fake-model",
            dataset_path=self.dataset_path,
            results_path=self.results_path,
        )

    def test_evaluate_writes_results_with_consistent_keys(self):
        self.run_evaluate()
        results = json.loads(self.results_path.read_text())
        self.assertEqual(len(results), 2)
        for item in results:
            self.assertIn("question", item)
            self.assertIn("expected", item)
            self.assertIn("response", item)
            self.assertIn("correct", item)
            self.assertIn("similarity", item)

    def test_expected_answer_key_is_supported(self):
        self.run_evaluate()
        results = json.loads(self.results_path.read_text())
        by_question = {item["question"]: item for item in results}
        self.assertEqual(
            by_question["What is the answer to life, the universe and everything?"]["expected"],
            "42",
        )
        self.assertTrue(
            by_question["What is the answer to life, the universe and everything?"]["correct"]
        )

    def test_existing_questions_are_not_reevaluated(self):
        self.run_evaluate()
        first = json.loads(self.results_path.read_text())
        self.run_evaluate()
        second = json.loads(self.results_path.read_text())
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
