from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from posts.models import Post

from .models import Follow, Profile
from .validations import is_valid_register_form, is_valid_update_form, is_valid_login_form

User = get_user_model()


def register(request):
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

        if not is_valid_register_form(request, username, first_name, last_name, password, confirm_password):
            return render(request, "register.html", context, status=400)

        user = User.objects.create_user(
            username=username, password=password, first_name=first_name, last_name=last_name)
        Profile.objects.create(user=user)
        login(request, user)
        return redirect("user", user.username)

    return render(request, "register.html")


def user(request, username):
    user = User.objects.filter(username=username).first()
    if not user:
        return render(request, "404.html", status=404)

    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(profile=profile).order_by("-created_at")
    follow_status = Follow.objects.filter(
        follower=request.user.profile, followed=profile).exists()

    context = {
        "profile": profile,
        "user": user,
        "posts": posts,
        "follow_status": follow_status,
    }

    return render(request, "user.html", context)


def log_in(request):
    if request.user.is_authenticated:
        return redirect("feed")

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)

        if not is_valid_login_form(request,user):
            context = {"username": username}
            return render(request, "login.html", context, status=400)

        login(request, user)
        return redirect("feed")

    return render(request, "login.html")


@login_required
@require_http_methods(["GET"])
def log_out(request):
    logout(request)
    return redirect("log_in")


@login_required
@require_http_methods(["POST"])
def delete_user(request):
    request.user.delete()
    return redirect("login")


@login_required
@require_http_methods(["POST"])
def update_user(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    first_name = request.POST.get("first_name", "")
    last_name = request.POST.get("last_name", "")
    bio = request.POST.get("bio", "")

    if not is_valid_update_form(request,first_name,last_name,bio):
        return render(request, "user.html", {"user": user, "profile": profile}, status=400)

    user.first_name, user.last_name = first_name, last_name
    profile.bio = bio
    user.save()
    profile.save()

    return redirect("user", user.username)


@login_required
def follow(request, username):

    target_profile = Profile.objects.get(user__username=username)
    my_profile = Profile.objects.get(user=request.user)
    
    follow_status = Follow.objects.filter(follower=my_profile,followed=target_profile).exists()
    
    if request.method == "POST":
        follow_status = my_profile.toggle_follow(target_profile)
    
    context = {
        "follow_status": follow_status,
        "username": username
    }
    
    return render(request, "htmx/follow_status.html", context)

def list_followers(request, username):
    profile = Profile.objects.filter(user__username=username)
    if not profile.exists():
        return redirect("feed")
    profile = profile.first()
    followers = Follow.objects.filter(followed=profile)
    following = Follow.objects.filter(follower=profile)

    context = {
        "followers": followers,
        "following": following
    }

    return render(request, "followers.html", context)


"""def list_following(request, username):
    profile = Profile.objects.filter(user__username=username)
    if not profile.exists():
        return redirect("feed")
    profile = profile.first()
    following = Follow.objects.filter(follower=profile)

    context = {
        "following": following
    }
    return render(request, "followers.html", context)"""