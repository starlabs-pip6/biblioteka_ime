from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LibratSerializer ,UsersSerializer
from .models import Book, NewUser, Progress
from .forms import RegistrationForm, UserAuthenticationForm, MyPasswordChangeForm
from django.views.generic import (CreateView, 
                                    ListView,
                                    DetailView,
                                    DeleteView,
                                    UpdateView)
                                    
from django.urls import reverse, reverse_lazy
from django.db import models
class MyPasswordChangeView(PasswordChangeView):
    form_class = MyPasswordChangeForm
    def get_success_url(self):
        return reverse('profile_page')


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
    current_user = request.user
    books = Book.objects.all()
    
    if(not current_user.is_anonymous):
       
        try :
            progress = Progress.objects.get(id_user=current_user.id)
            progressLibri = progress.id_libri
            progressUser = progress.id_user
            progressNowPages = progress.pages_now
            progressAllPages = progress.id_libri.nr_faqeve
            progressLibriTitulli = progress.id_libri.titulli
            progressPercent =  round(float((progressNowPages/progressAllPages)*100),1)
            progressBookImage = progress.id_libri.image_link
        except models.ObjectDoesNotExist:
            progressLibri = "no data"
            progressUser = "no data"
            progressNowPages = "no data"
            progressAllPages = "no data"
            progressLibriTitulli = "no data"
            progressPercent = "no data"
            progressBookImage = ""
            print("No user")
        dlcount = len(current_user.reading)
        dtlcount = len(current_user.read)
        klcount = len(current_user.want_to_read)
    else:
        progressLibri = "no data"
        progressUser = "no data"
        progressNowPages = "no data"
        progressAllPages = "no data"
        progressLibriTitulli = "no data"
        progressPercent = "no data"
        progressBookImage = ""
        dlcount = "no data"
        dtlcount = "no data"
        klcount = "no data"   # userR = users.reading
    if not current_user:
        current_user='anonimous user(not loged in)'
    context={
        # 'current_username' : current_user,
        'books': books,
        'booksLatest' : books.order_by('-viti_publikimit')[0:6],
        'booksR' : books.order_by('-mes_vleresimit')[0:6],
        'booksID' : books.order_by('?')[0:6],
        'dlcount' : dlcount,
        'klcount' : klcount,
        'dtlcount': dtlcount,
        'progressLibri': progressLibri,
        'progressUser' : progressUser,
        'progressNowPages' : progressNowPages,
        'progressAllPages' : progressAllPages,
        'progressLibriTitulli' : progressLibriTitulli,
        'progressPercent' : progressPercent,
        'progressBookImage':progressBookImage,
    }
    
    return render(request, 'libri_im/home.html',context)

def shfleto_view(request):
    books = Book.objects.all()
    context={
         'books' : books,
    }
    return render(request, 'libri_im/shfleto.html',context)

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

class BookCreateView(CreateView):
    model = Book
    fields =['isbn','titulli','autori','kategoria','pershkrimi','mes_vleresimit','nr_vleresimit','nr_faqeve','viti_publikimit','image_link']
    def get_success_url(self):
        return reverse('admin_home')

        
class BookListView(ListView):
    model = Book 
    template_name='backend/home.html'
    context_object_name = 'books'
    def get_success_url(self):
        return reverse('admin_home')
    ordering = ['id_libri']

class BookDetailView(DetailView):
    model = Book
   
class BookDeleteView(DeleteView):
    model=Book
    success_url = '/'
    template_name='backend/delete.html'

   
    def get_success_url(self):
        return reverse('admin_home')

class BookUpdateView(UpdateView):
    model = Book
    fields = ['isbn','titulli', 'autori', 'kategoria','pershkrimi','mes_vleresimit', 'nr_vleresimit', 'nr_faqeve', 'viti_publikimit','image_link']
    template_name= 'libri_im/backend/addbook.html'
    
    def get_success_url(self):
        return reverse('admin_home')


class ProfilePageView(DetailView):
    model = NewUser 
    template_name='libri_im/profile_page.html'
    context_object_name = 'user'
    
    def get_success_url(self):
        return reverse('profile_page')

    def get_object(self):
        return self.request.user
    
class ProfileUpdateView(UpdateView):
    model = NewUser
    fields = ['username','profileImg','email']
    template_name= 'libri_im/profile_page_update.html'
    
    def get_success_url(self):
        return reverse('profile_page')
    def get_object(self):
        return self.request.user


