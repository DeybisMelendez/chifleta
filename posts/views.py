from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from accounts.models import Follow, Profile

from .models import Post


@login_required(redirect_field_name="log_in")
def feed(request):

    user = request.user
    profile = Profile.objects.get(user=user)
    follows = Follow.objects.filter(follower=profile)
    # TODO: Optimizar cantidad de posts a enviar
    posts = 0
    for follow in follows:
        if posts == 0:
            posts = Post.objects.filter(profile=follow.followed)
        else:
            posts |= Post.objects.filter(profile=follow.followed)

    posts |= Post.objects.filter(profile=profile)
    posts = posts.order_by("-created_at")

    context = {
        "posts": posts
    }
    return render(request, "feed.html", context)


def post_view(request, id):
    post = Post.objects.get(pk=id)
    comments = Post.objects.filter(parent=post.id)
    context = {
        "post": post,
        "comments": comments,
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


@login_required(redirect_field_name="log_in")
def delete_post(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    post = Post.objects.get(pk=pk)
    if post.profile == profile:
        post.delete()
        return redirect("user", user.username)
    return redirect("feed")


@login_required(redirect_field_name="log_in")
def post_comment(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)

    content = request.POST.get("content", "")
    post = Post.objects.create(profile=profile, content=content)
    post.parent = pk
    post.save()
    return redirect("feed")


@login_required(redirect_field_name="log_in")
def post_share(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)

    content = request.POST.get("content", "")
    post = Post.objects.create(profile=profile, content=content)
    post.share = pk
    post.save()
    return redirect("feed")
