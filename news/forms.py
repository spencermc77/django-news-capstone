from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Article, Newsletter, Publisher, CustomUser


class RegisterForm(UserCreationForm):
    """Form used to register a new user with a selected role."""

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']


class ArticleForm(forms.ModelForm):
    """Form used to create and edit articles."""

    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']


class NewsletterForm(forms.ModelForm):
    """Form used to create and edit newsletters."""

    class Meta:
        model = Newsletter
        fields = ['title', 'description', 'articles']


class PublisherForm(forms.ModelForm):
    """Form used to create publishers."""

    class Meta:
        model = Publisher
        fields = ['name']


class SubscriptionForm(forms.ModelForm):
    """Form used by readers to subscribe to publishers and journalists."""

    class Meta:
        model = CustomUser
        fields = ['subscribed_publishers', 'subscribed_journalists']