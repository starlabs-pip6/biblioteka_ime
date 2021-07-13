from .models import NewUser, Sirtar, Progress, Book
def create_default_sirtar(email):
    user1 = NewUser.objects.get(email = email)
    duke_lexuar = Sirtar.objects.create(emri="Reading",
                                         id_user = user1).save()
    kam_lexuar = Sirtar.objects.create(emri="Read",
                                         id_user = user1).save()
    do_te_lexoj = Sirtar.objects.create(emri="Want to read",
                                         id_user = user1).save()

# def update_progress_from_dl(user):
#     Progress.objects.filter(id_user = user).delete()
#     if Sirtar.objects.filter(emri="Duke lexuar", id_user = user).exists():
#         dlBooks = Sirtar.objects.filter(emri="Duke lexuar", id_user = user).books
#         for idBook in dlBooks:  
#             Progress.objects.create(id_libri=Book.objects.get(isbn=idBook),id_user=user)