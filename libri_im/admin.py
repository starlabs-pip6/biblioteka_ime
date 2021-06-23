from django.contrib import admin
from libri_im.models import NewUser,Book
# Register your models here.
admin.site.register(Book)
admin.site.register(NewUser)
