from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Books Model
class Book(models.Model):
    id_libri = models.AutoField(primary_key=True)
    isbn = models.IntegerField()
    titulli = models.CharField(max_length=500)#char
    autori = models.CharField(max_length=100) #char
    kategoria = models.CharField(max_length=100)#char
    pershkrimi = models.TextField()#char
    mes_vleresimit = models.DecimalField(max_digits=5, decimal_places=2)#double
    nr_vleresimit = models.IntegerField()#int
    nr_faqeve = models.IntegerField()#int
    viti_publikimit = models.IntegerField() #int

    def __str__(self):
        return self.titulli


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
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user
        
def get_profile_image_path(self,filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_default_profile_image():
    return "foto.png"


          
# User Model based on AbsctractBaseUser
class NewUser(AbstractBaseUser):
    #User profile fields
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(verbose_name="Date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_path, null=True, blank=True, default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)
    # field for books that are connected to the user
    read=ArrayField(models.IntegerField(null=True),null=True)
    want_to_read=ArrayField(models.IntegerField(null=True),null=True)
    reading=ArrayField(models.IntegerField(null=True),null=True)

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