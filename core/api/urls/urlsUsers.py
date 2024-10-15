from django.urls import path
from ..interface import viewsUsers
from ..interface import viewsDashboards


urlpatterns = [
    # users
    path("users", viewsUsers.users, name="users"),
    path("users/registration", viewsUsers.usersRegistration, name="user_registration"),
    path("users/login", viewsUsers.usersLogin, name="user_login"),
    path("users/logout", viewsUsers.usersLogout, name="user_logout"),
    path("users/private-profile", viewsUsers.privateProfile, name="privateProfile"),
    path("users/public-profile/<str:userID>", viewsUsers.publicProfile, name="publicProfile"),
    path("users/<str:userID>/created-posts", viewsUsers.usersCreatedPosts, name="userCreatedPosts"),

    # dashboards
    

    # auth
    path("auth/check", viewsUsers.check_auth, name="check_auth")
]