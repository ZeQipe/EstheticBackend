from django.urls import path
from ..interface import viewsPosts
from ..interface import viewsComments


urlpatterns = [
        # posts
        path("posts", viewsPosts.posts, name="posts"), # Создание и возврат постов
        path("posts/toggle-like/<str:ID>", viewsPosts.posts_toggle_like, name="postsToggleLike"), # Установка и удаление лайка поста
        path("posts/<str:postID>", viewsPosts.posts_param, name="posts_param"), # Редактирование, удаление и детальная информация поста

        # comments
        path("comments/<str:ID>", viewsComments.comments, name="comments"), # Создание, получение, удаление и редактирование комментария
        path("comments/toggle-like/<str:commentID>", viewsComments.toggle_like, name="like") # Установка и удаления лайка поста 
]
