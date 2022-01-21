from django.contrib import admin
from django.urls import path
from .register import Register, Login, User, LogOut
from .views import UserListView, UserDetailView

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('userlogin/', User.as_view()),
    path('logout/', LogOut.as_view()),
    path('users/', UserListView.as_view()),
    path('user/<int:pk>', UserDetailView.as_view())

]
