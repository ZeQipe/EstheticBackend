from django.db import models
from django.utils import timezone


class User(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    user_name = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    password = models.TextField()
    avatar = models.TextField(unique=True, blank=True, null=True)
    tags_user = models.JSONField(default=list)
    subscribers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    @staticmethod
    def create_user(data):
        pass

    