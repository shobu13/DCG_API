from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'is_staff', 'last_login', 'date_joined',
            'amis',)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserDetailSerializer(serializers.ModelSerializer):
    amis = UserSimpleSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'
        depth = 0


class UserConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
