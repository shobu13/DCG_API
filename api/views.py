from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework import mixins
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action
from rest_framework.response import Response

from user.models import User
from api.serializers import UserSerializer, UserCreateSerializer, UserDetailSerializer


# Create your views here.

class MultiSerializerViewSet(viewsets.GenericViewSet):
    """
    MultiSerializerViewSet est une class custom permettant l'usage de plusieurs serializer
    en fonction de l'action.
    """
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action,
                                    self.serializers['default'])


class UserViewset(MultiSerializerViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, ):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()

    serializers = {
        'default': UserSerializer,
        'create': UserCreateSerializer,
        'user_detail': UserDetailSerializer,
        'user_detail_all': UserDetailSerializer,
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer["password"] = make_password(serializer["password"])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(
        detail=True,
        methods=['get'],
        permission_classes=(permissions.IsAdminUser, ),
        url_path='detail',
    )
    def user_detail(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(permissions.IsAdminUser, ),
        url_path='detail_all',
    )
    def user_detail_all(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
