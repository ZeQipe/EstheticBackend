from django.urls import path
from ..interface import viewsPosts
from ..interface import viewsComments


urlpatterns = [
        path("posts", viewsPosts.posts, name="posts"),
]