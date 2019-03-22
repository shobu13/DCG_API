from django.contrib.auth import authenticate

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings

from user.models import User
from interests.models import Interest
from places.models import Place
from promo.models import Promo
from event.models import Event

from user.serializers import UserSerializer, UserCreateSerializer, UserDetailSerializer, UserConnectSerializer, \
    UserSimpleSerializer, UserChangePasswordSerializer
from interests.serializers import InterestSerializer
from places.serializers import PlaceSerializer
from promo.serializers import PromoSerializer
from event.serializers import EventSerializer

from event.permissions import IsEventOwner


# Create your viewsets here.

class MultiSerializerViewSet(viewsets.GenericViewSet):
    """
    MultiSerializerViewSet est une class custom permettant l'usage de plusieurs serializer
    en fonction de l'action.
    Elle permet aussi de sélectionner les permissions à accorder en fonction de l'action.
    """
    serializers = {
        'default': None,
    }

    permission_classes = {
        'default': api_settings.DEFAULT_PERMISSION_CLASSES
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action,
                                    self.serializers['default'])

    def get_permissions(self):
        permission_list = self.permission_classes.get(self.action,
                                                      self.permission_classes['default'])
        return [permission() for permission in permission_list]


class UserViewset(MultiSerializerViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin):
    """
    Ce viewset permet de manipuler les donnée des Users.

    list:
    cette fonction permet de donner une liste non exaustive de tout les utilisateurs.
    create:
    cette fonction permet de créer un utilisateur, le mot de passe est récupérer et haché à l'aide
    de la fonction make_password().
    detail_full:
    Peut être utiliser seulement si administrateur, affiche tout les détails sur un utilisateur.
    list_full:
    Peut être utiliser seulement si administrateur, affiche tout les détails sur tout les utilisateurs.
    destroy:
    Cette fonction sert à supprimer un user.
    retrieve:
    Cette fonction renvoie les donnée non sensibles d'un user
    """

    queryset = User.objects.all()

    permission_classes = {
        'default': (permissions.IsAuthenticated,)
        # 'list_full': (permissions.IsAdminUser,),
    }

    serializers = {
        'default': UserSerializer,
        'list': UserSimpleSerializer,
        'create': UserCreateSerializer,
        'detail_full': UserDetailSerializer,
        'change_password': UserChangePasswordSerializer
        # 'list_full': UserDetailSerializer,
        # 'user_connect': UserConnectSerializer,
    }

    def perform_create(self, serializer):
        serializer_data = serializer.data
        user = User.objects.create_user(
            username=serializer_data["username"],
            email=serializer_data["email"],
            password=serializer_data["password"]
        )
        user.first_name = serializer_data["first_name"]
        user.last_name = serializer_data["last_name"]
        user.street = serializer_data["street"]
        user.postal_code = serializer_data["postal_code"]
        user.city = serializer_data["city"]
        user.phone_number = serializer_data["phone_number"]
        user.birth_date = serializer_data["birth_date"]
        user.save()

    @action(
        detail=True,
        methods=['get'],
        url_path='retrieve-full',
    )
    def retrieve_full(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['get'],
        url_path='list-full',
    )
    def list_full(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        url_path='change-password'
    )
    def change_password(self, request, *args, **kwargs):
        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid()
        if authenticate(request, username=request.user.username, password=serializer.validated_data["old_password"]):
            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "password not match"})


# @action(
#     detail=False,
#     methods=['post'],
#     url_path='user-connect',
# )
# def user_connect(self, request):
#     data = request.data
#     username = data.get('username')
#     password = data.get('password')
#     user = authenticate(username=username, password=password)
#     if user:
#         return Response(UserSerializer(user).data)
#     return Response(None)


class InterestViewset(MultiSerializerViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin):
    """
    Ce viewset permet de manipuler les données du modèle interest.

    list:
    permet de récupérer la liste des interets.
    retrieve:
    permet la récupération d'un interet préçis par son ID
    create:
    permet de créer un interet.
    destroy:
    permet de supprimer un interet.
    """

    queryset = Interest.objects.all()

    permission_classes = {
        'default': (permissions.AllowAny,),
    }

    serializers = {
        'default': InterestSerializer,
    }


class PlaceViewset(MultiSerializerViewSet, mixins.ListModelMixin, ):
    """
    Ce viewset permet de manipuler les données du modèle Place
    list:
    renvoie la liste des toutes les places.
    create:
    permet de créer une place, néscessite une connexion administrateur
    retrieve:
    permet de récupérer une place précise en fonction de son ID.
    """
    queryset = Place.objects.all()
    permission_classes = {
        'default': (permissions.AllowAny,),
        'create': (permissions.IsAdminUser,)
    }
    serializers = {
        'default': PlaceSerializer
    }


class PromoViewset(MultiSerializerViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    Viewset permettant de manipuler les donéne du modèle Promo. Les promo so créer depuis l'inteface d'admin.
    list:
    renvoie la liste de toutes les promotions enregistrées.
    retrieve:
    renvoie une promotion particulière en fonction de son ID.
    """
    queryset = Promo.objects.all()
    permission_classes = {
        'default': (permissions.IsAdminUser,),
        'list': (permissions.AllowAny,),
        'retrieve': (permissions.AllowAny,)
        # TODO permission pour les promoteurs
    }
    serializers = {
        'default': PromoSerializer
    }


class EventViewset(MultiSerializerViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    """
    Viewset permettant de gérer les évènements. Un évènement ne peut être modifier ou supprimer que par son créateur ou
    un admin.
    list:
    renvoie la liste de tout les évnènements enregistrer dans la BDD.
    create:
    permet la création d'un évènement
    destroy:
    permet la suppression d'un évènement
    update:
    permet la mise à jour totale d'un évènement.
    partial-update:
    permet la mise à jour partielle d'un évènement.
    retrieve:
    permet de récupérer un évènement en aprticulier via son ID.
    """
    queryset = Event.objects.all()
    permission_classes = {
        'default': (permissions.IsAuthenticatedOrReadOnly, IsEventOwner,),
        'list': (permissions.AllowAny,),
        'retrieve': (permissions.AllowAny,),
        'create': (permissions.IsAuthenticated,)
    }
    serializers = {
        'default': EventSerializer
    }
