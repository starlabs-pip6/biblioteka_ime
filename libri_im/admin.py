from django.contrib import admin
from libri_im.models import NewUser,Book, Progress, Sirtar, Comment,FriendList,FriendRequest, Relation
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

class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendList

class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender' , 'receiver']
    list_display = ['sender' , 'receiver']
    search_fields = ['sender__username','sender__email','receiver__username','receiver__email']
    
    class Meta:
        model = FriendRequest


admin.site.register(Book)
admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Progress, NewProgressAdmin)
admin.site.register(Sirtar)
admin.site.register(Comment)
admin.site.register(FriendList,FriendListAdmin)
admin.site.register(FriendRequest,FriendRequestAdmin)
admin.site.register(Relation)


