from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model,login, logout, authenticate
from django.contrib.auth.models import User
from .models import Profile
import asyncio
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

def is_valid_name(str):
    return len(str) >= 3 or len(str) <= 50


# Create your views here.
def register(request):
    
    User = get_user_model()

    if request.user.is_authenticated:
        return redirect("user",request.user.username)
    
    if request.method == "POST":
        username = request.POST.get("username", "") 
        first_name = request.POST.get("first_name","")
        last_name = request.POST.get("last_name","")
        password = request.POST.get("password1", "")
        confirm_password = request.POST.get("password2", "")
        if len(username) < 6:
            context={
                "error":"Escriba un minimo de 6 caracteres para el usuario."
            }
            return render(request,"register.html",context)
        if not is_valid_name(first_name):
            context={
                "error":"Escriba un nombre en un rango de 3 a 50 caracteres."
            }
            return render(request,"register.html",context)
        if not is_valid_name(last_name):
            context={
                "error":"Escriba un apellido en un rango de 3 a 50 caracteres."
            }
            return render(request,"register.html",context)
        if User.objects.filter(username = username).exists():
            context={
                "error":"Usuario ya existe, eliga otro usuario."
            }
            return render(request,"register.html",context)
        if password != confirm_password:
            context={
                "error":"La contraseña no es la misma, vuelva a intentarlo."
            }
            return render(request,"register.html",context )
        if len(password) < 8:
            context={
                "error":"La contraseña debe tener minimo 8 caracteres."
            }
            return render(request,"register.html",context )
        
        user = User.objects.create_user(username = username,
                                        password = password,
                                        first_name = first_name,
                                        last_name = last_name,)
        profile = Profile.objects.create(user = user)
        profile.save()

        user = authenticate(username=username,password=password)    

        return redirect("user",user.username)
    
    return render(request,"register.html")

def user(request,username):
    user = User.objects.filter(username = username)
    if not user.exists():
        return render(request,"404.html", status=404)
    user = list(user)[0]
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
    
    return render(request,"user.html", context)

def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is None:
            context={
                "error":"El usuario y/o la contraseña es incorrecta."
            }
            return render(request,"login.html", context)
        login(request,user)
        return redirect("user",user.username)
    return render(request,"login.html" )


@login_required(redirect_field_name="login")
@require_http_methods(["POST"])
def log_out(request):
    
    logout(request)
    
    return redirect("login")

@login_required(redirect_field_name="login")
@require_http_methods(["POST"])
def delete_user(request):
    request.user.delete()
    return redirect("login")

@login_required(redirect_field_name="user")
@require_http_methods(["POST"])
def update_user(request):
    user = request.user
    profile =  Profile.objects.get(user = user)
    first_name = request.POST.get("first_name","")
    last_name = request.POST.get("last_name","")
    bio = request.POST.get("bio","")
    context={
        "username": user.username,
        "first_name": user.first_name,
        "last_name" : user.last_name,
        "bio" : profile.bio,
        "avatar" : profile.avatar,
        "followers_count" : profile.followers_count,
        "following_count" : profile.following_count
    }
    if not is_valid_name(first_name):
        context["update_error"] = "Escriba un nombre en un rango de 3 a 50 caracteres."
        return render(request,"user.html", context)
    if not is_valid_name(last_name):
        context["update_error"] = "Escriba un apellido en un rango de 3 a 50 caracteres."
        return render(request,"user.html", context)
    if len(bio) > 160:
        context["update_error"] = "Escriba una bio menor de 160 caracteres."
        return render(request,"user.html", context)
    
    user.first_name = first_name
    user.last_name = last_name
    profile.bio = bio
    
    user.save()
    profile.save()
    
    return redirect("user",user.username)
