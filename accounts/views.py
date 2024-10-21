from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.
def register(request):
    
    #TODO: VALIDAR QUE USERNAME NO EXISTA O NO ESTE REGISTRADO
    
    #TODO: VALIDAR QUE CONTRASE;A SEA IGUALES.
    User = get_user_model()
    error = ""
    if request.user.is_authenticated:
        return redirect("user",request.user.username)
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        password = request.POST.get('password1', '')
        
        
        if  not User.objects.filter(username = username).exists():
        
            user = User.objects.create_user(username = username,
                                            password = password,
                                            first_name = first_name,
                                            last_name = last_name,)
            profile = Profile.objects.create(user = user)
            profile.save()

            user = authenticate(username=username,password=password)    

            return redirect("user",user.username)
        error="El Usuario ya Existe"
    
    context = {
        "error":error
    }
    
    return render(request,"register.html", context=context)

def user(request,username):
    user = User.objects.get(username = username)
    profile = Profile.objects.get(user = user)
    
    context = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name" : user.last_name,
        "bio" : profile.bio,
        "avatar" : profile.avatar,
        "followers_count" : profile.followers_count,
        "following_count" : profile.following_count
        
    }
    
    return render(request,"user.html", context = context)

def login(request):
    
    return render(request, )
