from rest_framework import serializers
from .models import Book, NewUser, Sirtar, Progress



class LibratSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields='__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields='__all__'

class SirtarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sirtar
        fields='__all__'

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'

        