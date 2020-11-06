from django.urls import path

from .views import AllTeamsView, TeamDetailView, AddTeamView, UpdateTeamView, AgencyListView, AgencyView

app_name = 'teams'

urlpatterns = [
    path('', AllTeamsView.as_view()),
    path('<int:pk>/', TeamDetailView.as_view()),
    path('add/', AddTeamView.as_view()),
    path('update/', UpdateTeamView.as_view()),

    path('agency/all/', AgencyListView.as_view()),
    path('agency/<int:pk>/', AgencyView.as_view())
]
