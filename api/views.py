from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_auth.views import LoginView, LogoutView

from .serializers import RegistrationSerializer


class UserLoginView(LoginView):
    def get_response(self):
        original_response = super().get_response()

        response = {
            "result": True,
            "data": {
                "token": original_response.data.get('key'),
                "user": {
                    "id": self.user.id,
                    "email": self.user.email,
                    "first_name": self.user.first_name,
                    "last_name": self.user.last_name
                }
            }
        }

        return Response(response, status=status.HTTP_201_CREATED)


class UserRegistrationView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response({"result": True}, status=status.HTTP_201_CREATED, headers=headers)


class UserLogoutView(LogoutView):
    def logout(self, request):
        super().logout(request)
        return Response({"result": True}, status=status.HTTP_201_CREATED)
