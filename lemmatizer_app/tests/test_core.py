from django.test import SimpleTestCase

from lemmatizer_app.core import lemmatize_many, lemmatize_verb, normalize_word


class LemmatizerCoreTests(SimpleTestCase):
    def test_normalize_word_unifies_apostrophes(self):
        self.assertEqual(normalize_word("тарпыдинзь\"") , "тарпыдинзь’")

    def test_lemmatize_verb_returns_candidates(self):
        result = lemmatize_verb("тарпыдинзь")
        self.assertTrue(result["candidates"])
        self.assertEqual(result["candidates"][0]["lemma"], "тарпы")

    def test_lemmatize_many_splits_text(self):
        results = lemmatize_many("тарпыдинзь\nханась")
        self.assertEqual(len(results), 2)
