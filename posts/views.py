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
    # TODO: Optimizar cantidad de posts a enviar (NO ES URGENTE)
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
    #TODO: Guardar correctamente el comentario
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        parent = Post.objects.get(pk=pk)
        content = request.POST.get("content", "")
        post = Post.objects.create(profile=profile, content=content, parent=parent)
        post.save()
        print(post)
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
    #TODO: Guardar correctamente el share
    user = request.user
    profile = Profile.objects.get(user=user)
    
    if request.method == "POST":
        share = Post.objects.get(pk=pk)
        content = request.POST.get("content", "")
        post = Post.objects.create(profile=profile, content=content,share=share)
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
