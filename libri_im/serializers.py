from rest_framework import serializers
from .models import librat

class LibratSerializer(serializers.ModelSerializer):
    class Meta:
        model = librat
        fields='__all__'
        