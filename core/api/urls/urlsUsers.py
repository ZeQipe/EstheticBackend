from django.urls import path
from ..inreface import viewsUsers
from ..inreface import viewsDashboards


urlpatterns = [
    path("users/registration", viewsUsers.usersRegistration, name="user_registration"),
    path("users/login", viewsUsers.usersLogin, name="user_login"),
    path("users/logout", viewsUsers.usersLogout, name="user_logout"),
    
]