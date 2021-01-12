from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserSettingsView, UserRegistrationView, ForgotPasswordView, ConfirmTokenView, ResetPasswordView, \
    ChangePasswordView, UserLogoutView, UserDetailsView

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
    path('get_user_details/', UserDetailsView.as_view()), # TODO rename and refactor
    #path('search/'),
    #path('price/'),
    #path('price-map/'),
    #path('book/'),
    #path('queue/'),
    #path('ticket/'),
    #path('cancel/'),
    #path('book/list/'),
    #path('book/trip/\w*/'),
    re_path(r'^users/', include('users.urls')),
    re_path(r'^teams/', include('teams.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

