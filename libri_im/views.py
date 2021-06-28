from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LibratSerializer ,UsersSerializer
from .models import Book, NewUser
from .forms import RegistrationForm, UserAuthenticationForm
from django.views.generic import (CreateView, 
                                    ListView,
                                    DetailView,
                                    DeleteView)
from django.urls import reverse


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


def home_view(request):
    current_user = request.user.username
    if not current_user:
        current_user='anonimous user(not loged in)'
    context={
        'current_username' : current_user
    }
    
    
    return render(request, 'libri_im/home.html',context)

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
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect("home")
        else:
            context['registration_form'] = form

    return render(request,'libri_im/register.html', context)

    
def logout_view(request):
    logout(request)
    return redirect("home")

def login_view(request,*args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated: 
        return redirect("home")

    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("home")
    else:
        form = UserAuthenticationForm()
    context['login_form'] = form
    return render(request, "libri_im/login.html", context)

def get_redirect_if_exists(request):
    redirect=None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect

class PostCreateView(CreateView):
    model = Book
    fields =['isbn','titulli','autori','kategoria','pershkrimi','mes_vleresimit','nr_vleresimit','nr_faqeve','viti_publikimit']
    def get_success_url(self):
        return reverse('admin_home')

        
class PostListView(ListView):
    model = Book 
    template_name='backend/home.html'
    context_object_name = 'books'
    def get_success_url(self):
        return reverse('admin_home')

class PostDetailView(DetailView):
    model = Book
   
class PostDeleteView(DeleteView):
    model=Book
    success_url = '/'
    template_name='backend/delete.html'

   
    def get_success_url(self):
        return reverse('admin_home')