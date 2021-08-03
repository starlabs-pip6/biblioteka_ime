from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse


# Books Model


class Book(models.Model):
    id_libri = models.AutoField(primary_key=True)
    isbn = models.BigIntegerField()
    titulli = models.CharField(max_length=2000)  # char
    autori = models.CharField(max_length=2000)  # char
    kategoria = ArrayField(models.CharField(max_length=2000),blank=True,null=True, default=list)  # ArrayField(char)
    pershkrimi = models.TextField()  # char
    mes_vleresimit = models.DecimalField(
        max_digits=5, decimal_places=2)  # double
    nr_vleresimit = models.IntegerField()  # int
    nr_faqeve = models.IntegerField()  # int
    viti_publikimit = models.IntegerField()  # int
    image_link = models.CharField(
        max_length=500, default="https://www.directtextbook.com/medium/.jpg")

    def __str__(self):
        return self.titulli

    def get_absolute_url(self):
        return reverse('libri_im:book_detail', kwargs={'pk': self.pk})


# AccountManager Model
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email adress.")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        duke_lexuar = Sirtar.objects.create(emri="Reading",
                                            id_user=user).save()
        kam_lexuar = Sirtar.objects.create(emri="Read",
                                           id_user=user).save()
        do_te_lexoj = Sirtar.objects.create(emri="Want to read",
                                            id_user=user).save()
        return user


# User Model based on AbsctractBaseUser
def get_profile_image_filepath(self, filename):
    return f'profile_images/{str(self.pk)}/{"profile_image.png"}'


def get_default_profile_image():
    return "profile_images/profile_image.png"


class NewUser(AbstractBaseUser):
    # User profile fields
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    first_login = models.BooleanField(default=True)
    fav_categories= ArrayField(models.CharField(max_length=100),blank=True, null=True, default=list)
    # field for books that are connected to the user
    #currently_reading = models.BigIntegerField(null=True, blank=True)

    profileImg = models.ImageField(max_length=255, upload_to=get_profile_image_filepath,
                                   null=True, blank=True, default=get_default_profile_image)
    friend_list = ArrayField(models.IntegerField(),blank=True, null=True, default=list)

    objects = MyAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    def dateJoined(self):
        return self.date_joined.strftime('%B %Y')

class Followers(models.Model):
    followers = models.ManyToManyField(NewUser, blank=True, related_name='followers')
    following = models.ManyToManyField(NewUser, blank=True, related_name='following')
    follow_requests=models.ManyToManyField(NewUser, blank=True, related_name='follow_requests')
    
class Progress(models.Model):
    id_libri = models.ForeignKey(Book, on_delete=models.CASCADE)
    id_user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    pages_now = models.IntegerField(default=0)

    def __str__(self):
        return self.id_user.username+" Progress"


class Sirtar(models.Model):
    emri = models.CharField(max_length=200, null=False, blank=False)
    id_user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    books = ArrayField(models.BigIntegerField(),
                       blank=True, null=True, default=list)
    is_public = models.BooleanField(null=False, blank=False, default=True)
    can_delete = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
            return self.id_user.username + " " + self.emri

class Comment(models.Model):
    book = models.ForeignKey(Book,related_name="comments", on_delete=models.CASCADE)
    name = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(NewUser,blank=True,related_name="comment_likes")
    dislikes = models.ManyToManyField(NewUser,blank=True,related_name="comment_dislikes")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True,null=True,related_name='+')

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('date_added').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def __str__(self):
        return '%s - %s' % (self.book.titulli , self.name)
