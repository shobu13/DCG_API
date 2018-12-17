from rest_framework import serializers

from event.models import Event

from api.serializers import user


class EventSerializer(serializers.ModelSerializer):
    owner = user.UserSimpleSerializer()
    participant = user.UserSimpleSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'
