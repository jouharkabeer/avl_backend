from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # User URLs
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/create/', views.UserCreate.as_view(), name='user-create'),
    path('users/<uuid:pk>/update/', views.UserUpdate.as_view(), name='user-update'),

    # UserType URLs
    path('usertypes/', views.UserTypeList.as_view(), name='usertype-list'),
    path('usertypes/create/', views.UserTypeCreate.as_view(), name='usertype-create'),
    path('usertypes/<uuid:pk>/update/', views.UserTypeUpdate.as_view(), name='usertype-update'),

    # Permission URLs
    path('permissions/', views.PermisionList.as_view(), name='permission-list'),
    path('permissions/create/', views.PermisionListCreate.as_view(), name='permission-create'),
    path('permissions/<uuid:pk>/update/', views.PermissionUpdate.as_view(), name='permission-update'),

    # Role URLs
    path('roles/', views.RoleList.as_view(), name='role-list'),
    path('roles/create/', views.RoleCreate.as_view(), name='role-create'),
    path('roles/<uuid:pk>/update/', views.RoleUpdate.as_view(), name='role-update'),
    
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),

    path('users/<uuid:user_id>/franchise-client-users/', FranchiseClientUsersByUserIdView.as_view(), name='franchise_client_users_by_user'),
]