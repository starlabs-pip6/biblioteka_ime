from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LibratSerializer ,UsersSerializer
from .models import Book, NewUser

# Create your views here.

@api_view(['GET'])
def backendOverView(request):
    backendUrls ={
        'Books' : '/books',
        'Specific Books': '/books/<id>',
    }
    return Response(backendUrls)


@api_view(['GET'])
def booksList(request):
    booksObj = Book.objects.all()
    serializer = LibratSerializer(booksObj, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def specificBook(request,pk):
    bookObj = Book.objects.get(id_libri=pk)
    serializer = LibratSerializer(bookObj, many=False)
    return Response(serializer.data)