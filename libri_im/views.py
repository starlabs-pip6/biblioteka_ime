from libri_im.friend_request_status import FriendRequestStatus
from django.utils.datastructures import MultiValueDictKeyError
from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from .serializers import LibratSerializer, UsersSerializer, SirtarSerializer, ProgressSerializer
from .models import Book, Event, FriendList, FriendRequest, NewUser, Progress, Sirtar,Comment, Relation, Notification
from .forms import NewCommentForm, RegistrationForm, UserAuthenticationForm, MyPasswordChangeForm
from django.views.generic import (CreateView,
                                  ListView,
                                  DeleteView,
                                  UpdateView,
                                  DetailView)
from .utils import account_activation_token,get_friend_request_or_false
from . import utils
#from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import auth
from django.views import View
from django.urls import reverse, reverse_lazy
from django.db import models
from django.db.models import Q, F
from .friend_request_status import FriendRequestStatus
from datetime import date
from django.core.paginator import PageNotAnInteger, Paginator
import json

def friendRequestPost(request):
    if request.method =="POST" and request.is_ajax:
        user = request.user
        user_id = request.POST.get('userid')
        if user_id:
            receiver = NewUser.objects.get(pk=user_id)
            if not Relation.objects.filter(user1=user, user2=receiver).exists() and not Relation.objects.filter(user1=receiver, user2=user).exists():
                Relation(user1=user,user2=receiver,status=1).save()
                return HttpResponse("No relation but created")
            else:
                if Relation.objects.filter(user1=user, user2=receiver).exists() or Relation.objects.filter(user1=receiver, user2=user, status=2).exists():
                    Relation.objects.filter(user1=user, user2=receiver).delete()
                    Relation.objects.filter(user1=receiver, user2=user).delete()
                    
                    return HttpResponse("had a relation but deleted")
                if Relation.objects.filter(user1=receiver, user2=user, status=1).exists():
                    Relation(user1=user,user2=receiver,status=2).save()
                    Relation.objects.get(user1=receiver, user2=user, status=1).delete()
                    return HttpResponse("had a relation from reciever so you are friends")


                

                
            


                
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getdataFriendRequest(request):
    if request.method == "GET" and request.is_ajax:
        receiver= request.GET.get('userid')
        finalText=""
        user = request.user
        if  Relation.objects.filter(user1=user, user2=receiver).exists():
            going_status = Relation.objects.get(user1=user, user2=receiver).status
        else:
            going_status = 0
        if Relation.objects.filter(user1=receiver, user2=user).exists():
            comming_status = Relation.objects.get(user1=receiver, user2=user).status
        else:
            comming_status = 0
        
        if going_status ==0 :
            if comming_status==0:
                finalText= "Add friend"
            elif comming_status==1:
                finalText= "Accept"
            elif comming_status ==2 or going_status==2:
                finalText= "Friends"
        elif going_status == 1:
            finalText= "Request sent"
        elif comming_status ==2 or going_status ==2 :
            finalText= "Friends"
        else:
            finalText= "Error"
        data = {
            'buttonText' : finalText
        }
        return Response(data)
    return HttpResponse("It wasn't GET or AJAX")



        





def send_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated and request.is_ajax:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = NewUser.objects.get(pk=user_id)
			try:
				# Get any friend requests (active and not-active)
				friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
				# find if any of them are active (pending)
				try:
					for request in friend_requests:
						if request.is_active:
							raise Exception("You already sent them a friend request.")
					# If none are active create a new friend request
					friend_request = FriendRequest(sender=user, receiver=receiver)
					friend_request.save()
					payload['response'] = "Friend request sent."
				except Exception as e:
					payload['response'] = str(e)
			except FriendRequest.DoesNotExist:
				# There are no friend requests so create one.
				friend_request = FriendRequest(sender=user, receiver=receiver)
				friend_request.save()
				payload['response'] = "Friend request sent."

			if payload['response'] == None:
				payload['response'] = "Something went wrong."
		else:
			payload['response'] = "Unable to sent a friend request."
	else:
		payload['response'] = "You must be authenticated to send a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")
      

'''This is a class based view which is provided by the Django Framework and it is used to 
change the current user's password '''
class MyPasswordChangeView(PasswordChangeView):
    form_class = MyPasswordChangeForm

    '''Redirects to profile_page after completion'''
    def get_success_url(self):
        return reverse('profile_page')



