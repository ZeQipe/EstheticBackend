from .authService import Authorization
from templates.answer import answer_dict as message
from apps.comments.models import Comment
from apps.dashboards.models import Board
from apps.posts.models import Post
from apps.users.models import User


class DeletterObject:
    @staticmethod
    def del_object(request, model, targetID=None):
        cookie_user = Authorization.is_authorization(request)
        
        if isinstance(cookie_user, dict):
            return message[401]
        
        elif model == User:
            cookie_user.delete()
        
        else:
            try:
                target = model.objects.get(id=targetID)
                
            except Exception as er:
                return message[400]
        
            if cookie_user.id != target.author.id:
                return message[403]
            
            if model == Board:
                if target.name == "Избранное":
                    return message[403]

            target.delete()
            
        return message[200]