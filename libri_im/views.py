from decimal import Context
from django.utils.datastructures import MultiValueDictKeyError
from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from .serializers import LibratSerializer, UsersSerializer, SirtarSerializer
from .models import Book, NewUser, Progress, Sirtar,Comment
from .forms import NewCommentForm, RegistrationForm, UserAuthenticationForm, MyPasswordChangeForm
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  DeleteView,
                                  UpdateView,
                                  DetailView)
from .utils import account_activation_token
#from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth
from django.views import View
from django.urls import reverse, reverse_lazy
from django.db import models
from django.db.models import Q, F
from . import myfunctions
from django.core.paginator import PageNotAnInteger, Paginator


class MyPasswordChangeView(PasswordChangeView):
    form_class = MyPasswordChangeForm

    def get_success_url(self):
        return reverse('profile_page')


@api_view(['GET'])
def backendOverView(request):
    backendUrls = {
        'Books': '/books',
        'Specific Books': '/books/<id>',
    }
    return Response(backendUrls)


@api_view(['GET'])
def booksList(request):
    booksObj = Book.objects.all()
    serializer = LibratSerializer(booksObj, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def specificBook(request, pk):
    bookObj = Book.objects.get(id_libri=pk)
    serializer = LibratSerializer(bookObj, many=False)
    return Response(serializer.data)


def home_view(request):
    current_user = request.user
    books = Book.objects.all()
    cBooks = books.order_by("?")[0:9]

    if(not current_user.is_anonymous):
        # sirtar = Sirtar.objects.all()
        if not Sirtar.objects.filter(id_user=current_user).exists():
            myfunctions.create_default_sirtar(current_user.email)
        myfunctions.update_progress_db("Reading", current_user.email)

        dlcount = Sirtar.objects.get(emri="Reading", id_user=current_user)
        dlcount = len(dlcount.books)
        dtlcount = Sirtar.objects.get(
            emri="Want to read", id_user=current_user)

        dtlcount = len(dtlcount.books)
        klcount = Sirtar.objects.get(emri="Read", id_user=current_user)
        klcount = len(klcount.books)

    else:
        dlcount = "no data"
        dtlcount = "no data"
        klcount = "no data"   # userR = users.reading
    if Progress.objects.filter(id_user=current_user.id).exists():
        progressArr = Progress.objects.filter(id_user=current_user.id)
        progress = progressArr[progressArr.count()-1]
        progressLibri = progress.id_libri
        progressUser = progress.id_user
        progressNowPages = progress.pages_now
        progressAllPages = progress.id_libri.nr_faqeve
        progressLibriTitulli = progress.id_libri.titulli[0:30]+"..."
        progressPercent = round(
            float((progressNowPages/progressAllPages)*100), 1)
        progressBookImage = progress.id_libri.image_link
    else:
        progressLibri = "no data"
        progressUser = "no data"
        progressNowPages = "no data"
        progressAllPages = "no data"
        progressLibriTitulli = "no data"
        progressPercent = "no data"
        progressBookImage = ""

    if not current_user:
        current_user = 'anonimous user(not loged in)'
    context = {
        # 'current_username' : current_user,
        'books': books,
        'cbooks': cBooks,
        'booksLatest': books.order_by('-viti_publikimit')[0:6],
        'booksR': books.order_by('-mes_vleresimit')[0:6],
        'booksFY': books.order_by('?')[0:6],
        'dlcount': dlcount,
        'klcount': klcount,
        'dtlcount': dtlcount,

        'progressLibri': progressLibri,
        'progressUser': progressUser,
        'progressNowPages': progressNowPages,
        'progressAllPages': progressAllPages,
        'progressLibriTitulli': progressLibriTitulli,
        'progressPercent': progressPercent,
        'progressBookImage': progressBookImage,
    }

    return render(request, 'libri_im/home.html', context)


def shfleto_view(request):
    books = Book.objects.all()
    query = request.GET.get('search')

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
    books1 = Book.objects.all()[0:10]
    # categories = books.viti_publikimit
    context = {
        'books': books,
        'books1': books1,


        #  'categories' : categories,
    }
    return render(request, 'libri_im/shfleto.html', context)


class RegistationView(View):
    def get(self, request):
        return render(request, 'libri_im/register.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        context = {
            'fieldValues': request.POST
        }

        if not NewUser.objects.filter(username=username).exists():
            if not NewUser.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.warning(
                        request, 'Password is too short, it has to be at least 8 characters.')
                    return render(request, 'libri_im/register.html', context)
                if password != password2:
                    messages.warning(
                        request, 'Password and confirmation does not match.')
                    return render(request, 'libri_im/register.html', context)

                user = NewUser.objects.create_user(
                    email=email, username=username)
                user.set_password(password)
                user.is_active = False
                user.save()
                # creates 3 default sirtars
                myfunctions.create_default_sirtar(email)

                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account in "Sirtari"'

                activate_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    'Hello '+user.username +
                    ', please click in the link below to activate your account in "Sirtari" \n'+activate_url,
                    'starlabs.pip6@gmail.com',
                    [request.POST['email']],
                )
                email.send(fail_silently=False)
                messages.success(
                    request, 'Your account has been created succesfully. To use this account, activate it with the link that we have sent you by email.')
                return render(request, 'libri_im/register.html')
            else:
                messages.warning(
                    request, f'Email: "{request.POST["email"]}" it\'s taken.')
                return render(request, 'libri_im/register.html')
        else:
            messages.warning(
                request, f'Username: "{request.POST["username"]}" it\'s taken.')
            return render(request, 'libri_im/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = NewUser.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                messages.warning(
                    request, 'Your account has been activated before. You can log in.')
                return redirect('login')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(
                request, 'Your account has been activated. You can log in now.')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


