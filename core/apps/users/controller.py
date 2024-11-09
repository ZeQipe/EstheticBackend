from templates.answer import answer_dict as message
from apps.users.models import User
from services.encriptionService import Encriptions
from django.http.multipartparser import MultiPartParser
from services.authService import Authorization
from services.parserService import Separement


def registration_users(request) -> dict:
    # Формируем информацию о пользователе
    request_data = MultiPartParser(request.META, request, request.upload_handlers).parse()
    user_data = {'id' : Encriptions.generate_string(30, User),
         'first_name' : request_data[0].get("firstName"),
          'last_name' : request_data[0].get("lastName"),
          'user_name' : request_data[0].get("userName"),
              'email' : request_data[0].get("email"),
           'password' : request_data[0].get("password"),
              'media' : request_data[1].get("avatar"),
          'tags_list' : request_data[0].get("tags")}

    # Отправляем в базу данных запрос
    try: user = User.create_user(user_data)
    except Exception: return message[500]

    # Формирование ответа
    if isinstance(user, User): response = Separement.user_information(user, status="owner")
    else: response = user
    return response


def user_profile(request, id_profile="") -> dict:
    # Поиск пользователя в базе данных по кукам
    cookie_user = Authorization.is_authorization(request)

    # Два варианта возврата данных
    if id_profile:
        # Поиск пользователя по ID
        try: user_profile = User.objects.get(id=id_profile)
        except Exception: return message[404]

        # Формирование ответа
        response = Separement.user_information(user_profile, cookie_user=cookie_user)
        return response

    else:
        # Поиск пользователя по кукам
        if isinstance(cookie_user, dict): return message[401]

        # Формирование ответа
        response = Separement.user_information(cookie_user, status="owner")
        return response


def edit_user_data(request):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]

    # Формируем информацию о пользователе
    put_data = MultiPartParser(request.META, request, request.upload_handlers).parse()
    user_data = {'first_name' : put_data[0].get("firstName"),
                  'last_name' : put_data[0].get("lastName"),
                  'user_name' : put_data[0].get("userName"),
                  'tags_list' : put_data[0].get("tags"),
                      'media' : put_data[1].get("avatar")}

    # Отправляем в базу данных запрос
    try: return User.change_user(cookie_user, user_data)
    except Exception: return message[500]


def user_created_post_list(request, userID):
    # Получаем query параметры offset и limit из запроса
    offset, limit = Separement.pagination_parametrs(request)

    # Поиск пользователя в базе данных
    try: user = User.objects.get(id=userID)
    except Exception:
        response = message[404].copy()
        response['message'] = "Not found User"
        return response

    # Получение постов, созданных пользователем
    posts_user = user.posts.all()
    count = user.posts.all().count()

    # Формирование ответа
    response = Separement.formatted_posts(posts_user, count)
    return response
