import os
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from templates.answer import answer_dict as message
from django.http import JsonResponse
from services.logService import LogException


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


# Метод для администратора
@csrf_exempt
def admin(request):
    try:
        # импорт необходимого файла и запуск процессе генерации
        from services.generate2 import start 
        
        response = start(request)

    except Exception as er:
        response = message[400].copy()
        response["error"] = f"{er}"
        LogException.write_data(er, "39", "Generate testing data", "Уникальные ошибки", "admin", "info", response,
                                "admins/generate-test-data", "GET", "400")

    return JsonResponse(response, status=response.get("status", 200))