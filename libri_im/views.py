from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LibratSerializer
from .models import librat
# Create your views here.


@api_view(['GET'])
def apiOverView(request):
    apiUrls ={
        'Librat' : '/librat',
        'Liber specifik': '/librat/<id>',
        'Userat' : '/users'
    }
    return Response(apiUrls)


@api_view(['GET'])
def libratList(request):
    libratObj=librat.objects.all()
    serializer = LibratSerializer(libratObj, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def libriSpecifik(request,pk):
    libri = librat.objects.get(id_libri=pk)
    serializer = LibratSerializer(libri, many=False)
    return Response(serializer.data)