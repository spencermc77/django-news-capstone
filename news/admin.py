from django.contrib import admin
from .models import CustomUser, Article, Publisher, Newsletter

admin.site.register(CustomUser)
admin.site.register(Article)
admin.site.register(Publisher)
admin.site.register(Newsletter)