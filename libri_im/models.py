from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class librat(models.Model):
    id_libri=models.AutoField(primary_key=True)
    isbn=models.IntegerField()
    titulli=models.CharField(max_length=500)#char
    autori=models.CharField(max_length=100) #char
    kategoria=models.CharField(max_length=100)#char
    pershkrimi=models.TextField()#char
    mes_vleresimit=models.DecimalField(max_digits=5, decimal_places=2)#double
    nr_vleresimit=models.IntegerField()#int
    nr_faqeve=models.IntegerField()#int
    viti_publikimit=models.IntegerField() #int

    def __str__(self):
        return self.titulli
class UserProfile(models.Model):
    #lidhja e userit me librat
    user=models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    lexova=ArrayField(models.IntegerField(),blank=True)
    do_ta_lexoj=ArrayField(models.IntegerField(),blank=True)
    duke_lexuar=ArrayField(models.IntegerField(),blank=True)
    def __str__(self):
        return self.user.username
