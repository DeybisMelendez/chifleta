from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from accounts.models import Follow, Profile

from .models import Post


@login_required(redirect_field_name="log_in")
def feed(request):

    user = request.user
    profile = Profile.objects.get(user=user)
    followeds = Follow.objects.filter(follower=profile)
    # TODO: Optimizar cantidad de posts a enviar
    posts = 0
    for followed in followeds:
        if posts == 0:
            posts = Post.objects.filter(profile=followed.followed)
        else:
            posts |= Post.objects.filter(profile=followed.followed)
    context = {
        "posts": posts
    }
    return render(request, "feed.html", context)


def post_view(request, id):
    post = Post.objects.get(pk=id)
    context = {
        "post": post
    }
    return render(request, "post.html", context)


@login_required(redirect_field_name="log_in")
@require_http_methods(["POST"])
def add_post(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    content = request.POST.get("content", "")
    post = Post.objects.create(profile=profile, content=content)
    post.save()
    return redirect("feed")
