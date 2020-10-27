from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_auth.views import LoginView, LogoutView
from fcm_django.models import FCMDevice
from datetime import datetime
import random

from .serializers import RegistrationSerializer
from users.models import User