from django.urls import path

from .views import AllTeamsView, TeamDetailView

app_name = 'teams'

urlpatterns = [
    path('', AllTeamsView.as_view()),
    path('<int:pk>/', TeamDetailView.as_view()),
]
