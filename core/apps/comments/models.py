from django.db import models
from apps.posts.models import Post
from apps.users.models import User


class Comment(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    text = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    users_liked = models.ManyToManyField(User, related_name='liked_comments', blank=True)