'''This is the home view and it displays the first page that the user sees'''
def home_view(request):
    current_user = request.user
    books = Book.objects.all()
    cBooks = books.order_by("?")[0:9]

    '''Different values for different request states'''
    if(not current_user.is_anonymous):
        '''Add default Sirtars'''
        if not Sirtar.objects.filter(id_user=current_user).exists():
            utils.create_default_sirtar(current_user.email)
        '''Update the progress by syncing it with Reading Sirtar'''
        utils.update_progress_db("Reading", current_user.email)
        if current_user.first_login:
            return redirect("survey")

        
        dukelexuar = []
        wtrBooks = []
        friends = []
        notifications=[]
        
        relations = Relation.objects.filter(Q(user1=current_user)| Q(user2=current_user)).filter(status=2)
        for relation in relations:   
            if relation.user1.username == current_user.username:
                friends.append(relation.user2)
            else:
                friends.append(relation.user1)
        
        for friend in friends:
            friendNotifications= Notification.objects.filter(user=friend)
            for fN in friendNotifications:
                notifications.append(fN)
        dlcount = Sirtar.objects.get(emri="Reading", id_user=current_user)
        '''Add Reading isbn-s of books to the dukelexuar array so we can use it as a variable in the home template'''
        for isbn in dlcount.books:
            dukelexuar.append(Book.objects.get(isbn=isbn))
      
        '''Add Want to read isbn-s of books to the wtrarray array so we can use it as a variable in the home template'''
        dtlcount = Sirtar.objects.get(
            emri="Want to read", id_user=current_user)
        for bookIsbn in dtlcount.books:
            wtrBooks.append(Book.objects.get(isbn=bookIsbn).isbn)

        '''Get length of arrays to show them as a count on the home page'''
        dlcount = len(dlcount.books)
        dtlcount = len(dtlcount.books)
        klcount = Sirtar.objects.get(emri="Read", id_user=current_user)
        klcount = len(klcount.books)
    else:
        dukelexuar = []
        wtrBooks = []
        friends = []
        notifications=[]
        dlcount = "no data"
        dtlcount = "no data"
        klcount = "no data"   # userR = users.reading
    if Progress.objects.filter(id_user=current_user.id).exists():
        '''Check and update the Progress variables that will be used in the home template'''
        userReadingBooks = Sirtar.objects.get(id_user=request.user, emri = "Reading").books
        progressIsbn = userReadingBooks[-1]
        progressBookObj = Book.objects.get(isbn=progressIsbn)
        progressBook = Progress.objects.get(id_libri=progressBookObj, id_user=request.user)
        progressLibri = progressBook.id_libri
        progressNowPages = progressBook.pages_now
        progressAllPages = progressBook.id_libri.nr_faqeve
        progressPercent = round(float((progressNowPages/progressAllPages)*100), 1)
        progressBookImage = progressBook.id_libri.image_link
        '''Progress Title truncation so it won't overflow the place that it is shown'''
        titleLength = 35
        if len(progressBook.id_libri.titulli)>titleLength:
            progressLibriTitulli = progressBook.id_libri.titulli[:titleLength]+"..."
        else:
            progressLibriTitulli = progressBook.id_libri.titulli[:titleLength]
        
      
    else:
        progressLibri = "no data"
        progressNowPages = "no data"
        progressAllPages = "no data"
        progressLibriTitulli = "no data"
        progressPercent = "no data"
        progressBookImage = ""

    if not current_user:
        current_user = 'anonimous user(not loged in)'
    '''Context variables to use in Home template'''
    context = {
        'books': books,                                                 #All books
        'cbooks': cBooks,                                               #Carousel Books(taken randomly)
        'booksLatest': books.order_by('-viti_publikimit')[0:6],         #Latest books ordered by Published Year
        'booksR': books.order_by('-mes_vleresimit')[0:6],               #Most rated books ordered by Rating Averaga
        'booksFY': books.order_by('?')[0:6],                            #For you books that for now are chosen randomly
        'dlcount': dlcount,                                             #Reading book count
        'klcount': klcount,                                             #Read book count
        'dtlcount': dtlcount,                                           #Want to read book count
        'dukelexuar': dukelexuar,                                       #Reading array(only with isbn-s in an array)
        'wtrBooks' : wtrBooks,                                          #Want to read array(only with isbn-s in an array)
        'progressLibri': progressLibri,                                 #The book that is shown as the current Progress book in the Home page
        'progressNowPages': progressNowPages,                           #The number of pages that have been read of the current Progress Book
        'progressAllPages': progressAllPages,                           #The total number of pages of the current Progress Book
        'progressLibriTitulli': progressLibriTitulli,                   #The title of the current Progress Book
        'progressPercent': progressPercent,                             #The calculated percentage of the current Progress Book
        'progressBookImage': progressBookImage,                         #The cover image of the current Progress Book
        'friends': friends,
        'notifications': notifications
    }
    print("notifications: " + str(notifications.__str__()))
    return render(request, 'libri_im/home.html', context)

def findFriends(request):
    current_user = request.user
    
    query = request.GET.get('searchFriend')
    userList=NewUser.objects.all()
    if query:
        userList = NewUser.objects.filter(Q(username__icontains=query) | (Q(email__icontains=query)) )
    context = {
        'userList' : userList,
    }
       
    return render(request, 'libri_im/friend_list.html', context)

class ProfileDetailView(View):
    def get(self,request,pk,*args,**kwargs):
        if pk==request.user.id:
            return redirect('profile_page_view')
        context = {}
        account = NewUser.objects.get(pk=pk)
        if Relation.objects.filter(user1=request.user, user2=account).exists():
            going_status = Relation.objects.get(user1=request.user, user2=account).status
        else:
            going_status = 0
        if Relation.objects.filter(user1=account, user2=request.user).exists():
            comming_status = Relation.objects.get(user1=account, user2=request.user).status
        else:
            comming_status = 0

        print(going_status)
        print(comming_status)
        

        context = {
            'user':account,
            'userid' : account.id,
            'going_status' : going_status,
            'comming_status' : comming_status,
           
        }

        return render(request , 'libri_im/follower_view.html' , context)

