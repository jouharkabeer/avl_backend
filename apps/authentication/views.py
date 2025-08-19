import logging
logger = logging.getLogger(__name__)
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from rest_framework import generics
from django.http import FileResponse, HttpResponse
from .models import *
from .serializer import *
from rest_framework import status
from rest_framework import generics
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.service_provider.master.views import BaseCreateView, BaseDeleteView, BaseListView, BaseUpdateView

class UserCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    def get_queryset(self):
        user = self.request.user

        if user.account is None:
            return User.objects.filter(
                Q(account__parent_account__isnull=True) | Q(account__isnull=True)
            )
        elif user.account and user.account.parent_account:
            return User.objects.filter(account=user.account)
        
        return User.objects.filter(
                    Q(account=user.account) | Q(account__parent_account=user.account)
                )
    
class UserUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class UserTypeCreate(generics.ListCreateAPIView):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer

class UserTypeList(generics.ListAPIView):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    
class UserTypeUpdate(generics.RetrieveUpdateAPIView):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer

class PermisionListCreate(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class PermisionList(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
class PermissionUpdate(generics.RetrieveUpdateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
class RoleCreate(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleList(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
class RoleUpdate(generics.RetrieveUpdateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class MyTokenRefreshView(TokenRefreshView):
    pass

class FranchiseClientUsersByUserIdView(generics.ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, user_id=user_id)

        if user.account:
            franchise_account = user.account
            if franchise_account.account_type.account_type_name == "Franchise Partner":
                return User.objects.filter(
                    Q(account=franchise_account) | 
                    Q(franchise_account.parent_account==franchise_account)
                ).select_related('account', 'user_role', 'user_type')

        elif user.account is None:
            return User.objects.filter(
                Q(account__isnull=True) | 
                Q(account__account_type__account_type_name="Franchise Partner")
            ).select_related('user_role', 'user_type')

        return None
