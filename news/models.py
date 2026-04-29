from django.contrib.auth.models import AbstractUser
from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('journalist', 'Journalist'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    subscribed_publishers = models.ManyToManyField(
        Publisher,
        blank=True,
        related_name='subscribers'
    )

    subscribed_journalists = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='reader_subscribers'
    )

    def __str__(self):
        return self.username


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='articles'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='newsletters'
    )

    articles = models.ManyToManyField(Article, blank=True)

    def __str__(self):
        return self.title