def shfleto_view(request):
    current_user = request.user
    books = Book.objects.all()
    query = request.GET.get('search')
    categoryQuery = request.GET.get('category_name')
    sortQuery =request.GET.get('sort_name')
    try:
        books = Book.objects.all().order_by(request.GET['sort_name'])
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 42)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
    except MultiValueDictKeyError:
        books = Book.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 42)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)

    if query:
        books = Book.objects.filter(Q(titulli__icontains=query) | (Q(autori__icontains=query)) | (
            Q(isbn__icontains=query)) | (Q(kategoria__icontains=query)) | (Q(viti_publikimit__icontains=query)))
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 42)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
    if categoryQuery:
        books = []
        booksAll = Book.objects.all()
        for book in booksAll:
            for kategori in book.kategoria:
                if categoryQuery in kategori:
                    books.append(book)
        books = list(set(books))
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 42)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
    books1 = Book.objects.all()[0:10]
    # categories = books.viti_publikimit
    context = {
        'books': books,
        'books1': books1,
        'sortQuery' : sortQuery,
        'categoryQuery' : categoryQuery,
 

        #  'categories' : categories,
    }
    return render(request, 'libri_im/shfleto.html', context)

def shfleto_view1(request):
    current_user = request.user
    books = Book.objects.all()
    booksAll = Book.objects.all()
    query = request.GET.get('search')
    categoryQuery = request.GET.get('category_name')
    sortQuery =request.GET.get('sort_name')
    try:
        books = Book.objects.all().order_by(request.GET['sort_name'])
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 42)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
    except MultiValueDictKeyError:
        books = Book.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 42)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)

    if query:
        books = Book.objects.filter(Q(titulli__icontains=query) | (Q(autori__icontains=query)) | (
            Q(isbn__icontains=query)) | (Q(kategoria__icontains=query)) | (Q(viti_publikimit__icontains=query)))
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 42)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
    if categoryQuery:
        books = []
        booksAll = Book.objects.all()
        for book in booksAll:
            for kategori in book.kategoria:
                if categoryQuery in kategori:
                    books.append(book)
        books = list(set(books))
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 42)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
    books1 = Book.objects.all()[0:10]
    # categories = books.viti_publikimit
    wtrBooks = Sirtar.objects.get(emri="Want to read", id_user=current_user).books
    readBooks = Sirtar.objects.get(emri="Read", id_user=current_user).books
    readingBooks = Sirtar.objects.get(emri="Reading", id_user=current_user).books
    print(wtrBooks)
    context = {
        'books': booksAll,
        'books1': books1,
        'sortQuery' : sortQuery,
        'categoryQuery' : categoryQuery,
        'wtrBooks': Sirtar.objects.get(emri="Want to read", id_user=current_user).books,
        'readBooks': Sirtar.objects.get(emri="Read", id_user=current_user).books,
        'readingBooks': Sirtar.objects.get(emri="Reading", id_user=current_user).books,
        
    }
    return render(request, 'libri_im1/discover1.html', context)

'''This is a class based view that is used to create and process the user registration form'''
class RegistationView(View):
    def get(self, request):
        return render(request, 'libri_im1/register1.html')

    '''The method that defines what happens if the request is a POST request.
       This method is used to: GET USER DATA, VALIDATE, create a user account'''
    def post(self, request):

        '''Get the fields that the user submited'''
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']
        context = {
            'fieldValues': request.POST
        }

        '''Check if it is a unique username'''
        if not NewUser.objects.filter(username=username).exists():
            '''Check if it is a unique email'''
            if not NewUser.objects.filter(email=email).exists():
                '''Check if the password has at least 8 characters'''
                if len(password) < 8:
                    messages.warning(
                        request, 'Password is too short, it has to be at least 8 characters.')
                    return render(request, 'libri_im1/register1.html', context)
                    '''Check if the password and confirm password are the same'''
                if password != password2:
                    messages.warning(
                        request, 'Password and confirmation does not match.')
                    return render(request, 'libri_im1/register1.html', context)
                '''Create a new user from the submited data''' 
                user = NewUser.objects.create_user(
                    email=email, username=username)
                user.set_password(password)
                user.is_active = False
                user.save()
                '''Create the 3 default sirtars'''
                utils.create_default_sirtar(email)
                '''Send te activation email'''
                utils.send_email_activation(request,user)
                messages.success(
                    request, 'Your account has been created succesfully. To use this account, activate it with the link that we have sent you by email.')
                return render(request, 'libri_im1/register1.html')
            else:
                messages.warning(
                    request, f'Email: "{request.POST["email"]}" it\'s taken.')
                return render(request, 'libri_im1/register1.html')
        else:
            messages.warning(
                request, f'Username: "{request.POST["username"]}" it\'s taken.')
            return render(request, 'libri_im1/register1.html')

'''This is a class based view that handles the authentication of the activation token and redirects the user to the login page'''
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = NewUser.objects.get(pk=id)
            '''Check if the token has been already used(users can't use the same link twice)'''
            if not account_activation_token.check_token(user, token):
                messages.warning(
                    request, 'Your account has been activated before. You can log in.')
                return redirect('login1')
            '''What happensn after activation'''
            if user.is_active:
                return redirect('login1')
            user.is_active = True
            user.save()

            messages.success(
                request, 'Your account has been activated. You can log in now.')
            return redirect('login1')

        except Exception as ex:
            pass

        return redirect('login1')

