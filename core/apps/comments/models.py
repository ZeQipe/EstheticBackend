from templates.answer import answer_dict as message
from django.db import models
from django.utils import timezone
from apps.posts.models import Post
from apps.users.models import User


class Comments(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    text = models.CharField(max_length=600)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    answerCommentId = models.CharField(max_length=50, null=True, default=None)
    answerUserLastName = models.CharField(max_length=100, null=True, default=None)
    answerUserFirstName = models.CharField(max_length=100, null=True, default=None)
    answerUserId = models.CharField(max_length=100, null=True, default=None)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    users_liked = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    created_at = models.DateTimeField(default=timezone.now)


    @staticmethod
    def create(data):
        # Валидация данных
        result_validate, message_validate = Comments.__validate_data(data["text"])
        if not result_validate:
            response = message[400].copy()
            response["message"] = message_validate
            return response

        # Создание поста
        comment = Comments.objects.create(id=data["id"],
                                        text=data["text"],
                                      author=data["author"],
                             answerCommentId=data["answer"].get("id"),
                          answerUserLastName=data["answer"].get("firstName"),
                         answerUserFirstName=data["answer"].get("lastName"),
                                answerUserId=data["answer"].get("userId"),
                                        post=data["post"])


        return {"postId": comment.post.id}
    

    def edit(self, text):
        # Валидация данных
        result_validate, message_validate = Comments.__validate_data(text)
        if not result_validate:
            response = message[400].copy()
            response["message"] = message_validate
            return response
        
        self.text = text
        self.save()
        return self


    @staticmethod
    def __validate_data(text):
        if len(text) < 601 and len(text) > 0: return True, "Данные корректны"
        
        else: return False, "Длина текста не действительна"
