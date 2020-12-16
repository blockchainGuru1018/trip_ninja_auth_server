from django.urls import path
from .views import BasicInfoView, UserDetailView, SearchDetailView, AddUserView, AllUsersListView, BulkAddUserView,\
    EmailCheckView, UserUpdateView, UserAchieveView, AvailableUsersListView, GeneralInfoView, AvailableAdminListView

app_name = 'users'

urlpatterns = [
    path('basic/', BasicInfoView.as_view()),
    path('general/', GeneralInfoView.as_view()),
    path('search/', SearchDetailView.as_view()),
    path('list/', AllUsersListView.as_view()),
    path('list/<int:pk>/', AvailableUsersListView.as_view()),
    path('list/agency/<int:pk>/', AvailableAdminListView.as_view()),
    path('single-add/', AddUserView.as_view()),
    path('bulk-add/', BulkAddUserView.as_view()),
    path('email-check/', EmailCheckView.as_view()),

    path('<int:pk>/', UserDetailView.as_view()),
    path('update/', UserUpdateView.as_view()),
    path('<int:pk>/archive/', UserAchieveView.as_view()),
]
