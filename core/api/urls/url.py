from django.urls import path
from ..interface import views


urlpatterns = [
    path('media/webp/content/<path:file_path>', views.serve_webp_content, name='serve_webp'), # Отправка изображения постов
    path('media/webp/avatars/<path:file_path>', views.serve_webp_avatars, name='serve_webp'), # Отправка изображения аватаров
    path("admins/generate-test-data", views.admin, name="test-data") # Генерация тестовых данных (необходим файл generate)
]
