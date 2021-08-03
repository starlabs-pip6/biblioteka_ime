from django.contrib import admin
from libri_im.models import Followers, NewUser,Book, Progress, Sirtar, Comment
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class NewUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class NewProgressAdmin(UserAdmin):
    list_display = ('id_libri','id_user', 'pages_now')
    #search_fields = ('id_libri', 'id_perdoruesi')
    # readonly_fields = ('id')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('id_user','id_libri')

admin.site.register(Book)
admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Progress, NewProgressAdmin)
admin.site.register(Sirtar)
admin.site.register(Comment)
admin.site.register(Followers)


