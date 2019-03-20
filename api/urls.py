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
from django.urls import path, URLPattern

from rest_framework.routers import DefaultRouter
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api import viewsets

schema_view = get_schema_view(
    openapi.Info(
        title="DCG API",
        default_version='v3.14',
        description="read the docs",
        contact=openapi.Contact(email="lelu.awen@hacari.org"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

router = DefaultRouter()
router.register('user', viewsets.UserViewset)
router.register('interests', viewsets.InterestViewset)
router.register('places', viewsets.PlaceViewset)
router.register('promos', viewsets.PromoViewset)
router.register('events', viewsets.EventViewset)

urlpatterns = [
    path('docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
urlpatterns += router.urls
# i: URLPattern
# for i in router.urls:
#     print(i.name, i.pattern)
