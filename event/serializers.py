from rest_framework import serializers

from event.models import Event

from user.serializers import UserSimpleSerializer


class EventSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer()
    participant = UserSimpleSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'
