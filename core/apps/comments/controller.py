from templates.answer import answer_dict as message
from services.authService import Authorization
from apps.comments.models import Comments
from apps.posts.models import Post
from services.encriptionService import Encriptions
from services.parserService import Separement
import json


def create_comments(request, postId):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]

    try: post = Post.objects.get(id=postId)
    except Exception: return message[404]

    # Формируем информацию о посте
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return message[400]
    
    answerId = data.get("answerCommentId", default="None")
    
    if answerId != "None":
        try: answerComment = Comments.objects.get(answerId)
        except Exception: 
            response = message[404]
            response["error"] = "Комментарий, на который Вы пытались ответить, не найден."
            return response
        
    else: answerComment = "None"

    comments_data = {"id" : Encriptions.generate_string(50, Comments),
                   "text" : data[0].get("text"),
                 "author" : cookie_user,
                 "answer" : answerComment,
                   "post" : post}
    
    try: 
        result = Comments.create(comments_data)
        return {"postId" : result.post.id}
    except Exception: return message[500]


def get_comments(request, postId):
    # Получаем query параметры offset и limit из запроса
    offset, limit = Separement.pagination_parametrs(request)

    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)

    try: post = Post.objects.get(id=postId)
    except Exception: return message[404]

    comments = Comments.objects.filter(post=post).order_by('-created_at')

    if comments.count() == 0:
        return {"commentsAmount" : 0,
                 "commentsList" : []}
    else:
        response = Separement.formatted_comments(comments, cookie_user, offset, limit, modelComments=Comments)
        return response


def edit_comments(request, commentId):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]

    # Проверка на существования комментария
    try: comment = Comments.objects.get(id=commentId)
    except Exception: return message[404]

    # Проверка что комментарий принадлежит пользователю
    if comment.author.id != cookie_user.id:
        return message[403]
    
    # Формируем информацию о посте
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return message[400]
    
    comment_text = data.get("text")

    try: 
        result = comment.edit(comment_text)
        return  {"postId" : result.post.id}
    
    except Exception: return message[500]




def change_like(request, commentsId):
    # Проверка на авторизацию пользователя
    cookie_user = Authorization.is_authorization(request)
    if isinstance(cookie_user, dict): return message[401]

    # Поиск поста в базе данных
    try: comment = Comments.objects.get(id=commentsId)
    except Exception: return message[404]

    # Установка или удаление лайка
    if comment.users_liked.filter(id=cookie_user.id).exists():
        comment.users_liked.remove(cookie_user)
    else:
        comment.users_liked.add(cookie_user)

    return message[200]