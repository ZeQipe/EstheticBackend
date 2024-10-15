from services.encriptionService import Encriptions
from services.mediaService import Media
import json


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
    def unpacking_tags(tags_str: str) -> list[str]:
        if not tags_str:
            return []
        
        tags = json.loads(tags_str)

        prew_tags = []
        for i in tags:
            prew_tags.append(i["label"])
        
        return prew_tags


    @staticmethod
    def user_information(user, cookie_user=False, status=False):
        user_data = {"user": {
                             "userId": user.id,
                             "subscribersAmount": user.subscribers.count(),
                             "avatar": Media.get_full_url(user.avatar),
                             "firstName": user.first_name,
                             "lastName": user.last_name,
                             "userName": user.user_name,
                             }
                    }
        
        if status == "owner":
            user_data['user']['email'] = user.email
            user_data['user']['tags'] = Separement.packing_tags(cookie_user.tags_user)

        elif cookie_user:
            if not isinstance(cookie_user, dict) and cookie_user.id == user.id:
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
    

    @staticmethod
    def formatted_posts(result, start, end, amount) -> list[dict]:
        """
        Парсит результат и формирует список постов в нужном формате.
        :param result: результат запроса
        :param columns: список колонок
        :return: список отформатированных постов
        """
        formatted_posts = {"postsAmount": amount,
                        "posts": []}
        
        for post in result[start:start+end:]:
            posted = {
                "postId": post.id,
                "contentType": post.type_content,
                "url": Media.get_full_url(post.url),
                "aspectRatio": post.aspect_ratio,
            }

            formatted_posts["posts"].append(posted)

        return formatted_posts