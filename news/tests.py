from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from .models import Article, Publisher, Newsletter


User = get_user_model()


class NewsAppTests(TestCase):

    def setUp(self):
        self.publisher = Publisher.objects.create(name='Test Publisher')

        self.reader = User.objects.create_user(
            username='reader',
            password='testpass123',
            email='reader@example.com',
            role='reader'
        )

        self.editor = User.objects.create_user(
            username='editor',
            password='testpass123',
            email='editor@example.com',
            role='editor'
        )

        self.journalist = User.objects.create_user(
            username='journalist',
            password='testpass123',
            email='journalist@example.com',
            role='journalist'
        )

        self.article = Article.objects.create(
            title='Approved Story',
            content='This is an approved article.',
            author=self.journalist,
            publisher=self.publisher,
            approved=True,
            approved_at=timezone.now()
        )

        self.pending_article = Article.objects.create(
            title='Draft Story',
            content='This is a pending article.',
            author=self.journalist,
            publisher=self.publisher,
            approved=False
        )

        self.newsletter = Newsletter.objects.create(
            title='Weekly Newsletter',
            description='A simple test newsletter.',
            author=self.journalist
        )

        self.newsletter.articles.add(self.article)

    def test_reader_can_view_approved_articles_page(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Approved Story')

    def test_pending_article_not_shown_on_public_articles_page(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Draft Story')

    def test_editor_can_view_pending_articles(self):
        self.client.login(username='editor', password='testpass123')
        response = self.client.get('/articles/pending/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Draft Story')

    def test_article_can_be_approved(self):
        self.client.login(username='editor', password='testpass123')
        response = self.client.post(f'/articles/{self.pending_article.id}/approve/')
        self.pending_article.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.pending_article.approved)
        self.assertIsNotNone(self.pending_article.approved_at)

    def test_newsletter_page_loads(self):
        response = self.client.get('/newsletters/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Weekly Newsletter')

    def test_api_requires_authentication(self):
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 401)

    def test_api_reader_can_get_articles(self):
        api_client = APIClient()
        api_client.force_authenticate(user=self.reader)

        response = api_client.get('/api/articles/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], 'Approved Story')

    def test_api_reader_cannot_create_article(self):
        api_client = APIClient()
        api_client.force_authenticate(user=self.reader)

        response = api_client.post('/api/articles/', {
            'title': 'Reader Article',
            'content': 'Reader should not create this.',
            'publisher_id': self.publisher.id
        })

        self.assertEqual(response.status_code, 403)

    def test_api_journalist_can_create_article(self):
        api_client = APIClient()
        api_client.force_authenticate(user=self.journalist)

        response = api_client.post('/api/articles/', {
            'title': 'Journalist Article',
            'content': 'Journalist created this.',
            'publisher_id': self.publisher.id
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Journalist Article')

    def test_api_subscribed_articles(self):
        self.reader.subscribed_publishers.add(self.publisher)

        api_client = APIClient()
        api_client.force_authenticate(user=self.reader)

        response = api_client.get('/api/articles/subscribed/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], 'Approved Story')