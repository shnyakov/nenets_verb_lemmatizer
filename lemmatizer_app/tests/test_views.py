from django.test import SimpleTestCase
from django.urls import reverse


class LemmatizerViewTests(SimpleTestCase):
    def test_home_renders(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Лемматизация ненецких глагольных форм")
        self.assertContains(response, "тарпыдась")

    def test_home_returns_results_for_query(self):
        response = self.client.get(reverse("home"), {"text": "тарпыдинзь"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "тарпы")

    def test_api_returns_json(self):
        response = self.client.get(reverse("api-lemmatize"), {"text": "тарпыдинзь"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["input"], "тарпыдинзь")
        self.assertEqual(payload["results"][0]["candidates"][0]["lemma"], "тарпы")