'''This is a function based view that defines where to redirect the user after he logs out'''
def logout_view(request):
    logout(request)
    return redirect("home1")

'''This is a function based view that defines the process of checking the data and logging in the user after data validation'''
def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    '''Redirect the user if already logged in'''
    if user.is_authenticated:
        return redirect("home1")
    


    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    '''Validate the login form from the POST request that is submited'''
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        '''Check the form data'''
        if form.is_valid():
            '''Authenticate the user'''
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            '''If user exists'''
            if user:
                '''Check if the user activated the account'''
                if not user.is_active:
                    messages.warning(
                        request, 'Your account is not activated yet. To use this account please activate with the link we have sent you in email.')
                    return redirect('login')
                '''login the user'''
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("home1")
        else:
            messages.warning(request, 'Email or password is wrong.')
            return redirect('login1')
    else:
        form = UserAuthenticationForm()
    context['login_form'] = form
    #return render(request, "libri_im/login.html", context)
    return render(request, 'libri_im1/login1.html', context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


class BookCreateView(CreateView):
    model = Book
    fields = ['isbn', 'titulli', 'autori', 'kategoria', 'pershkrimi',
              'mes_vleresimit', 'nr_vleresimit', 'nr_faqeve', 'viti_publikimit', 'image_link']

    def get_success_url(self):
        return reverse('admin_home1')
   
'''Takes the Book model and returns to the home.html page
This class based view lists all the books that are saved in
the database and orders DESC (from the end)'''
class BookListView(ListView):
   
    model = Book
    template_name = 'backend/home.html'
    context_object_name = 'books'

    def get_success_url(self):
        return reverse('admin_home')
    ordering = ['-id_libri']

'''This class lists details of a single book'''
class BookDetailView(DetailView):
    model = Book

'''This class deletes a book, it redirects you to delete.html file and asks you 
if you are sure that you want to delete this specific home. After you click yes or cancel
it returns you to admin_home'''
class BookDeleteView(DeleteView):
    model = Book
    success_url = '/'
    template_name = 'backend1/delete1.html'

    def get_success_url(self):
        return reverse('admin_home1')

'''This class based view helps you to edit informations of a specific book, it takes fields that are
declared below at variable fields and after clicking save it redirects you to admin_home '''
class EditBook(UpdateView):
    model = Book
    fields = ['isbn', 'titulli', 'autori', 'kategoria', 'pershkrimi',
              'mes_vleresimit', 'nr_vleresimit', 'nr_faqeve', 'viti_publikimit', 'image_link']
    template_name = 'libri_im1/backend1/book_update1.html'

    def get_success_url(self):
        return reverse('admin_home1')
class EventCreateView(CreateView):
    model = Event
    fields = ['name', 'start_date', 'end_date', 'nr_books','books']

    def get_success_url(self):
        return reverse('admin_home1')

class EventListView(ListView):
   
    model = Event
    template_name = 'backend1/event.html'
    context_object_name = 'events'

    def get_success_url(self):
        return reverse('admin_home1')
    ordering = ['-id']
class EventDetailView(DetailView):
    model = Event

'''This class deletes a book, it redirects you to delete.html file and asks you 
if you are sure that you want to delete this specific home. After you click yes or cancel
it returns you to admin_home'''
class EventDeleteView(DeleteView):
    model = Event
    success_url = '/'
    template_name = 'backend1/deleteEvent1.html'

    def get_success_url(self):
        return reverse('admin_home1')
class EditEvent(UpdateView):
    model = Event
    fields = ['name', 'start_date', 'end_date', 'nr_books','books']
    template_name = 'libri_im1/backend1/edit_event.html'

    def get_success_url(self):
        return reverse('admin_home1')
'''This is a class based view that shows to the user their data like Username, Email, Profile pic and registration date'''
class ProfilePageView(DetailView):
    model = NewUser
    template_name = 'libri_im/profile_page.html'
    context_object_name = 'user'
    '''This function is executed before the other functions and redirects the user
    if he is not authenticated or not activte'''
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')
        if not self.request.user.is_active:
            return redirect('logout')
        return super().dispatch(request, *args, **kwargs)
        
    '''Redirect after all other functions'''
    def get_success_url(self):
        return reverse('profile_page')

    def get_object(self):
        return self.request.user

'''This is a class based view that allows the user to change their data'''
class EditProfile(UpdateView):
 
    model = NewUser
    fields = ['username', 'profileImg', 'email']
    template_name = 'libri_im/profile_page_update.html'
    
    '''Redirect after submit'''
    def get_success_url(self):
        return reverse('profile_page')

    def get_object(self):
        return self.request.user
    '''Change the default form validation behaviour'''
    def form_valid(self, form):
        if 'email' in form.changed_data:
            self.request.user.is_active = False
            utils.send_email_activation(self.request,self.request.user)
            messages.success(
                self.request, f'Your email has been changed succesfully. To use this account, activate it with the link that we have sent you by email at "{self.request.user.email}"')

        return super().form_valid(form)

def ProfilePageViewDetails(request):
    current_user = request.user
    if current_user.is_anonymous:
        return redirect('home')
    #Get Read Books from the database
    ReadSirtar = Sirtar.objects.get(emri="Read", id_user=request.user).books
    ReadBooks = []
    for bookIsbn in ReadSirtar:
        ReadBooks.append(Book.objects.get(isbn=bookIsbn))
    #Get Reading Books from the database
    ReadingSirtar = Sirtar.objects.get(emri="Reading", id_user=request.user).books
    ReadingBooks = []
    for bookIsbn in ReadingSirtar:
        ReadingBooks.append(Book.objects.get(isbn=bookIsbn))
    #Get Want to read Books from the database
    WtrSirtar = Sirtar.objects.get(emri="Want to read", id_user=request.user).books
    WtrBooks = []
    for bookIsbn in WtrSirtar:
        WtrBooks.append(Book.objects.get(isbn=bookIsbn))
    
    userFriends = Relation.objects.filter(Q(user1=current_user) | Q(user2=current_user)).filter(status=2)
    Read = ReadBooks
    Reading = ReadingBooks
    WantToRead = WtrBooks

    context = {
        'currentUser' : current_user,
        'wantToRead': WantToRead,
        'reading': Reading,
        'read': Read,
        'readCount': len(Read),
        'readingCount': len(Reading),
        'wantToReadCount': len(WantToRead),
        'userFriendsCount': len(userFriends),

        

    }
    return render(request, 'libri_im1/profile_page_view1.html', context)


class CommentDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    model = Comment
    template_name = 'libri_im/CommentDeleteConfirm.html'
    
    def get_success_url(self):
        return self.request.path[:20]
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.name
    
class CommentEditView(UserPassesTestMixin,LoginRequiredMixin,UpdateView):
    model = Comment
    fields = ['body']
    template_name = 'libri_im/Comment_edit.html'
    
    def get_success_url(self):
        return self.request.path[:20]

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.name


class BookDV(View):
    def get(self,request,isbn,*args,**kwargs):
        current_user = request.user
        book = Book.objects.get(isbn=isbn)
        form = NewCommentForm()
        
        comments = Comment.objects.filter(book=book).order_by('-date_added')
        if not current_user.is_anonymous:
            wtrSirtar = Sirtar.objects.get(emri="Want to read", id_user=current_user).books
            readSirtar = Sirtar.objects.get(emri="Read", id_user=current_user).books
            readingSirtar = Sirtar.objects.get(emri="Reading", id_user=current_user).books
        else:
            wtrSirtar = []
            readSirtar = []
            readingSirtar = []
        context = {
            'book':book,
            'form':form,
            'comments':comments,
            'currentUser': current_user,
            'wtrBooks': wtrSirtar,
            'readBooks': readSirtar,
            'readingBooks': readingSirtar,

        }

        return render(request,'libri_im1/book-detail1.html' , context)

    def post(self,request,isbn,*args,**kwargs):
        book = Book.objects.get(isbn=isbn)
        form = NewCommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.name = request.user
            new_comment.book = book
            new_comment.save()
            form = NewCommentForm()

        comments = Comment.objects.filter(book=book).order_by('-date_added')

        context = {
            'book':book,
            'form':form,
            'comments':comments,
        }

        # return HttpResponse("<p>Hello</p>")

        return render(request,'libri_im/book-detail.html' , context)

class CommentReplyView(View):
    def post(self,request,pk,isbn,*args,**kwargs):
        book = Book.objects.get(isbn=isbn)
        parent_comment = Comment.objects.get(pk=pk)
        form = NewCommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.name = request.user
            new_comment.book = book
            new_comment.parent = parent_comment
            new_comment.save()

        return redirect('book-detail', isbn=isbn)

class AddCommentLike(View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddCommentDislike(View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddChildCommentLike(View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddChildCommentDislike(View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


'''This function based view takes the action of a clicked button "Want to read" that is handled with ajax and 
gets the isbn and adds it to array WantToReadSirtar.books in sirtari model and checks if this book is in 
Want to read array and it removes it then adds the isbn in READING array'''
def wantToReadPost(request):
    if request.method == "POST" and request.is_ajax:
        isbn = int(request.POST.get('isbn'))
        new_sirtar = Sirtar.objects.get(emri="Want to read", id_user=request.user)
        utils.add_to_sirtar("Want to read", isbn, request)
        return HttpResponse('<p>Success</p>')
    return HttpResponse('<p>Error</p>')

'''This function based view takes the action of a clicked button READING that is handled with ajax and 
gets the isbn and adds it to array READING in sirtari model and checks if this book is in 
Want to read array and it removes it then adds the isbn in READING array'''
def ReadingPost(request):
    if request.method == "POST" and request.is_ajax:
        isbn = int(request.POST.get('isbn'))
        new_sirtar = Sirtar.objects.get(emri="Reading", id_user=request.user)
        utils.add_to_sirtar("Reading", isbn, request)
        return HttpResponse('<p>Success</p>')
    return HttpResponse('<p>Error</p>')

'''This function based view handles the GET request sent when the "Reading"
button is clicked. It provides all of the variables that are needed for the AJAX function'''
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getdataReading(request):
    if request.method == 'GET' and request.is_ajax:
        return utils.get_data_function(request, "Reading")
    return HttpResponse("GET Failed")

'''This function based view handles the GET request sent when the "Want to read"
button is clicked. It provides all of the variables that are needed for the AJAX function'''
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getdataWtr(request):
    if request.method == 'GET' and request.is_ajax:
        return utils.get_data_function(request, "Want to read")
    return HttpResponse("GET Failed")

def ReadPost(request):
    if request.method == "POST" and request.is_ajax:
        isbn = int(request.POST.get('isbn'))
        new_sirtar = Sirtar.objects.get(emri="Read", id_user=request.user)
        utils.add_to_sirtar("Read", isbn, request)
        return HttpResponse('<p>Success</p>')
    return HttpResponse('<p>Error</p>')


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getdataRead(request):
    if request.method == 'GET' and request.is_ajax:
        return utils.get_data_function(request, "Read")
    return HttpResponse("GET Failed")


def progressPost(request):
    if request.method == "POST" and request.is_ajax:
        userSirtar = Sirtar.objects.get(emri="Reading", id_user=request.user)
        ReadSirtar = Sirtar.objects.get(emri="Read",id_user = request.user)
        inputPost = request.POST.get('progressPages')
        progressBookIsbn = int(userSirtar.books[len(userSirtar.books)-1])
        progressBook = Book.objects.get(isbn=progressBookIsbn)
        progressObj = Progress.objects.get(id_user=request.user,id_libri=progressBook)
        if not inputPost=='':
            if int(inputPost)>0 and int(inputPost)<progressBook.nr_faqeve:
                progressInput = int(inputPost)
            elif int(inputPost) == progressBook.nr_faqeve:
                userSirtar.books.remove(progressBook.isbn)
                ReadSirtar.books.append(progressBook.isbn)
                userSirtar.save(update_fields=['books'])
                ReadSirtar.save(update_fields=['books'])
                progressInput = int(inputPost)
            elif int(inputPost)>progressBook.nr_faqeve:
                progressInput = progressBook.nr_faqeve-1
            elif int(inputPost)<=0:
                progressInput = 0
        else:
            progressInput=progressObj.pages_now
      
        progressObj.pages_now = progressInput
        progressObj.save(update_fields=['pages_now'])
        return HttpResponse('<p>Pages Updated Successfuly</p>')
    return HttpResponse('<p>Error</p>')

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getdataProgress(request):
    if request.method =="GET" and request.is_ajax:
        userSirtar = Sirtar.objects.get(emri="Reading", id_user=request.user).books
        readSirtar = Sirtar.objects.get(emri="Read", id_user=request.user).books
        if len(userSirtar)>=1:
            progressBookIsbn = int(userSirtar[len(userSirtar)-1])
            progressBook = Book.objects.get(isbn=progressBookIsbn)
            progressImage = progressBook.image_link
            progressTitle = progressBook.titulli
            readingCount = len(userSirtar)
            readCount = len(readSirtar)
            progressObj = Progress.objects.get(id_user=request.user.id,id_libri=progressBook)
            progressNowPages = progressObj.pages_now
            progressAllPages = progressObj.id_libri.nr_faqeve
            progressPercent = round(
                    float((progressNowPages/progressAllPages)*100), 1)
            finalString = ""
        else:
            progressBookIsbn = -1
            progressBook =-1
            progressImage = -1
            progressTitle = -1
            readingCount = len(userSirtar)
            readCount = len(readSirtar)
            progressObj = -1
            progressNowPages = -1
            progressAllPages = -1
            progressPercent = -1
            finalString = "You should add books to the Reading shelf to show the progress."
        data = {
            'progressNowPages': progressNowPages,
            'progressAllPages': progressAllPages,
            'progressPercent': progressPercent,
            'finalString' : finalString,
            'progressImage': progressImage,
            'progressTitle': progressTitle,
            'readingCount' : readingCount,
            'readCount' : readCount,

        }
        return Response(data)
    return HttpResponse('<p>Error</p>')



def selectBookPost(request):
    if request.method=="POST" and request.is_ajax:
        selectedBookIsbn = int(request.POST.get('isbn'))
        readingSirtar = Sirtar.objects.get(id_user = request.user,emri="Reading")
        readingSirtar.books.remove(selectedBookIsbn)
        readingSirtar.books.append(selectedBookIsbn)
        readingSirtar.save(update_fields=['books'])
        return HttpResponse("Book appended to end")
    return HttpResponse("Error")
        


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getdataSelectBook(request):
    if request.method == 'GET' and request.is_ajax:
        userReadingBooks = Sirtar.objects.get(id_user=request.user, emri = "Reading").books
        progressIsbn = userReadingBooks[-1]
        progressBookObj = Book.objects.get(isbn=progressIsbn)
        progressBook = Progress.objects.get(id_libri=progressBookObj, id_user=request.user)
        progressNowPages = progressBook.pages_now
        progressAllPages = progressBook.id_libri.nr_faqeve
        # Progress Title Truncation
        titleLength = 35
        if len(progressBook.id_libri.titulli)>titleLength:
            progressLibriTitulli = progressBook.id_libri.titulli[:titleLength]+"..."
        else:
            progressLibriTitulli = progressBook.id_libri.titulli[:titleLength]
        progressPercent = float(round(
            (progressNowPages/progressAllPages)*100, 1))
        progressBookImage = progressBook.id_libri.image_link
        data = {
            'progressBookImage' : progressBookImage,
            'progressNowPages' : progressNowPages,
            'progressAllPages' : progressAllPages,
            'progressLibriTitulli' : progressLibriTitulli,
            'progressPercent' : progressPercent,
        }
    return Response(data)

def userSurvey(request):
    '''Survey backend'''
    current_user = request.user
    current_user.first_login = False
    current_user.save(update_fields=['first_login'])
    currentFav = current_user.fav_categories
    books = Book.objects.all().order_by('-mes_vleresimit')[:32]
    categories = ["Art","Economic","Fantasy","Fiction","Gothic","Historical","Horror","Humor","Inspirational","Mystery","Nonfiction","Poetry","Romance","Thriller" ]
    context= {
        'books' : books,
        'categories' : categories,
        'user': current_user,
        'currentFav' : currentFav,
        'readBooks': Sirtar.objects.get(emri="Read", id_user=current_user).books,
    }
    return render(request,"libri_im/survey.html", context)


# class AddFollower(LoginRequiredMixin, View):
#     def Follow(self, request, pk, *args, **kwargs):
#         users=Followers.objects.all()

#         users.followers.add(request.user)
#         return redirect('profile_page_view')


# class RemoveFollower(LoginRequiredMixin, View):
#     def RemoveFollow(self, request, pk, *args, **kwargs):
#         users=Followers.objects.all()

#         users.followers.remove(request.user)
#         return redirect('profile_page_view')


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getSearched(request):
    if request.method=="GET" and request.is_ajax:
        searchedArray = []
        getInput = request.GET.get('searchInput')
        filteredBooks = Book.objects.filter(Q(titulli__icontains=getInput) | (Q(autori__icontains=getInput)) | (
           Q(isbn__icontains=getInput)) | (Q(kategoria__icontains=getInput)) | (Q(viti_publikimit__icontains=getInput)))
        #for book in filteredBooks:
        #    searchedArray.append(book.isbn)
        booksobj = Book.objects.all()
        serialized = LibratSerializer(filteredBooks, many=True)
        data = {
            'searched' : searchedArray ,
            'filteredBooks': serialized.data

        }
        return Response(data)


def categoryPost(request):
    if request.method == "POST" and request.is_ajax:
        category = request.POST.get('category')
        user = request.user
        currentCategories = user.fav_categories
        
        if category in currentCategories:
            currentCategories.remove(category)
            print("Removed"+category)
            user.save(update_fields=['fav_categories'])
        else:
            # if len(currentCategories) >=3:
            #     return HttpResponse("<p>Can't add more than 3 categories</p>")
                
            currentCategories.append(category)
            print("Appended"+category)
            user.save(update_fields=['fav_categories'])
        
        return HttpResponse('<p>Success category added</p>')
    return HttpResponse('<p>Error</p>')


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getCategory(request):
    if request.method == 'GET' and request.is_ajax:
        user = request.user
        currentCategories = user.fav_categories
        clickedCategory = str(request.GET.get('category'))
        print(currentCategories)
        print(clickedCategory)
        added = None
        if clickedCategory in currentCategories:
            added = True
        else:
            added = False
        data = {
            'added' : added
        }
        return Response(data)
    return HttpResponse("GET Failed")



def home1(request):
    current_user = request.user
    books = Book.objects.all()

    '''Different values for different request states'''
    if(not current_user.is_anonymous):
        '''Add default Sirtars'''
        if not Sirtar.objects.filter(id_user=current_user).exists():
            utils.create_default_sirtar(current_user.email)
        '''Update the progress by syncing it with Reading Sirtar'''
        utils.update_progress_db("Reading", current_user.email)
        if current_user.first_login:
            return redirect("survey")

        
        dukelexuar = []
        wtrBooks = []
        friends = []
        notifications=[]

        allNotifications= Notification.objects.all().order_by("-dateCreated")
        relations = Relation.objects.filter(Q(user1=current_user)| Q(user2=current_user)).filter(status=2)

        for relation in relations:   
            if relation.user1.username == current_user.username:
                friends.append(relation.user2)
            else:
                friends.append(relation.user1)

        for notification in allNotifications:
            if notification.user in friends:
                notifications.append(notification)


        dlcount = Sirtar.objects.get(emri="Reading", id_user=current_user)
        '''Add Reading isbn-s of books to the dukelexuar array so we can use it as a variable in the home template'''
        for isbn in dlcount.books:
            dukelexuar.append(Book.objects.get(isbn=isbn))

        '''Add Want to read isbn-s of books to the wtrarray array so we can use it as a variable in the home template'''
        dtlcount = Sirtar.objects.get(
            emri="Want to read", id_user=current_user)
        for bookIsbn in dtlcount.books:
            wtrBooks.append(Book.objects.get(isbn=bookIsbn).isbn)

        '''Get length of arrays to show them as a count on the home page'''
        dlcount = len(dlcount.books)
        dtlcount = len(dtlcount.books)
        klcount = Sirtar.objects.get(emri="Read", id_user=current_user)
        klcount = len(klcount.books)
    else:
        dukelexuar = []
        wtrBooks = []
        friends = []
        notifications=[]
        dlcount = "no data"
        dtlcount = "no data"
        klcount = "no data"   # userR = users.reading
    if Progress.objects.filter(id_user=current_user.id).exists():
        '''Check and update the Progress variables that will be used in the home template'''
        userReadingBooks = Sirtar.objects.get(id_user=request.user, emri = "Reading").books
        progressIsbn = userReadingBooks[-1]
        progressBookObj = Book.objects.get(isbn=progressIsbn)
        progressBook = Progress.objects.get(id_libri=progressBookObj, id_user=request.user)
        progressLibri = progressBook.id_libri
        progressNowPages = progressBook.pages_now
        progressAllPages = progressBook.id_libri.nr_faqeve
        progressPercent = round(float((progressNowPages/progressAllPages)*100), 1)
        progressBookImage = progressBook.id_libri.image_link
        '''Progress Title truncation so it won't overflow the place that it is shown'''
        titleLength = 35
        if len(progressBook.id_libri.titulli)>titleLength:
            progressLibriTitulli = progressBook.id_libri.titulli[:titleLength]+"..."
        else:
            progressLibriTitulli = progressBook.id_libri.titulli[:titleLength]

    else:
        progressLibri = "no data"
        progressNowPages = "no data"
        progressAllPages = "no data"
        progressLibriTitulli = "no data"
        progressPercent = "no data"
        progressBookImage = ""

    if not current_user:
        current_user = 'anonimous user(not loged in)'
    '''Context variables to use in Home template'''
    context = {
        'books': books,                                                 #All books
        'booksRandom': books.order_by('?')[0:6],                         #For you books that for now are chosen randomly
        'dlcount': dlcount,                                             #Reading book count
        'klcount': klcount,                                             #Read book count
        'dtlcount': dtlcount,                                           #Want to read book count
        'dukelexuar': dukelexuar,                                       #Reading array(only with isbn-s in an array)
        'wtrBooks' : wtrBooks,                                          #Want to read array(only with isbn-s in an array)
        'progressLibri': progressLibri,                                 #The book that is shown as the current Progress book in the Home page
        'progressNowPages': progressNowPages,                           #The number of pages that have been read of the current Progress Book
        'progressAllPages': progressAllPages,                           #The total number of pages of the current Progress Book
        'progressLibriTitulli': progressLibriTitulli,                   #The title of the current Progress Book
        'progressPercent': progressPercent,                             #The calculated percentage of the current Progress Book
        'progressBookImage': progressBookImage,                         #The cover image of the current Progress Book
        'friends': friends,
        'notifications': notifications
    }

    return render(request, 'libri_im1/home1.html',context)


def login1(request):
    return render(request, 'libri_im1/login1.html')
def register1(request):
    return render(request, 'libri_im1/register1.html')
def discover1(request):
    current_user = request.user
    books = Book.objects.all()
    query = request.GET.get('search')
    categoryQuery = request.GET.get('category_name')
    sortQuery =request.GET.get('sort_name')
    try:
        books = Book.objects.all().order_by(request.GET['sort_name'])
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 42)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
    except MultiValueDictKeyError:
        books = Book.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 42)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)

    if query:
        books = Book.objects.filter(Q(titulli__icontains=query) | (Q(autori__icontains=query)) | (
            Q(isbn__icontains=query)) | (Q(kategoria__icontains=query)) | (Q(viti_publikimit__icontains=query)))
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 42)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
    if categoryQuery:
        books = []
        booksAll = Book.objects.all()
        for book in booksAll:
            for kategori in book.kategoria:
                if categoryQuery in kategori:
                    books.append(book)
        books = list(set(books))
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 42)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
    books1 = Book.objects.all()[0:10]
    # categories = books.viti_publikimit
    context = {
        'books': books,
        'books1': books1,
        'sortQuery' : sortQuery,
        'categoryQuery' : categoryQuery,
        'wtrBooks' : Sirtar.objects.get(emri="Want to read", id_user=current_user).books,
        'readBooks' : Sirtar.objects.get(emri="Read", id_user=current_user).books ,
        'readingBooks' : Sirtar.objects.get(emri="Reading", id_user=current_user).books,

        #  'categories' : categories,
    }
    return render(request,'libri_im1/discover1.html',context)
