from django.urls import path

from .views import AllTeamsView, TeamDetailView, AddTeamView, UpdateTeamView, AgencyListView, AddAgencyView, \
    UpdateAgencyView

app_name = 'teams'

urlpatterns = [
    path('', AllTeamsView.as_view()),
    path('<int:pk>/', TeamDetailView.as_view()),
    path('add/', AddTeamView.as_view()),
    path('update/', UpdateTeamView.as_view()),

    path('agency/', AgencyListView.as_view()),
    path('agency/add/', AddAgencyView.as_view()),
    path('agency/update/', UpdateAgencyView.as_view())
]
