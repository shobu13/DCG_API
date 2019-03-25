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
        fields = (
            'username', 'password', 'first_name', 'last_name', 'email', 'postal_code', 'city', 'phone_number',
            'birth_date')


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserDetailSerializer(serializers.ModelSerializer):
    amis = UserSimpleSerializer(many=True)

    class Meta:
        model = User
        exclude = ('password',)
        depth = 0


class UserConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
