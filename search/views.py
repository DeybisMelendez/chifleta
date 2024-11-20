from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from accounts.models import Profile
from posts.models import Post


@require_http_methods(["POST"])
def search_all(request):

    search = request.POST.get("search", "").strip()

    if search:
        profiles = Profile.objects.filter(user__username__icontains=search)
        posts = Post.objects.filter(content__icontains=search)
    else:
        profiles = Profile.objects.none()
        posts = Post.objects.none()

    context = {
        "profiles": profiles,
        "posts": posts,
    }

    return render(request, "search.html", context)
