
from django.db import models
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)  # Fix the typo in the field name

    class Meta:
        model = Role
        fields = '__all__'
class UserListSerializer(serializers.ModelSerializer):
    user_role = RoleSerializer(read_only=True) 
    individual_permissions = PermissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = '__all__'
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])  
        return super().create(validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
 
        token['user_id'] = str(user.user_id)
        token['username'] = user.username
        token['fisrt_name'] = user.first_name
        token['last_name'] = user.last_name
        token['account_id'] = str(user.account.account_id) if user.account else None
        token['account_name'] = user.account.name if user.account else None
        token['email'] = user.email
        token['phone'] = user.phone
        token['is_active'] = user.is_active
        token['user_role'] = user.user_role.role_name if user.user_role else None
        token['user_type'] = user.user_type.user_type_name if user.user_type else None
        token['profile_image'] = user.profile_image.url if user.profile_image else None
        token['last_login'] = user.last_login.isoformat() if user.last_login else None
        token['date_of_birth'] = user.date_of_birth.isoformat() if user.date_of_birth else None

        return token   
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'user_id': str(self.user.user_id),
            'fisrt_name': str(self.user.first_name),
            'last_name': str(self.user.last_name),
            'username': self.user.username,
            'account_name': self.user.account.name if self.user.account else None,
            'account_id' : str(self.user.account.account_id) if self.user.account else None,
            'email': self.user.email,
            'phone': self.user.phone,
            'is_active': self.user.is_active,
            'user_role': self.user.user_role.role_name if self.user.user_role else None,
            'user_type': self.user.user_type.user_type_name if self.user.user_type else None,
            'profile_image': self.user.profile_image.url if self.user.profile_image else None,
            'last_login': self.user.last_login.isoformat() if self.user.last_login else None,
            'date_of_birth': self.user.date_of_birth.isoformat() if self.user.date_of_birth else None,
        }

        return data   

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'