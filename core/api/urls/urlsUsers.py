from django.urls import path
from ..inreface import viewsUsers
from ..inreface import viewsDashboards


urlpatterns = [
    path("users", viewsUsers.users, name="users"),
    path("users/registration", viewsUsers.usersRegistration, name="user_registration"),
    path("users/login", viewsUsers.usersLogin, name="user_login"),
    path("users/logout", viewsUsers.usersLogout, name="user_logout"),
    path("users/private-profile", viewsUsers.privateProfile, name="privateProfile"),
    path("users/public-profile/<str:userID>", viewsUsers.publicProfile, name="publicProfile"),
    path("users/<str:userID>/created-posts", viewsUsers.usersCreatedPosts, name="userCreatedPosts"),
]