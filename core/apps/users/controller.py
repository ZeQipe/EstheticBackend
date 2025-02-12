from templates.answer import answer_dict as message
from apps.users.models import User
from services.encriptionService import Encriptions
from django.http.multipartparser import MultiPartParser
from services.authService import Authorization
from services.parserService import Separement
from services.logService import LogException


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
    try: 
        user = User.create_user(user_data)

    except Exception as er: 
        LogException.write_data(er, "23", "user -- controller", "Ошибка при обращении к модели", 
                "registration_users", "warning", user_data, "users/registration", "POST", "500")
        
        return message[500]

    # Формирование ответа
    try: 
        if isinstance(user, User): 
            response = Separement.user_information(user, status="owner")
        
        else: 
            response = user
    
    except Exception as er:
            LogException.write_data(er, "33", "user -- controller", "Ошибка при формировании ответа", "registration_users", 
                                "warning", f"user: {user_data} -- type: {type(user)}", "users/registration", "POST", "500")
            
            response = message[500]
    
    return response


def user_profile(request, id_profile="") -> dict:
    # Поиск пользователя в базе данных по кукам
    cookie_user = Authorization.is_authorization(request)

    # Два варианта возврата данных
    if id_profile:

        # Поиск пользователя по ID
        try: 
            user_profile = User.objects.get(id=id_profile)
        
        except Exception as er: 
            LogException.write_data(er, "57", "user -- controller", "Ошибка при обращении к базе данных", "user_profile", "warning",
                                    f"id_profile: {id_profile}", "users/public-profile/<str:userID>" , "GET", "404")
            
            return message[404]

        # Формирование ответа
        try:
            response = Separement.user_information(user_profile, cookie_user=cookie_user)

        except Exception as er:
            LogException.write_data(er, "67", "user -- controller", "Ошибка при формировании ответа", "user_profile", "warning", 
                                    f"user_profile_type: {type(user_profile)}", "users/public-profile/<str:userID>", "GET", "500")
        
            return message[500]

    else:
        # Поиск пользователя по кукам
        if isinstance(cookie_user, dict): 
            LogException.write_data(er, "78", "user -- controller", "Ошибка авторизации", "user_profile", "info", 
                                    f"user_profile: {type(cookie_user)}",  "users/private-profile", "GET", "404")
            
            return message[404]

        # Формирование ответа
        try:
            response = Separement.user_information(cookie_user, status="owner")

        except Exception as er:
            LogException.write_data(er, "85", "user -- controller", "Ошибка при формировании ответа", "user_profile", "warning", 
                                    f"user_profile: {type(cookie_user)} -- {cookie_user}", "users/private-profile", "GET", "500")

            response = message[500]

    return response


def edit_user_data(request):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка изменить данные не своего аккаунта", "100", "user -- controller", "Ошибка авторизации", 
                                "edit_user_data", "info", f"user_profile_type: {type(cookie_user)} -- {cookie_user}", "users/", "PUT", "401")
        
        return message[401]

    # Формируем информацию о пользователе
    put_data = MultiPartParser(request.META, request, request.upload_handlers).parse()
    user_data = {'first_name' : put_data[0].get("firstName"),
                  'last_name' : put_data[0].get("lastName"),
                  'user_name' : put_data[0].get("userName"),
                  'tags_list' : put_data[0].get("tags"),
                      'media' : put_data[1].get("avatar")}

    # Отправляем в базу данных запрос
    try: 
        return User.change_user(cookie_user, user_data)
    
    except Exception as er: 
        LogException.write_data(er, "115", "user -- controller", "Ошибка при обращении к модели", "edit_user_data", "warning", 
                                f"user_profile_type: {type(cookie_user)} -- {user_data}", "users/", "PUT", "500")
        
        return message[500]


def user_created_post_list(request, userID):
    # Получаем query параметры offset и limit из запроса
    offset, limit = Separement.pagination_parametrs(request)

    # Поиск пользователя в базе данных
    try: 
        user = User.objects.get(id=userID)

    except Exception as er:
        response = message[404].copy()
        response['message'] = "Not found User"
        LogException.write_data(er, "130", "user -- controller", "Ошибка при обращении к базе данных", "user_created_post_list", "warning", 
                                f"user_profile_type: {type(user)}", "users/<str:userID>/created-posts", "GET", "404")

        return response

    # Получение постов, созданных пользователем
    posts_user = user.posts.all()
    count = user.posts.all().count()

    # Формирование ответа
    try:
        response = Separement.formatted_posts(posts_user, count)
    
    except Exception as er:
        LogException.write_data(er, "146", "user -- controller", "Ошибка при формировании ответа", "user_created_post_list", "warning", 
                                f"posts_user: {posts_user} -- count: {count}", "users/<str:userID>/created-posts", "GET", "500")
        
        return message[500]
    
    return response


def delete_users_avatar(request):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): 
        LogException.write_data("Попытка изменить данные не своего аккаунта", "100", "user -- controller", "Ошибка авторизации", 
                                "edit_user_data", "info", f"user_profile_type: {type(cookie_user)} -- {cookie_user}", "users/", "PUT", "401")
        
    if not cookie_user.avatar:
        return message[400]
    
    if cookie_user.delete_avatars():
        return message[200]
    
    else:
        return message[500]