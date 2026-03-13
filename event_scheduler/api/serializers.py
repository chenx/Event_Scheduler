from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Event, CustomUser


class EventSerializer(serializers.ModelSerializer):
    # owner = serializers.StringRelatedField()  # use owner name instead of id
    owner_name = serializers.SerializerMethodField()

    class Meta:
        model = Event
        # fields = '__all__'
        fields = ['event_id', 'owner', 'owner_name', 'permission_type', 'title', 'description', \
                  'start_time', 'end_time', 'created_at', 'last_updated']

    def get_owner_name(self, obj):
        return f"{obj.owner.first_name} {obj.owner.last_name}"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
