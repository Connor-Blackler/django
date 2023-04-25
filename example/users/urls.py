from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("", views.profiles, name="profiles"),
    path("profile/<str:pk>", views.user_profile, name="user-profile"),
    path("my-profile/", views.my_profile, name="my-profile"),
    path("edit-profile/", views.edit_profile, name="edit-profile"),
    path("create-skill/", views.create_skill, name="create-skill"),
    path("edit-skill/<str:pk>", views.update_skill, name="edit-skill"),
    path("delete-skill/<str:pk>", views.delete_skill, name="delete-skill"),
    path("user-inbox/", views.user_inbox, name="user-inbox"),
    path("user-message/<str:pk>", views.user_message, name="user-message"),
    path("user-create-message/<str:pk>",
         views.user_create_message, name="user-create-message"),
]
