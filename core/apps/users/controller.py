from templates.answer import answer_dict as message
from apps.users.models import User
from services.encriptionService import Encriptions
from django.http.multipartparser import MultiPartParser
from services.authService import Authorization
from services.parserService import Separement


def registration_users(request) -> dict:
    """
    Create a new user in the DB.
    """

    # Получение данных из запроса    
    request_data = MultiPartParser(request.META, request, request.upload_handlers).parse()

    user_data = {'id' : Encriptions.generate_string(30, User),
         'first_name' : request_data[0].get("firstName"),
          'last_name' : request_data[0].get("lastName"), 
          'user_name' : request_data[0].get("userName"), 
              'email' : request_data[0].get("email"),
           'password' : request_data[0].get("password"),
              'media' : request_data[1].get("avatar"),
          'tags_list' : request_data[0].get("tags")}
    
    # Создание нового пользователя
    try:
        result = User.create_user(user_data)

    except Exception as er:
        return message[500]
    
    return result


def user_profile(request, id_profile=""):
    cookie_user = Authorization.is_authorization(request)
    
    if id_profile:
        try:    
            user_profile = User.objects.get(id=id_profile)

        except Exception as er:
            return message[404]
        
        response = Separement.user_information(user_profile, cookie_user, status="guest")
        return response
    
    else:
        if isinstance(cookie_user, dict):
            return message[401]
        
        response = Separement.user_information(cookie_user, status="owner")
        return response["user"]
    

        
