from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from accounts.models import Follow, Profile

from .models import Post


@login_required(redirect_field_name="log_in")
def feed(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    followed_ids = Follow.objects.filter(
        follower=profile).values_list("followed_id", flat=True)

    posts = Post.objects.filter(Q(profile_id__in=followed_ids) | Q(
        profile=profile) & Q(parent__isnull=True)).order_by("-created_at")

    context = {
        "posts": posts
    }
    return render(request, "feed.html", context)


def post_view(request, id):
    post = Post.objects.get(pk=id)
    comments = Post.objects.filter(parent=post.id)

    parents = Post.objects.none()
    parent = post.parent

    while parent is not None:
        parents |= Post.objects.filter(pk=parent.pk)
        parent = parent.parent

    context = {
        "post": post,
        "comments": comments,
        "parents": parents
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
    if request.method == "POST":
        parent = Post.objects.get(pk=pk)
        content = request.POST.get("content", "")
        post = Post.objects.create(
            profile=profile, content=content, parent=parent)
        post.save()
        return redirect("feed")

    post = Post.objects.filter(pk=pk)
    if not post.exists():
        return redirect("feed")

    post = post.first()
    context = {
        "post": post
    }
    return render(request, "htmx/post_comment.html", context)


@login_required(redirect_field_name="log_in")
def post_share(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        share = Post.objects.get(pk=pk)
        content = request.POST.get("content", "")
        post = Post.objects.create(
            profile=profile, content=content, share=share)
        post.save()
        return redirect("feed")

    post = Post.objects.filter(pk=pk)
    if not post.exists():
        return redirect("feed")

    post = post.first()

    context = {
        "post": post,
    }

    return render(request, "htmx/post_share.html", context)


def list_followers(request, username):
    user = User.objects.filter(username=username).first()
    profile = Profile.objects.get(user=user)
    # TODO anadir validaciones de errores
    followers = Follow.objects.filter(followed=profile)

    context = {
        "followers": followers
    }

    return render(request, "followers.html", context)


def list_following(request, username):
    user = User.objects.filter(username=username).first()
    profile = Profile.objects.get(user=user)

    following = Follow.objects.filter(follower=profile)

    context = {
        "following": following
    }
    return render(request, "followers.html", context)
