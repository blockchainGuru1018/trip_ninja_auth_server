from django.urls import path
from .views import UserDetailView, SearchDetailView, AddUserView, AllUsersListView, BulkAddUserView,\
    EmailCheckView, UserUpdateView, UserAchieveView, AvailableUsersListView

app_name = 'users'

urlpatterns = [
    path('search/', SearchDetailView.as_view()),
    path('list/', AllUsersListView.as_view()),
    path('list/<int:pk>/', AvailableUsersListView.as_view()),
    path('single-add/', AddUserView.as_view()),
    path('bulk-add/', BulkAddUserView.as_view()),
    path('email-check/', EmailCheckView.as_view()),

    path('<int:pk>/', UserDetailView.as_view()),
    path('update/', UserUpdateView.as_view()),
    path('<int:pk>/archive/', UserAchieveView.as_view()),
]
