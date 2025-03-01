from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.UserRegistrationView.as_view()),
    path("login/", views.UserLoginView.as_view()),
    path("users-list/", views.UserPaginatedListView.as_view()),
    path("role/", views.RoleView.as_view()),
]
