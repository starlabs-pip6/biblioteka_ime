from rest_framework import serializers
from .models import Book, NewUser



class LibratSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields='__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields='__all__'

        