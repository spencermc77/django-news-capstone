from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Article, Newsletter
from .forms import ArticleForm, NewsletterForm
from .serializers import ArticleSerializer


def is_editor_or_admin(user):
    return user.is_superuser or user.role == 'editor'


def home(request):
    return render(request, 'news/home.html')


def article_list(request):
    articles = Article.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'news/article_list.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id, approved=True)
    return render(request, 'news/article_detail.html', {'article': article})


@login_required
def create_article(request):
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


@login_required
@user_passes_test(is_editor_or_admin)
def pending_articles(request):
    articles = Article.objects.filter(approved=False).order_by('-created_at')
    return render(request, 'news/pending_articles.html', {'articles': articles})


@login_required
@user_passes_test(is_editor_or_admin)
def approve_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    article.approved = True
    article.approved_at = timezone.now()
    article.save()

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

    print(f'Internal API notification: Article {article.id} was approved.')

    return redirect('pending_articles')


def newsletter_list(request):
    newsletters = Newsletter.objects.all().order_by('-created_at')
    return render(request, 'news/newsletter_list.html', {'newsletters': newsletters})


def newsletter_detail(request, newsletter_id):
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    return render(request, 'news/newsletter_detail.html', {'newsletter': newsletter})


@login_required
def create_newsletter(request):
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


# ======================
# API VIEWS START HERE
# ======================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_articles(request):
    if request.method == 'GET':
        articles = Article.objects.filter(approved=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    if request.user.role != 'journalist' and not request.user.is_superuser:
        return Response(
            {'error': 'Only journalists can create articles.'},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = ArticleSerializer(data=request.data)

    if serializer.is_valid():
        article = serializer.save(author=request.user)
        return Response(ArticleSerializer(article).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'GET':
        if not article.approved:
            return Response(
                {'error': 'This article is not approved yet.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    if request.method == 'PUT':
        if request.user.role not in ['journalist', 'editor'] and not request.user.is_superuser:
            return Response(
                {'error': 'Only journalists or editors can update articles.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ArticleSerializer(article, data=request.data, partial=True)

        if serializer.is_valid():
            updated_article = serializer.save()
            return Response(ArticleSerializer(updated_article).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if request.user.role not in ['journalist', 'editor'] and not request.user.is_superuser:
            return Response(
                {'error': 'Only journalists or editors can delete articles.'},
                status=status.HTTP_403_FORBIDDEN
            )

        article.delete()
        return Response({'message': 'Article deleted successfully.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_subscribed_articles(request):
    user = request.user

    publisher_articles = Article.objects.filter(
        publisher__in=user.subscribed_publishers.all(),
        approved=True
    )

    journalist_articles = Article.objects.filter(
        author__in=user.subscribed_journalists.all(),
        approved=True
    )

    articles = (publisher_articles | journalist_articles).distinct()

    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def api_approved_notification(request):
    return Response({'message': 'Approval notification received'}, status=200)