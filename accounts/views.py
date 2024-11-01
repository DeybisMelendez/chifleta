from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from posts.models import Post
from .models import Profile, Follow


def is_valid_name(str):
    return len(str) >= 3 or len(str) <= 50


# Create your views here.
def register(request):

    User = get_user_model()

    if request.user.is_authenticated:
        return redirect("feed")

    if request.method == "POST":
        username = request.POST.get("username", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        password = request.POST.get("password1", "")
        confirm_password = request.POST.get("password2", "")
        context = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password1": password,
            "password2": confirm_password,
        }

        if len(username) < 6:
            context["error"] = "Escriba un minimo de 6 caracteres para el usuario."
            return render(request, "register.html", context, status=400)
        if not is_valid_name(first_name):
            context["error"] = "Escriba un nombre en un rango de 3 a 50 caracteres."
            return render(request, "register.html", context, status=400)
        if not is_valid_name(last_name):
            context["error"] = "Escriba un apellido en un rango de 3 a 50 caracteres."
            return render(request, "register.html", context, status=400)
        if User.objects.filter(username=username).exists():
            context["error"] = "Usuario ya existe, eliga otro usuario."
            return render(request, "register.html", context, status=400)
        if password != confirm_password:
            context["error"] = "La contraseña no es la misma, vuelva a intentarlo."
            return render(request, "register.html", context, status=400)
        if len(password) < 8:
            context["error"] = "La contraseña debe tener minimo 8 caracteres."
            return render(request, "register.html", context, status=400)

        user = User.objects.create_user(username=username,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name,)
        profile = Profile.objects.create(user=user)
        profile.save()

        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect("user", user.username)

    return render(request, "register.html")


def user(request, username):
    user = User.objects.filter(username=username)
    if not user.exists():
        return render(request, "404.html", status=404)
    user = list(user)[0]
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(profile=profile).order_by("-created_at")
    
    follow_status = False
    
    my_user = request.user
    my_profile = Profile.objects.get(user=my_user)
    
    follow = Follow.objects.filter(follower = my_profile, followed = profile)
    
    if follow.exists():
        follow_status = True
    
    context = {
        "profile": profile,
        "user": user,
        "posts": posts,
        "follow_status": follow_status
    }

    return render(request, "user.html", context)


def log_in(request):
    if request.user.is_authenticated:
        return redirect("feed")
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        context = {
            "username": username,
            "password": password
        }
        if user is None:
            context["error"] = "El usuario y/o la contraseña es incorrecta."
            return render(request, "login.html", context, status=400)
        login(request, user)
        return redirect("feed")
    return render(request, "login.html")


@login_required(redirect_field_name="log_in")
@require_http_methods(["GET"])
def log_out(request):
    logout(request)
    return redirect("log_in")


@login_required(redirect_field_name="log_in")
@require_http_methods(["POST"])
def delete_user(request):
    request.user.delete()
    return redirect("login")


@login_required(redirect_field_name="user")
@require_http_methods(["POST"])
def update_user(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    first_name = request.POST.get("first_name", "")
    last_name = request.POST.get("last_name", "")
    bio = request.POST.get("bio", "")
    context = {
        "user": user,
        "profile": profile
    }
    if not is_valid_name(first_name):
        context["update_error"] = "Escriba un nombre en un rango de 3 a 50 caracteres."
        return render(request, "user.html", context, status=400)
    if not is_valid_name(last_name):
        context["update_error"] = "Escriba un apellido en un rango de 3 a 50 caracteres."
        return render(request, "user.html", context, status=400)
    if len(bio) > 160:
        context["update_error"] = "Escriba una bio menor de 160 caracteres."
        return render(request, "user.html", context, status=400)

    user.first_name = first_name
    user.last_name = last_name
    profile.bio = bio

    user.save()
    profile.save()

    return redirect("user", user.username)


@login_required(redirect_field_name="log_in")
def follow_profile(request, username):
    user = User.objects.filter(username = username)
    if not user.exists():
        return redirect("user", user.username)
    profile = Profile.objects.get(user=user)
    follow_status = False
    
    my_user = request.user
    my_profile = Profile.objects.get(user=my_user)
    
    follow = Follow.objects.filter(follower = my_profile, followed = profile)
    
    if follow.exists():
        follow.delete()
    else:
        follow = Follow.objects.create(follower =my_profile,followed = profile)
        follow.save()
        follow_status = True
    
    context={
        "profile": profile,
        "follow_status": follow_status
    }
    return render(request,"htmx/follow_status.html",context)