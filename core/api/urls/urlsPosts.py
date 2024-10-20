from django.urls import path
from ..interface import viewsPosts
from ..interface import viewsComments


urlpatterns = [
        path("posts", viewsPosts.posts, name="posts"),
        path("posts/toggle-like/<str:postID>", viewsPosts.posts_toggle_like, name="postsToggleLike"),
        path("posts/<str:postID>", viewsPosts.posts_param, name="posts_param"),
]
