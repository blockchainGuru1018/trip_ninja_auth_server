from django.urls import path
from .views import UserDetailView, AllUserDetailView

app_name = 'users'

urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view()),
    path('all/', AllUserDetailView.as_view()),
]
