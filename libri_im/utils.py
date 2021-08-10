from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from .models import NewUser, Sirtar, Progress, Book, FriendRequest
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render, redirect
from .serializers import  SirtarSerializer
from rest_framework.response import Response

'''This class generates tokens to send you specific tokens in every email for account activation'''
class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()
'''This function creates three different sirtars for each user that is signs up in webpage.'''
def create_default_sirtar(email):
    user1 = NewUser.objects.get(email = email)
    duke_lexuar = Sirtar.objects.create(emri="Reading",
                                         id_user = user1).save()
    kam_lexuar = Sirtar.objects.create(emri="Read",
                                         id_user = user1).save()
    do_te_lexoj = Sirtar.objects.create(emri="Want to read",
                                         id_user = user1).save()


'''This function makes sure that the user has the 3 default Sirtars and it will sync the Reading Sirtar with Progress table'''
def update_progress_db(emri,email):   
    user = NewUser.objects.get(email = email)
  
    '''If there are no default Sirtars create them for the current user'''
    if not Sirtar.objects.get(emri=emri,id_user=user):
        create_default_sirtar(user)
    currentReading = Sirtar.objects.get(emri=emri,id_user=user).books
    userProgress = Progress.objects.filter(id_user=user)
    currentProgress = []
    '''Fills the empty array with isbn-s from the current progress data'''
    for progress in userProgress:
        currentProgress.append(progress.id_libri.isbn)
    '''Check if there are new books in reading sirtar that need to be added in Progress'''
    for book in currentReading:
        if book not in currentProgress:
            Progress.objects.create(id_libri=Book.objects.get(isbn=book),id_user=user,pages_now=0)
    '''Check if there are deleted books in reading sirtar that need to be deleted in Progress'''
    for progress in currentProgress:
            if progress not in currentReading:
                Progress.objects.get(id_libri=Book.objects.get(isbn=progress),id_user=user).delete()

'''This function is used to send emails for account activation. Takes user, domain, token that is 
generated from the function that is declared in the beggining of this page and sends the link in 
users email'''
def send_email_activation(request,user):
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
                
'''This function is used to add a book in any of the default Sirtars("Want to read", "Reading", "Read") and it removes the same book
if it exists within the other default sirtars'''
def add_to_sirtar(emri, isbn, request):
    readSirtar = Sirtar.objects.get(emri='Read', id_user=request.user)
    readingSirtar = Sirtar.objects.get(emri='Reading', id_user=request.user)
    wtrSirtar = Sirtar.objects.get(emri='Want to read', id_user=request.user)
    requestSirtar = Sirtar.objects.get(emri=emri, id_user=request.user)                 #[1,2,3]  []    [2] 
    '''Add or remove isbn from requestSirtar'''
    if isbn not in requestSirtar.books:
        requestSirtar.books.append(isbn)
        requestSirtar.save(update_fields=['books'])   
    else:
        requestSirtar.books.remove(isbn)
        requestSirtar.save(update_fields=['books'])    
    '''Remove isbn from other sirtars'''
    if emri == "Read":
        if isbn in readingSirtar.books:
            readingSirtar.books.remove(isbn)
            readingSirtar.save(update_fields=['books'])
        if isbn in wtrSirtar.books:
            wtrSirtar.books.remove(isbn)
            wtrSirtar.save(update_fields=['books'])
    elif emri == "Reading":
        if isbn in readSirtar.books:
            readSirtar.books.remove(isbn)
            readSirtar.save(update_fields=['books'])
        if isbn in wtrSirtar.books:
            wtrSirtar.books.remove(isbn)
            wtrSirtar.save(update_fields=['books'])
    elif emri == "Want to read":
        if isbn in readSirtar.books:
            readSirtar.books.remove(isbn)
            readSirtar.save(update_fields=['books'])
        if isbn in readingSirtar.books:
            readingSirtar.books.remove(isbn)
            readingSirtar.save(update_fields=['books'])



def get_data_function(request, emri):
    sirtari = Sirtar.objects.get(emri=emri, id_user=request.user).books
    clickedIsbn = int(request.GET.get('isbn'))
    '''The added variable is used to determine the state of the book and change
    how it is displayed in the front-end'''
    added = None
    if clickedIsbn in sirtari:
        added = True
    else:
        added = False
    '''the needed variables'''
    wtrCount = Sirtar.objects.get(emri="Want to read", id_user=request.user)
    readCount = Sirtar.objects.get(emri="Read", id_user=request.user)
    readingCount = Sirtar.objects.get(emri="Reading", id_user=request.user)
    wtrSerialize = SirtarSerializer(wtrCount, many=False)
    readSerialize = SirtarSerializer(readCount, many=False)
    readingSerialize = SirtarSerializer(readingCount, many=False)

    data = {
        'added': added,                             #The state of the book
        'wtrCount': wtrSerialize.data,              #The number of Want to read books
        'readCount': readSerialize.data,            #The number of Read books
        'readingCount': readingSerialize.data,      #The number of Reading books
    }
    return Response(data)

def get_friend_request_or_false(sender,receiver):
    try:
        return FriendRequest.objects.get(sender=sender,receiver=receiver,is_active=True)
    except FriendRequest.DoesNotExist:
        return False

