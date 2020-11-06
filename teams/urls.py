from django.urls import path

from .views import AllTeamsView, TeamDetailView, TeamEditView, AgencyListView, AgencyView

app_name = 'teams'

urlpatterns = [
    path('all/', AllTeamsView.as_view()),
    path('<int:pk>/', TeamDetailView.as_view()),
    path('edit/<int:pk>/', TeamEditView.as_view()),
    path('agency/all/', AgencyListView.as_view()),
    path('agency/<int:pk>/', AgencyView.as_view())
]
