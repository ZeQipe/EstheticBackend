from services.encriptionService import Encriptions
from services.mediaService import Media
from django.utils.dateformat import DateFormat
from django.utils.timezone import get_current_timezone
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
    def pagination_parametrs(request) -> tuple:
        try: offset = int(request.GET.get('offset', 0))
        except ValueError: offset = 0

        try: limit = int(request.GET.get('limit', 20))
        except ValueError: limit = 20

        return offset, limit


    @staticmethod
    def user_information(user, cookie_user=False, status=False) -> dict:
        user_data = {"user": {"userId" : user.id,
                   "subscribersAmount" : user.subscribers.count(),
                              "avatar" : Media.get_full_url(user.avatar) if user.avatar else None,
                          "avatarBlur" : Media.get_full_url(user.avatar_blur) if user.avatar_blur else None,
                           "firstName" : user.first_name,
                            "lastName" : user.last_name,
                            "userName" : user.user_name} }

        if status == "owner":
            user_data['user']['email'] = user.email
            user_data['user']['tags'] = Separement.packing_tags(user.tags_user)

        elif cookie_user:
            if not isinstance(cookie_user, dict):
                if cookie_user.id == user.id:
                    user_data['user']['email'] = user.email
                    user_data['guest'] = {"isOwner" : True,
                                      "isSubscribe" : False}

                else:
                    user_data['guest'] = {"isOwner" : False,
                                      "isSubscribe" : True if cookie_user in user.subscribers.all() else False}

        return user_data["user"] if status == "owner" else user_data


    @staticmethod
    def formatted_posts(result, amount) -> list[dict]:
        formatted_posts = {"postsAmount" : amount,
                                 "posts" : []}

        for post in result:
            posted = {"postId" : post.id,
                 "contentType" : post.type_content,
                         "url" : Media.get_full_url(post.url),
                     "urlBlur" : Media.get_full_url(post.url_blur),
                 "aspectRatio" : post.aspect_ratio}
            formatted_posts["posts"].append(posted)

        return formatted_posts
    

    @staticmethod
    def detail_info_post(post, guest):
        data = {"post" : {"postId" : post.id,
                            "name" : post.post_name,
                     "description" : post.description,
                            "link" : post.link,
                           "media" : {"type" : post.type_content,
                                       "url" : Media.get_full_url(post.url),
                                   "urlBlur" : Media.get_full_url(post.url_blur),
                               "aspectRatio" : post.aspect_ratio},
                       "likeCount" : post.users_liked.count(),
                   "commentsCount" : post.comments.count(),
                            "tags" : Separement.packing_tags(post.tags_list),
                          "author" : {"firstName" : post.author.first_name,
                                       "lastName" : post.author.last_name,
                                       "userName" : post.author.user_name,
                                         "userId" : post.author.id,
                                         "avatar" : Media.get_full_url(post.author.avatar) if post.author.avatar else None,
                                     "avatarBlur" : Media.get_full_url(post.author.avatar_blur) if post.author.avatar_blur else None} },
                "user" : {"isLike" : not isinstance(guest, dict) and guest in post.users_liked.all(),
                         "isOwner" : not isinstance(guest, dict) and guest.id == post.author.id} }

        return data


    @staticmethod
    def parse_dashboard_list(user, start, end, type = False):
        response = {"dashboardsAmount" : user.boards.count(),
                           "favorites" : None,
                          "dashboards" : []}

        boards = user.boards.all()
        favorites_board = boards.filter(name="Избранное").first()

        if favorites_board:
            recent_posts = favorites_board.posts.order_by('-boardpost__added_at')[:5]
            response["favorites"] = {"dashboardId" : favorites_board.id,
                                             "urls" : [Media.get_full_url(post.url) for post in recent_posts],
                                             "urlsBlur" : [Media.get_full_url(post.url_blur) for post in recent_posts]}

            if type == "full":
                response["favorites"]["created_at"] = favorites_board.created_at
                response["favorites"]["postsAmount"] = favorites_board.posts.all().count()

            response["dashboardsAmount"] -= 1

        for board in boards.exclude(name="Избранное")[start:start+end]:
            recent_posts = board.posts.order_by('-boardpost__added_at')[:5]

            board_info = {"dashboardId" : board.id,
                        "dashboardName" : board.name,
                                 "urls" : [Media.get_full_url(post.url) for post in recent_posts],
                             "urlsBlur" : [Media.get_full_url(post.url_blur) for post in recent_posts],}

            board_info["dateOfCreation"] = board.created_at
            board_info["postsAmount"] = board.posts.all().count()
            response["dashboards"].append(board_info)

        return response


    @staticmethod
    def pars_dashboards_info_in(boards):
        data = {"inFavorites" : False,
               "inDashboards" : []} 

        for board in boards:
            if board.name == "Избранное":
                data["inFavorites"] = True
                continue
            data["inDashboards"].append(board.id)

        return data


    @staticmethod
    def parse_dashboard(board):
        # Получение и форматирование даты создания доски
        created_at = board.created_at
        formatted_date = DateFormat(created_at.astimezone(get_current_timezone())).format('Y-m-d\TH:i:sP')

        # Получение и форматирование постов
        all_posts = board.posts.order_by('-boardpost__added_at')
        post_count = all_posts.count()
        posts = Separement.formatted_posts(all_posts, post_count)

        # Формирование инфорации о доске
        data = {"dashboardInfo": {"dashboardId": board.id,
                                "dashboardName": board.name,
                                  "postsAmount": post_count,
                               "dateOfCreation": formatted_date},
                       "author":{"firstName" : board.author.first_name,
                                  "lastName" : board.author.last_name,
                                  "userName" : board.author.user_name,
                                    "userId" : board.author.id,
                                    "avatar" : Media.get_full_url(board.author.avatar) if board.avatar else None,
                                "avatarBlur" : Media.get_full_url(board.avatar_blur) if board.avatar_blur else None},
                        "posts": posts['posts']}

        return data
