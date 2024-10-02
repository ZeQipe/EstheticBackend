from django.db import models
from apps.users.models import User
from apps.posts.models import Post
from django.utils import timezone


class Board(models.Model):
    id = models.CharField(max_length=45, primary_key=True)
    name = models.CharField(max_length=35)
    posts = models.ManyToManyField(Post, related_name='boards', blank=True)
    author = models.ForeignKey(User, related_name='boards', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    