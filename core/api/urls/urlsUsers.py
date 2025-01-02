from django.urls import path
from ..interface import viewsUsers
from ..interface import viewsDashboards


urlpatterns = [
    # users
    path("users", viewsUsers.users, name="users"), # Удаление и редактирование пользователя
    path("users/registration", viewsUsers.usersRegistration, name="user_registration"), # Регистрация пользователя
    path("users/login", viewsUsers.usersLogin, name="user_login"), # Авторизация
    path("users/logout", viewsUsers.usersLogout, name="user_logout"), # Выход из аккаунта
    path("users/private-profile", viewsUsers.privateProfile, name="privateProfile"), # Получение профиля по Cookie
    path("users/public-profile/<str:userID>", viewsUsers.publicProfile, name="publicProfile"), # Получение профиля по ID
    path("users/<str:userID>/created-posts", viewsUsers.usersCreatedPosts, name="userCreatedPosts"), # Список постов пользователя

    # dashboards
    path("dashboards", viewsDashboards.dashboards, name='dashboards'), # Создание и получение досок
    path("dashboards/check-posts", viewsDashboards.post_in_boards, name="post_in_boards"), # Наличие поста в доске
    path("dashboards/<str:boardID>/delete-posts", viewsDashboards.dashboards_delete_posts, name="dashboardsDeletePosts"), # Удаление поста из доски
    path("dashboards/<str:userID>/list", viewsDashboards.dashboards_list, name="dashboards_param"), # информация о досках пользователя
    path("dashboards/<str:boardID>", viewsDashboards.dashboards_param, name="dashboards_param"), # Удаление доски, добавления поста в доску, детализированной информация о доске

    # auth 
    path("auth/check", viewsUsers.check_auth, name="check_auth") # Проверка авторизации
]
