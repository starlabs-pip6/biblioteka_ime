from .models import NewUser, Sirtar
def create_default_sirtar(email):
    user1 = NewUser.objects.get(email = email)
    duke_lexuar = Sirtar.objects.create(emri="Reading",
                                         id_user = user1).save()
    kam_lexuar = Sirtar.objects.create(emri="Read",
                                         id_user = user1).save()
    do_te_lexoj = Sirtar.objects.create(emri="Want to read",
                                         id_user = user1).save()