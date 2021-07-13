from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
# Books Model
class Book(models.Model):
    id_libri = models.AutoField(primary_key=True)
    isbn = models.BigIntegerField()
    titulli = models.CharField(max_length=2000)#char
    autori = models.CharField(max_length=2000) #char
    kategoria = models.CharField(max_length=2000)#char
    pershkrimi = models.TextField()#char
    mes_vleresimit = models.DecimalField(max_digits=5, decimal_places=2)#double
    nr_vleresimit = models.IntegerField()#int
    nr_faqeve = models.IntegerField()#int
    viti_publikimit = models.IntegerField() #int
    image_link = models.CharField(max_length=500, default="https://www.directtextbook.com/medium/.jpg")

    def __str__(self):
        return self.titulli
    def get_absolute_url(self):
       return reverse('libri_im:book_detail', kwargs={'pk': self.pk})


#AccountManager Model
class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Users must have an email adress.")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user


          
# User Model based on AbsctractBaseUser
def get_profile_image_filepath(self, filename):
    return f'profile_images/{str(self.pk)}/{"profile_image.png"}'

def get_default_profile_image():
    return "profile_images/profile_image.png"
class NewUser(AbstractBaseUser):
    #User profile fields
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    # field for books that are connected to the user
    read=ArrayField(models.IntegerField(),blank=True, null=True, default=list)
    want_to_read=ArrayField(models.IntegerField(),blank=True, null=True, default=list)
    reading=ArrayField(models.IntegerField(),blank=True, null=True, default=list)

    profileImg = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)

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



class Progress(models.Model):
    id_libri = models.ForeignKey(Book, on_delete=models.CASCADE)
    id_user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    pages_now = models.IntegerField(default=0)
    def __str__(self):
            return self.id_user.username+" Progress"

class Sirtar(models.Model):
    id = models.AutoField(primary_key=True)
    emri = models.CharField(max_length = 200, null= False, blank = False)
    id_user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    books = ArrayField(models.BigIntegerField(),blank=True, null=True, default=list)
    is_public = models.BooleanField(null = False, blank = False, default = True)
    can_delete = models.BooleanField(null = False, blank = False, default = False)

    def __str__(self):
            return self.id_user.username+" "+ self.emri
