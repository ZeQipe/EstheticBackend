import os
from django.http import HttpResponse, Http404
from django.conf import settings

def serve_webp_avatars(request, file_path):
    # Получаем полный путь к файлу
    file_full_path = os.path.join(settings.MEDIA_ROOT, "webp", "avatars", file_path)

    # Проверяем, существует ли файл
    if not os.path.exists(file_full_path): raise Http404("Файл не найден")

    # Открываем файл и отправляем его с правильным заголовком
    with open(file_full_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='image/webp')
        return response


def serve_webp_content(request, file_path):
    # Получаем полный путь к файлу
    file_full_path = os.path.join(settings.MEDIA_ROOT, "webp", "content", file_path)

    # Проверяем, существует ли файл
    if not os.path.exists(file_full_path): raise Http404("Файл не найден")

    # Открываем файл и отправляем его с правильным заголовком
    with open(file_full_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='image/webp')
        return response
