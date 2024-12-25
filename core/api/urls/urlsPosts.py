from django.urls import path
from ..interface import viewsPosts
from ..interface import viewsComments


urlpatterns = [
        # posts
        path("posts", viewsPosts.posts, name="posts"),
        path("posts/toggle-like/<str:ID>", viewsPosts.posts_toggle_like, name="postsToggleLike"),
        path("posts/<str:postID>", viewsPosts.posts_param, name="posts_param"),

        # comments
        path("comments/<str:ID>", viewsComments.comments, name="comments"),
        path("comments/toggle-like/<str:commentID>", viewsComments.toggle_like, name="like")
]
