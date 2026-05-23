import requests

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import (
    ArticleForm,
    NewsletterForm,
    PublisherForm,
    RegisterForm,
    SubscriptionForm,
)
from .models import Article, Newsletter, Publisher
from .serializers import ArticleSerializer


def home(request):
    """Display the home page."""
    return render(request, 'news/home.html')


def register(request):
    """Register a new user and add the user to the selected role group."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            role_name = user.role.capitalize()
            group, created = Group.objects.get_or_create(name=role_name)
            user.groups.add(group)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'news/register.html', {'form': form})


@login_required
def manage_subscriptions(request):
    """Allow readers to manage publisher and journalist subscriptions."""
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('manage_subscriptions')
    else:
        form = SubscriptionForm(instance=request.user)

    return render(request, 'news/manage_subscriptions.html', {'form': form})


def article_list(request):
    """Display all approved articles."""
    articles = Article.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'news/article_list.html', {'articles': articles})


def article_detail(request, article_id):
    """Display one approved article."""
    article = get_object_or_404(Article, id=article_id, approved=True)
    return render(request, 'news/article_detail.html', {'article': article})


@login_required
@permission_required('news.add_article', raise_exception=True)
def create_article(request):
    """Allow journalists to create articles."""
    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.approved = False
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()

    return render(request, 'news/create_article.html', {'form': form})


def user_can_edit_article(user, article):
    """Return True if a user can edit a specific article."""
    if user.has_perm('news.can_approve_article'):
        return True

    return article.author == user and user.has_perm('news.change_article')


def user_can_delete_article(user, article):
    """Return True if a user can delete a specific article."""
    if user.has_perm('news.can_approve_article'):
        return True

    return article.author == user and user.has_perm('news.delete_article')


@login_required
def edit_article(request, article_id):
    """Allow editors or the article author to edit an article."""
    article = get_object_or_404(Article, id=article_id)

    if not user_can_edit_article(request.user, article):
        return HttpResponseForbidden('You do not have permission to edit this article.')

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)

        if form.is_valid():
            form.save()
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'news/edit_article.html', {'form': form, 'article': article})


@login_required
def delete_article(request, article_id):
    """Allow editors or the article author to delete an article."""
    article = get_object_or_404(Article, id=article_id)

    if not user_can_delete_article(request.user, article):
        return HttpResponseForbidden('You do not have permission to delete this article.')

    if request.method == 'POST':
        article.delete()
        return redirect('article_list')

    return render(request, 'news/delete_article.html', {'article': article})


@login_required
@permission_required('news.can_approve_article', raise_exception=True)
def pending_articles(request):
    """Display articles waiting for editor approval."""
    articles = Article.objects.filter(approved=False).order_by('-created_at')
    return render(request, 'news/pending_articles.html', {'articles': articles})


def notify_subscribers(article):
    """Email subscribers when an article has been approved."""
    subscriber_emails = []

    if article.publisher:
        publisher_subscribers = article.publisher.subscribers.all()
        subscriber_emails += [
            user.email for user in publisher_subscribers if user.email
        ]

    journalist_subscribers = article.author.reader_subscribers.all()
    subscriber_emails += [
        user.email for user in journalist_subscribers if user.email
    ]

    subscriber_emails = list(set(subscriber_emails))

    if subscriber_emails:
        send_mail(
            subject=f'New approved article: {article.title}',
            message=f'A new article has been approved: {article.title}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=subscriber_emails,
            fail_silently=True,
        )


def notify_approval_api(article):
    """Send a POST request to the internal approval API endpoint."""
    try:
        requests.post(
            'http://127.0.0.1:8000/api/approved/',
            json={
                'article_id': article.id,
                'title': article.title,
                'approved_at': str(article.approved_at),
            },
            timeout=3,
        )
    except requests.RequestException:
        pass


@login_required
@permission_required('news.can_approve_article', raise_exception=True)
def approve_article(request, article_id):
    """Approve an article and trigger notifications."""
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        article.approved = True
        article.approved_at = timezone.now()
        article.save()

        notify_subscribers(article)
        notify_approval_api(article)

    return redirect('pending_articles')


def newsletter_list(request):
    """Display all newsletters."""
    newsletters = Newsletter.objects.all().order_by('-created_at')
    return render(
        request,
        'news/newsletter_list.html',
        {'newsletters': newsletters},
    )


def newsletter_detail(request, newsletter_id):
    """Display one newsletter."""
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    return render(
        request,
        'news/newsletter_detail.html',
        {'newsletter': newsletter},
    )


@login_required
@permission_required('news.add_newsletter', raise_exception=True)
def create_newsletter(request):
    """Allow journalists to create newsletters."""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)

        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            form.save_m2m()
            return redirect('newsletter_list')
    else:
        form = NewsletterForm()

    return render(request, 'news/create_newsletter.html', {'form': form})


def user_can_edit_newsletter(user, newsletter):
    """Return True if a user can edit a specific newsletter."""
    if user.has_perm('news.can_approve_article'):
        return True

    return newsletter.author == user and user.has_perm('news.change_newsletter')


def user_can_delete_newsletter(user, newsletter):
    """Return True if a user can delete a specific newsletter."""
    if user.has_perm('news.can_approve_article'):
        return True

    return newsletter.author == user and user.has_perm('news.delete_newsletter')


@login_required
def edit_newsletter(request, newsletter_id):
    """Allow editors or the newsletter author to edit a newsletter."""
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    if not user_can_edit_newsletter(request.user, newsletter):
        return HttpResponseForbidden(
            'You do not have permission to edit this newsletter.'
        )

    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=newsletter)

        if form.is_valid():
            form.save()
            return redirect('newsletter_detail', newsletter_id=newsletter.id)
    else:
        form = NewsletterForm(instance=newsletter)

    return render(
        request,
        'news/edit_newsletter.html',
        {'form': form, 'newsletter': newsletter},
    )


@login_required
def delete_newsletter(request, newsletter_id):
    """Allow editors or the newsletter author to delete a newsletter."""
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    if not user_can_delete_newsletter(request.user, newsletter):
        return HttpResponseForbidden(
            'You do not have permission to delete this newsletter.'
        )

    if request.method == 'POST':
        newsletter.delete()
        return redirect('newsletter_list')

    return render(
        request,
        'news/delete_newsletter.html',
        {'newsletter': newsletter},
    )


def publisher_list(request):
    """Display all publishers."""
    publishers = Publisher.objects.all().order_by('name')
    return render(
        request,
        'news/publisher_list.html',
        {'publishers': publishers},
    )


@login_required
@permission_required('news.add_publisher', raise_exception=True)
def create_publisher(request):
    """Allow editors to create publishers."""
    if request.method == 'POST':
        form = PublisherForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('publisher_list')
    else:
        form = PublisherForm()

    return render(request, 'news/create_publisher.html', {'form': form})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_articles(request):
    """API endpoint for listing approved articles or creating articles."""
    if request.method == 'GET':
        articles = Article.objects.filter(approved=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    if not request.user.has_perm('news.add_article'):
        return Response(
            {'error': 'Only journalists can create articles.'},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = ArticleSerializer(data=request.data)

    if serializer.is_valid():
        article = serializer.save(author=request.user)
        return Response(
            ArticleSerializer(article).data,
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_article_detail(request, article_id):
    """API endpoint for retrieving, updating, or deleting one article."""
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'GET':
        if not article.approved:
            return Response(
                {'error': 'This article is not approved yet.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    if request.method == 'PUT':
        if not user_can_edit_article(request.user, article):
            return Response(
                {'error': 'You do not have permission to update this article.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ArticleSerializer(article, data=request.data, partial=True)

        if serializer.is_valid():
            updated_article = serializer.save()
            return Response(ArticleSerializer(updated_article).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if not user_can_delete_article(request.user, article):
            return Response(
                {'error': 'You do not have permission to delete this article.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        article.delete()
        return Response(
            {'message': 'Article deleted successfully.'},
            status=status.HTTP_200_OK,
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_subscribed_articles(request):
    """Return approved articles from subscribed publishers or journalists."""
    user = request.user

    publisher_articles = Article.objects.filter(
        publisher__in=user.subscribed_publishers.all(),
        approved=True,
    )

    journalist_articles = Article.objects.filter(
        author__in=user.subscribed_journalists.all(),
        approved=True,
    )

    articles = (publisher_articles | journalist_articles).distinct()
    serializer = ArticleSerializer(articles, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def api_approved_notification(request):
    """Receive internal approval notifications."""
    return Response(
        {
            'message': 'Approval notification received',
            'data': request.data,
        },
        status=status.HTTP_200_OK,
    )