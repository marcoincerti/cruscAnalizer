"""cruscanalyzer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from cruscanalyzer.views import HomePageView

from cruscanalyzer.views import UserProfileView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('user/<int:pk>/', UserProfileView.as_view(), name='other-user'),
    path('user_management/', include('user_management.urls')),
    path('text_management/', include('text_management.urls')),
    path('admin/', admin.site.urls),
]
