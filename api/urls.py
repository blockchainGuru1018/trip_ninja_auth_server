from django.urls import path, re_path, include
from .views import UserRegistrationView, UserLoginView, UserLogoutView

app_name = 'api'

urlpatterns = [
    path('login/', UserLoginView.as_view()),
    path('register/', UserRegistrationView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    re_path(r'^users/', include('users.urls')),
    re_path(r'^teams/', include('teams.urls')),
]
