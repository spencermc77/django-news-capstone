"""
Tests for the News application.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import Client, TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from .models import Article


User = get_user_model()


class NewsAppTests(TestCase):
    """
    Test suite for the News application.
    """

    def setUp(self):
        """
        Create test users, groups, permissions, and a test article.
        """
        self.client = Client()

        self.editor_group, created = Group.objects.get_or_create(
            name="Editor"
        )

        self.journalist_group, created = Group.objects.get_or_create(
            name="Journalist"
        )

        add_article_permission = Permission.objects.get(
            codename="add_article"
        )

        change_article_permission = Permission.objects.get(
            codename="change_article"
        )

        delete_article_permission = Permission.objects.get(
            codename="delete_article"
        )

        approve_article_permission = Permission.objects.get(
            codename="can_approve_article"
        )

        self.editor_group.permissions.add(
            change_article_permission,
            delete_article_permission,
            approve_article_permission,
        )

        self.journalist_group.permissions.add(
            add_article_permission,
            change_article_permission,
            delete_article_permission,
        )

        self.editor_user = User.objects.create_user(
            username="editor",
            password="password123",
            role="editor",
        )

        self.journalist_user = User.objects.create_user(
            username="journalist",
            password="password123",
            role="journalist",
        )

        self.editor_user.groups.add(self.editor_group)
        self.journalist_user.groups.add(self.journalist_group)

        self.article = Article.objects.create(
            title="Test Article",
            content="Test Content",
            author=self.journalist_user,
            approved=False,
        )

    def test_api_journalist_can_create_article(self):
        """
        Test that a journalist can create an article through the API.
        """
        api_client = APIClient()
        api_client.force_authenticate(user=self.journalist_user)

        response = api_client.post(
            "/api/articles/",
            {
                "title": "New Article",
                "content": "New Content",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

    def test_article_can_be_approved(self):
        """
        Test that an editor can approve an article.
        """
        self.client.login(
            username="editor",
            password="password123",
        )

        response = self.client.post(
            reverse("approve_article", args=[self.article.id])
        )

        self.assertEqual(response.status_code, 302)

        self.article.refresh_from_db()

        self.assertTrue(self.article.approved)

    def test_editor_can_view_pending_articles(self):
        """
        Test that editors can view pending articles.
        """
        self.client.login(
            username="editor",
            password="password123",
        )

        response = self.client.get(
            reverse("pending_articles")
        )

        self.assertEqual(response.status_code, 200)

    def test_journalist_cannot_approve_article(self):
        """
        Test that journalists cannot approve articles.
        """
        self.client.login(
            username="journalist",
            password="password123",
        )

        response = self.client.post(
            reverse("approve_article", args=[self.article.id])
        )

        self.article.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.article.approved)