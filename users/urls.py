from django.urls import path
from .views import UserDetailView, AllUserDetailView, SearchDetailView, AddUserView

app_name = 'users'

urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view()),
    path('all/', AllUserDetailView.as_view()),
    path('search/', SearchDetailView.as_view()),
    path('add/', AddUserView.as_view())
]
