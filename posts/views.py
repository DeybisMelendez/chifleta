from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Profile, Follow
from .models import Post

# Create your views here.
@login_required(redirect_field_name="login")
def feed(request):
    
    user = request.user
    profile = Profile.objects.get(user = user)
    followeds = Follow.objects.filter(follower = profile)
    
    for followed in followeds:
        posts = Post.objects.filter(profile = followed)
    
    return