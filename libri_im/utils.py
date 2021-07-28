from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from .models import NewUser, Sirtar, Progress, Book
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render, redirect

class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()

def create_default_sirtar(email):
    user1 = NewUser.objects.get(email = email)
    duke_lexuar = Sirtar.objects.create(emri="Reading",
                                         id_user = user1).save()
    kam_lexuar = Sirtar.objects.create(emri="Read",
                                         id_user = user1).save()
    do_te_lexoj = Sirtar.objects.create(emri="Want to read",
                                         id_user = user1).save()

def update_progress_db(emri,email):
    user = NewUser.objects.get(email = email)
  
    if not Sirtar.objects.get(emri=emri,id_user=user):
        create_default_sirtar(user)
    currentReading = Sirtar.objects.get(emri=emri,id_user=user).books
    userProgress = Progress.objects.filter(id_user=user)
    currentProgress = []
    for progress in userProgress:
        currentProgress.append(progress.id_libri.isbn)
    #Check if there are new books in reading sirtar that need to be added in Progress
    for book in currentReading:
        if book not in currentProgress:
            Progress.objects.create(id_libri=Book.objects.get(isbn=book),id_user=user,pages_now=0)
    #Check if there are deleted books in reading sirtar that need to be deleted in Progress
    for progress in currentProgress:
            if progress not in currentReading:
                Progress.objects.get(id_libri=Book.objects.get(isbn=progress),id_user=user).delete()

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
                