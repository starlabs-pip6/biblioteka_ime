from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LibratSerializer ,UsersSerializer
from .models import Book, NewUser
from .forms import RegistrationForm

# Create your views here.
def register_view(request,*args,**kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'You are already authenticated as {user.email}')
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_pw = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_pw)
            login(request, account)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect("home")
        else:
            context['registration_form'] = form

    return render(request,'libri_im/register.html', context)

    
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