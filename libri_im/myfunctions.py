from .models import NewUser, Sirtar, Progress, Book
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
