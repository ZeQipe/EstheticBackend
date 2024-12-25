from django.db import models
from django.utils import timezone
from django.db.models import Q
from services.encriptionService import Encriptions
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class Board(models.Model):
    id = models.CharField(max_length=45, primary_key=True)
    name = models.CharField(max_length=35)
    posts = models.ManyToManyField("posts.Post", related_name='boards', blank=True)
    author = models.ForeignKey('users.User', related_name='boards', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    recent_photo_urls = ArrayField(models.URLField(), size=5, blank=True, default=list)


    @staticmethod
    def create_board(user, name: str) -> dict:
        """
        Функция создает доску в базе данных

        :user: Объект класса User, который будет автором доски
        :name: Строка, не более 35 символов
        :return: dict
        """
        # Генерируем новый ID
        id_board = Encriptions.generate_string(35, Board)

        # Создаём доску
        board = Board.objects.create(
                            id=id_board,
                            name=name,
                            author=user
                            )

        # Возвращаем ID доски
        return {"dashboardId": board.id}


    @staticmethod
    def check_board_name(user, name) -> bool:
        """
        Функция проверяет, существует ли доска с указанным именем среди досок пользователя.

        :param user: объект пользователя, которому принадлежат доски
        :param name: имя доски, которое нужно проверить
        :return: bool
        """
        # Если список id пустой, возвращаем False
        if not user.boards.all():
            return False

        # Ищем доски пользователя по списку id и имени доски
        if Board.objects.filter(
            Q(author=user) & Q(name=name)
        ).exists():
            return True

        # Если совпадений нет
        return False


class BoardPost(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-added_at']
