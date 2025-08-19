"""
URL configuration for axtella_avl_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    # path('api/common/', include('apps.common.urls')),
    # path('api/service_provider/', include('apps.service_provider.urls')),
    # path('api/franchise_partner/', include('apps.franchise_partner.urls')),
    # path('api/customer/', include('apps.customer.urls')),
     path('api/service_provider/master/', include('apps.service_provider.master.urls')),
     path('api/franchise_partner/franchise_partner_master/', include('apps.franchise_partner.franchise_partner_master.urls')),
     path('api/franchise_partner/franchise_partner_transaction/', include('apps.franchise_partner.franchise_partner_transaction.urls')),
]
