"""DCG_API URL Configuration

The `urlpatterns` list routes URLs to viewsets. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function viewsets
    1. Add an import:  from my_app import viewsets
    2. Add a URL to urlpatterns:  path('', viewsets.home, name='home')
Class-based viewsets
    1. Add an import:  from other_app.viewsets import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from api.viewsets import user

router = DefaultRouter()
router.register('user', user.UserViewset)

urlpatterns = [
    path('docs/', get_swagger_view(title='read the docs bastard'))
]
urlpatterns += router.urls
