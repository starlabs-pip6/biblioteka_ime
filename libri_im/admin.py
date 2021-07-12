from django.contrib import admin
from libri_im.models import NewUser,Book, Progress, Sirtar
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class NewUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Book)
admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Progress)
admin.site.register(Sirtar)



