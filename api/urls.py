from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserSettingsView, UserRegistrationView, ForgotPasswordView, ConfirmTokenView, ResetPasswordView, \
    ChangePasswordView, UserLogoutView, UserDetailsView, SearchFlightsView, PriceFlightsView, BookView, \
    PriceMapView, QueueView, TicketView, CancelView, BookingDetailsView, BookingsListView

app_name = 'api'
urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('settings/', UserSettingsView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('confirm-token/', ConfirmTokenView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('user-details/', UserDetailsView.as_view()),
    path('search/', SearchFlightsView.as_view()),
    path('price/', PriceFlightsView.as_view()),
    path('price-map/', PriceMapView.as_view()),
    path('book/', BookView.as_view()),
    path('queue/', QueueView.as_view()),
    path('ticket/', TicketView.as_view()),
    path('cancel/', CancelView.as_view()),
    path('book/list/', BookingsListView.as_view()),
    re_path('book/trip/\w+/', BookingDetailsView.as_view()),
    re_path(r'^users/', include('users.urls')),
    re_path(r'^teams/', include('teams.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

