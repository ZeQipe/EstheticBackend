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
    path("dashboards", viewsDashboards.dashboards, name='dashboards'),
    path("dashboards/check-posts", viewsDashboards.post_in_boards, name="post_in_boards"),
    path("dashboards/<str:boardID>/delete-posts", viewsDashboards.dashboards_delete_posts, name="dashboardsDeletePosts"),
    path("dashboards/<str:userID>/list", viewsDashboards.dashboards_list, name="dashboards_param"),

    # auth
    path("auth/check", viewsUsers.check_auth, name="check_auth")
]