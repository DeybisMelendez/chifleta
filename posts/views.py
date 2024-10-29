from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Profile, Follow
from .models import Post
from django.views.decorators.http import require_http_methods

# Create your views here.
@login_required(redirect_field_name="login")
def feed(request):
    
    user = request.user
    profile = Profile.objects.get(user = user)
    followeds = Follow.objects.filter(follower = profile)
    #TODO: Optimizar cantidad de posts a enviar
    posts = 0
    for followed in followeds:
        if posts == 0:
            posts = Post.objects.filter(profile = followed.followed)
        else:
            posts |= Post.objects.filter(profile = followed.followed)
    print(posts)
    context={
        "posts": posts
    }
    return render(request,"feed.html", context)

def post_view(request,id):    
    post = Post.objects.get(pk = id)  
    context={
        "post": post
    }
    return render(request,"post.html",context)

@login_required(redirect_field_name="login")
@require_http_methods(["POST"])
def add_post(request):
    user = request.user
    profile =  Profile.objects.get(user = user)
    
    content = request.POST.get("content","")
    post = Post.objects.create(profile = profile, content = content)
    post.save()
    return redirect("feed")