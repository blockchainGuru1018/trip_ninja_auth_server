from django.urls import path

from .views import AllTeamsView, TeamDetailView, AddTeamView, AllAgencyView, AddAgencyView, AllTeamsListView, \
    AgencyListView, TeamUpdateView, AgencyDetailView, AgencyUpdateView

app_name = 'teams'

urlpatterns = [
    path('search/', AllTeamsView.as_view()),
    path('list/', AllTeamsListView.as_view()),
    path('add/', AddTeamView.as_view()),
    path('<int:pk>/', TeamDetailView.as_view()),
    path('update/', TeamUpdateView.as_view()),

    path('agency/search/', AllAgencyView.as_view()),
    path('agency/list/', AgencyListView.as_view()),
    path('agency/add/', AddAgencyView.as_view()),
    path('agency/<int:pk>/', AgencyDetailView.as_view()),
    path('agency/update/', AgencyUpdateView.as_view())
]
