from libri_im.models import NewUser



def users_to_base(request):    
    try:
        myuser = NewUser.objects.get(id=request.user.id).profileImg.url
    except NewUser.DoesNotExist:
        myuser = ""
    return {'myuser': myuser }