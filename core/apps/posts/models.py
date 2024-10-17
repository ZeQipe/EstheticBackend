from django.db import models
from apps.users.models import User
from django.utils import timezone


class Post(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    post_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True, null=True)
    users_liked = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    type_content = models.TextField()
    url = models.TextField(unique=True)
    tags_list = models.JSONField(default=list)
    aspect_ratio = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    @staticmethod
    def create_post(data):
        pass