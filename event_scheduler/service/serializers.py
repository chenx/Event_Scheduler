from rest_framework import serializers
from .models import DataStore


class DatastoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataStore
        fields = '__all__'

    def get_owner_name(self, obj):
        return obj.title
