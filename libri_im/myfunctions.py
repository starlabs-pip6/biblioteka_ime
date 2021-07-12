from .models import NewUser, Sirtar
def create_default_sirtar(email):
    user1 = NewUser.objects.get(email = email)
    duke_lexuar = Sirtar.objects.create(emri="Duke lexuar",
                                         id_user = user1).save()
    kam_lexuar = Sirtar.objects.create(emri="Kam lexuar",
                                         id_user = user1).save()
    do_te_lexoj = Sirtar.objects.create(emri="Dua ta lexoj",
                                         id_user = user1).save()