def eventsView(request):
    user = request.user
    events = Event.objects.all()
    currentdate = date.today()
    nowEvents = []
    nowEventsId = []
    joinedEvents = []
    joinedEventsId = request.user.events
    for id in joinedEventsId:
        joinedEvents.append(Event.objects.get(id=id))
    for event in events:
        startdate = event.start_date
        enddate = event.end_date
        if startdate<=currentdate<=enddate:
            nowEvents.append(event)
            nowEventsId.append(event.id)
    print(nowEvents)
    context = {
        'events' : events,
        'nowEvents': nowEvents,
        'joinedEvents':joinedEvents,
        'nowEventsId' : nowEventsId,
    }

    return render(request, 'libri_im/events.html', context)


def post_addevent(request):
    user = request.user
    userEvents = user.events
    eventid = int(request.POST.get('eventid'))
    if request.method=='POST' and request.is_ajax:
        if eventid not in userEvents:
            userEvents.append(eventid)
            user.save(update_fields=['events'])
        else:
            userEvents.remove(eventid)
            user.save(update_fields=['events'])
        return HttpResponse('<p>Success</p>')
    return HttpResponse('<p>Failed, not post or not get or not ajax</p>')

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getEvents(request):
    if request.method == 'GET' and request.is_ajax:
        user = request.user
        userEvents  = user.events
        eventid= int(request.GET.get('eventid'))
        added=None
        if eventid in userEvents:
            added = True
        else:
            added = False
        data = {
            'added' : added
        }
        return Response(data)
    return HttpResponse("GET Failed")
