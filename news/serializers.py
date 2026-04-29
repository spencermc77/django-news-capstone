from rest_framework import serializers
from .models import Article, Newsletter, Publisher, CustomUser


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    publisher_id = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.all(),
        source='publisher',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'author',
            'publisher',
            'publisher_id',
            'created_at',
            'approved',
            'approved_at',
        ]
        read_only_fields = ['approved', 'approved_at', 'created_at']


class NewsletterSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    articles = ArticleSerializer(many=True, read_only=True)
    article_ids = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all(),
        source='articles',
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Newsletter
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'author',
            'articles',
            'article_ids',
        ]
        read_only_fields = ['created_at']