from django.urls import path
from ..interface import views
from django.urls import path


urlpatterns = [
    path('media/webp/content/<path:file_path>', views.serve_webp_content, name='serve_webp'),
    path('media/webp/avatars/<path:file_path>', views.serve_webp_avatars, name='serve_webp'),
]