def logout_view(request):
    logout(request)
    return redirect("home")


def login_view(request, *args, **kwargs):
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
                if not user.is_active:
                    messages.warning(
                        request, 'Your account is not activated yet. To use this account please activate with the link we have sent you in email.')
                    return redirect('login')
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("home")
        else:
            messages.warning(request, 'Email or password is wrong.')
            return redirect('login')
    else:
        form = UserAuthenticationForm()
    context['login_form'] = form
    return render(request, "libri_im/login.html", context)


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
        return reverse('admin_home')


class BookListView(ListView):
    model = Book
    template_name = 'backend/home.html'
    context_object_name = 'books'

    def get_success_url(self):
        return reverse('admin_home')
    ordering = ['id_libri']


class BookDetailView(DetailView):
    model = Book


class BookDeleteView(DeleteView):
    model = Book
    success_url = '/'
    template_name = 'backend/delete.html'

    def get_success_url(self):
        return reverse('admin_home')


class EditBook(UpdateView):
    model = Book
    fields = ['isbn', 'titulli', 'autori', 'kategoria', 'pershkrimi',
              'mes_vleresimit', 'nr_vleresimit', 'nr_faqeve', 'viti_publikimit', 'image_link']
    template_name = 'libri_im/backend/addbook.html'

    def get_success_url(self):
        return reverse('admin_home')


class ProfilePageView(DetailView):
    model = NewUser
    template_name = 'libri_im/profile_page.html'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse('profile_page')

    def get_object(self):
        return self.request.user


class EditProfile(UpdateView):
    model = NewUser
    fields = ['username', 'profileImg', 'email']
    template_name = 'libri_im/profile_page_update.html'

    def get_success_url(self):
        return reverse('profile_page')

    def get_object(self):
        return self.request.user


def ProfilePageViewDetails(request):
    current_user = request.user
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
    
    Read = ReadBooks
    Reading = ReadingBooks
    WantToRead = WtrBooks

    context = {
        'currentUser' : current_user,
        'WantToRead': WantToRead,
        'Reading': Reading,
        'Read': Read,
        'ReadCount': len(Read),
        'ReadingCount': len(Reading),
        'WantToReadCount': len(WantToRead),
        

    }
    return render(request, 'libri_im/profile_page_view.html', context)


# class BookDV(DetailView):
#     model = Book
#     template_name = 'libri_im/book-detail.html'

#     def get_object(self, queryset=None):
#         return Book.objects.get(isbn=self.kwargs.get("isbn"))

class BookDV(View):
    def get(self,request,isbn,*args,**kwargs):
        book = Book.objects.get(isbn=isbn)
        form = NewCommentForm()

        comments = Comment.objects.filter(book=book).order_by('-date_added')

        context = {
            'book':book,
            'form':form,
            'comments':comments,
        }

        return render(request,'libri_im/book-detail.html' , context)

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



def wantToReadPost(request):
    if request.method == "POST" and request.is_ajax:
        isbn = int(request.POST.get('isbn'))
        new_sirtar = Sirtar.objects.get(
            emri="Want to read", id_user=request.user)
        if isbn not in new_sirtar.books:
            new_sirtar.books.append(isbn)
            new_sirtar.save(update_fields=['books'])
            return HttpResponse('<p>Success book added</p>')
        else:
            new_sirtar.books.remove(isbn)
            new_sirtar.save(update_fields=['books'])
            return HttpResponse('<p>Removed book from want to read</p>')

        return HttpResponse('<p>Error</p>')


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getdataWtr(request):
    if request.method == 'GET' and request.is_ajax:
        wtrCount = Sirtar.objects.get(
            emri="Want to read", id_user=request.user)
        serializer = SirtarSerializer(wtrCount, many=False)
    return Response(serializer.data)
