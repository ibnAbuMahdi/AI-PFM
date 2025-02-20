"""
URL configuration for AI_PFM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.views import ObtainAuthToken
from daas.views import *
from tenants.views import CustomObtainAuthToken, UserRegistrationViewSet, LogoutView, UserDashboardViewSet, TransactionViewSet, BudgetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'budgets', BudgetViewSet, basename='budgets')
router.register(r'register', UserRegistrationViewSet)
router.register(r'dashboard', UserDashboardViewSet, basename='user_dashboard')
router.register(r'user', UserViewSet, basename='daas_users')
router.register(r'prospects', ProspectViewSet, basename='daas_prospects')
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('daas/login/', DAASObtainAuthToken.as_view()),
    path('login/', CustomObtainAuthToken.as_view()),  # Login endpoint
    path('logout/', LogoutView.as_view()),  # Logout endpoint
    path('', include('rest_framework.urls')),
    path('', include(router.urls)),
]
