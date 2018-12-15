from rest_framework import serializers

from event.models import Event

from api.serializers import user


class EventSerializer(serializers.ModelSerializer):
    owner = user.UserSerializer()
    participant = user.UserSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'
