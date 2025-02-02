from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import FAQ
from django.core.cache import cache
from googletrans import Translator

translator = Translator()

class FAQModelTest(TestCase):

    def test_create_faq(self):
        """Test creating a FAQ instance."""
        faq = FAQ.objects.create(
            question="What is Django?",
            answer="<p>Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.</p>"
        )
        self.assertEqual(faq.question, "What is Django?")
        self.assertTrue(faq.answer.startswith("<p>Django is"))
        self.assertEqual(str(faq), "What is Django?")

    def test_faq_fields(self):
        """Test that FAQ model fields are defined correctly."""
        faq = FAQ(question="How to install Django?", answer="<p>Use pip to install Django.</p>")
        self.assertEqual(faq.question, "How to install Django?")
        self.assertEqual(faq.answer, "<p>Use pip to install Django.</p>")

    def test_faq_str_method(self):
        """Test the __str__ method of the FAQ model."""
        faq = FAQ.objects.create(
            question="What is Python?",
            answer="<p>Python is an interpreted, high-level, general-purpose programming language.</p>"
        )
        self.assertEqual(str(faq), "What is Python?")


class FAQAPITest(TestCase):

    def setUp(self):
        """Create a few FAQ entries for testing."""
        self.client = APIClient()
        self.faq1 = FAQ.objects.create(
            question="What is Django?",
            answer="<p>Django is a high-level Python web framework.</p>"
        )
        self.faq2 = FAQ.objects.create(
            question="How to install Django?",
            answer="<p>Use pip to install Django.</p>"
        )

    def test_get_faqs_without_lang(self):
        """Test the GET request for FAQs without specifying a language."""
        response = self.client.get('/api/faqs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        faqs = response.data
        print("Response Status:", response.status_code)
        print("Response Data:", faqs)

        self.assertEqual(len(faqs), 2)
        self.assertEqual(faqs[0]['question'], "What is Django?")
        self.assertTrue(faqs[0]['answer'].startswith("<p>Django is"))

    def test_get_faqs_with_lang(self):
        """Test the GET request for FAQs with a specific language."""
        response = self.client.get('/api/faqs/', {'lang': 'es'})  # Spanish
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        faqs = response.data
        print("Response Status:", response.status_code)
        print("Response Data:", faqs)

        # Translate question and answer using Google Translate
        translated_question = translator.translate("What is Django?", dest='es').text
        translated_answer = translator.translate("<p>Django is a high-level Python web framework.</p>", dest='es').text

        # Normalize text for comparison
        self.assertEqual(faqs[0]['question'].strip().lower(), translated_question.strip().lower())
        self.assertEqual(faqs[0]['answer'].strip().lower(), translated_answer.strip().lower())

    def test_cache_translation(self):
        """Test that translations are cached correctly."""
        cache_key_question = f'faq_{self.faq1.id}_question_es'
        cache_key_answer = f'faq_{self.faq1.id}_answer_es'

        cache.clear()  # Ensure cache is empty before testing
        self.assertIsNone(cache.get(cache_key_question))
        self.assertIsNone(cache.get(cache_key_answer))

        # Make GET request with lang='es'
        self.client.get('/api/faqs/', {'lang': 'es'})

        # Check if cache is now storing the translation
        self.assertIsNotNone(cache.get(cache_key_question), "Cache key for question is not being set!")
        self.assertIsNotNone(cache.get(cache_key_answer), "Cache key for answer is not being set!")

    def test_post_faq(self):
        """Test the POST request to create a new FAQ."""
        data = {
            'question': "What is Python?",
            'answer': "<p>Python is an interpreted, high-level, general-purpose programming language.</p>"
        }
        response = self.client.post('/api/faqs/', data, format='json')
        print("Response Status:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['question'], "What is Python?")
        self.assertEqual(response.data['answer'], "<p>Python is an interpreted, high-level, general-purpose programming language.</p>")

def test_invalid_post_faq(self):
    """Test the POST request with invalid data."""
    data = {
        'question': "",  # Empty question should trigger validation error
        'answer': "<p>Python is a programming language.</p>"
    }
    response = self.client.post('/api/faqs/', data, format='json')

    print("Response Status:", response.status_code)
    print("Response Data:", response.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('question', response.data)
    self.assertEqual(response.data['question'][0], "This field may not be blank.")

