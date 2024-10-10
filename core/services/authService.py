from apps.users.models import User
from services.encriptionService import Encriptions
from services.parserService import Separement
from templates.answer import answer_dict as message
import json


class Authorization:
    @staticmethod
    def login(request):
        """
        Function to validate user login data
        :param data: dictionary with user login and password
        :return: dictionary with result
        """
        # Поиск нужного пользователя по EMail адресу    
        try:
            user_data = json.loads(request.body)
            email_user, password_user = user_data["email"], user_data["password"]

        except Exception as er:
            return message[401]
        
        try:
            user = User.objects.get(email=email_user)

        except Exception as er:
            return message[401]
                    
        # расшифровка пароля
        password = Encriptions.decrypt_string(user.password)
        if password != password_user:
            return message[401]
        
        else:
            response = Separement.user_information(user)
            return response
        
    @staticmethod
    def set_key_in_coockies(response, cookie_key):
        response.set_cookie(
                            key='auth_key',
                            value=cookie_key,
                            httponly=True,
                            secure=False,
                            samesite='Lax',
                            max_age=604800  # срок жизни куки. число - 1 неделя в секундах
                            )
        return response

