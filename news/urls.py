from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='news/login.html'),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout',
    ),

    path('subscriptions/', views.manage_subscriptions, name='manage_subscriptions'),

    path('articles/', views.article_list, name='article_list'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/pending/', views.pending_articles, name='pending_articles'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('articles/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('articles/<int:article_id>/delete/', views.delete_article, name='delete_article'),
    path('articles/<int:article_id>/approve/', views.approve_article, name='approve_article'),

    path('newsletters/', views.newsletter_list, name='newsletter_list'),
    path('newsletters/create/', views.create_newsletter, name='create_newsletter'),
    path('newsletters/<int:newsletter_id>/', views.newsletter_detail, name='newsletter_detail'),
    path('newsletters/<int:newsletter_id>/edit/', views.edit_newsletter, name='edit_newsletter'),
    path('newsletters/<int:newsletter_id>/delete/', views.delete_newsletter, name='delete_newsletter'),

    path('publishers/', views.publisher_list, name='publisher_list'),
    path('publishers/create/', views.create_publisher, name='create_publisher'),

    path('api/articles/', views.api_articles),
    path('api/articles/subscribed/', views.api_subscribed_articles),
    path('api/articles/<int:article_id>/', views.api_article_detail),
    path('api/approved/', views.api_approved_notification),
]