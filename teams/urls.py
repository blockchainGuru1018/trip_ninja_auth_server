from django.urls import path

from .views import NameCheckView, AllTeamsView, TeamDetailView, AddTeamView, AllAgencyView, AddAgencyView, AllTeamsListView, \
    AgencyListView, TeamUpdateView, AgencyDetailView, AgencyUpdateView, DataSourceView, TeamAchieveView, \
    AvailableDataSourceView, AgencyAchieveView, AgencyTeamsListView

app_name = 'teams'

urlpatterns = [
    path('name-check/', NameCheckView.as_view()),
    path('search/', AllTeamsView.as_view()),
    path('list/', AllTeamsListView.as_view()),
    path('list/<int:pk>/', AgencyTeamsListView.as_view()),
    path('add/', AddTeamView.as_view()),
    path('<int:pk>/', TeamDetailView.as_view()),
    path('update/', TeamUpdateView.as_view()),
    path('<int:pk>/archive/', TeamAchieveView.as_view()),

    path('agency/search/', AllAgencyView.as_view()),
    path('agency/list/', AgencyListView.as_view()),
    path('agency/add/', AddAgencyView.as_view()),
    path('agency/<int:pk>/', AgencyDetailView.as_view()),
    path('agency/update/', AgencyUpdateView.as_view()),
    path('agency/<int:pk>/archive/', AgencyAchieveView.as_view()),

    path('data_source/', DataSourceView.as_view()),
    path('data_source/<int:pk>/', AvailableDataSourceView.as_view())
]
