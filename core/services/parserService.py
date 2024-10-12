from services.encriptionService import Encriptions
from apps.users.models import User


class Separement:
    @staticmethod
    def packing_tags(tags: list) -> list:
        if not tags:
            return tags

        id_list = []
        while len(id_list) < len(tags):
            id = Encriptions.generate_string(8, False)
            if id not in id_list:
                id_list.append(Encriptions.generate_string(8, False))
            
        tag_response = []
        for i in range(len(id_list)):
            tag_dict = {"tagId" : id_list[i],
                        "label" : tags[i]}
            
            tag_response.append(tag_dict)
        
        return tag_response


    @staticmethod
    def unpacking_tags(tags: list[dict]) -> list[str]:
        print(tags, type(tags))
        if not tags:
            return []
        
        prew_tags = []
        for i in tags:
            prew_tags.append(i["label"])
        
        return prew_tags


    @staticmethod
    def user_information(user: User, cookie_user=False, status=False):
        user_data = {"user": {
                             "userId": user.id,
                             "subscribersAmount": user.subscribers.count(),
                             "avatar": user.avatar,
                             "firstName": user.first_name,
                             "lastName": user.last_name,
                             "userName": user.user_name,
                             }
                    }
        
        if status == "owner":
            user_data['user']['email'] = user.email
            user_data['user']['tags'] = Separement.packing_tags(cookie_user.tags_user)

        elif isinstance(cookie_user, User) and cookie_user.id == user.id:
            user_data['user']['email'] = user.email
            user_data['guest'] = {
                "isOwner": True,
                "isSubscribe": False
            }

        elif status == "guest":
            user_data['guest'] = {
                "isOwner" : False,
                "isSubscribe": False if isinstance(cookie_user, dict) else (True if cookie_user in user.subscribers else False)
            }

        return user_data["user"] if not status else user_data
