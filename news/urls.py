from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('articles/', views.article_list, name='article_list'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/pending/', views.pending_articles, name='pending_articles'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('articles/<int:article_id>/approve/', views.approve_article, name='approve_article'),

    path('newsletters/', views.newsletter_list, name='newsletter_list'),
    path('newsletters/create/', views.create_newsletter, name='create_newsletter'),
    path('newsletters/<int:newsletter_id>/', views.newsletter_detail, name='newsletter_detail'),

    path('api/articles/', views.api_articles),
    path('api/articles/subscribed/', views.api_subscribed_articles),
    path('api/articles/<int:article_id>/', views.api_article_detail),
    path('api/approved/', views.api_approved_notification),
]