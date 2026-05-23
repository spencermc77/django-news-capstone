from django.contrib.auth.models import AbstractUser
from django.db import models


class Publisher(models.Model):
    """Represents a publisher that can publish articles."""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """Custom user model with roles and subscription fields."""

    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('journalist', 'Journalist'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    subscribed_publishers = models.ManyToManyField(
        Publisher,
        blank=True,
        related_name='subscribers',
    )

    subscribed_journalists = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='reader_subscribers',
    )

    def __str__(self):
        return self.username


class Article(models.Model):
    """Represents a news article."""

    title = models.CharField(max_length=255)
    content = models.TextField()

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='articles',
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='articles',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = [
            ('can_approve_article', 'Can approve article'),
        ]

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    """Represents a newsletter containing one or more articles."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='newsletters',
    )

    articles = models.ManyToManyField(Article, blank=True)

    def __str__(self):
        return self.title