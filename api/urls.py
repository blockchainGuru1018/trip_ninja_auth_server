from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import UserLoginView, UserRegistrationView, ForgotPasswordView, ConfirmTokenView, ResetPasswordView, \
    ChangePasswordView, UserLogoutView

app_name = 'api'
urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('confirm-token/', ConfirmTokenView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^users/', include('users.urls')),
    re_path(r'^teams/', include('teams.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

