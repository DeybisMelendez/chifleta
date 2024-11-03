"""
URL configuration for chifleta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from accounts.views import (delete_user, log_in, log_out, register,
                            update_user, user, follow_profile)
from posts.views import add_post, feed, post_view, delete_post, post_comment, post_share

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", log_in, name="index"),
    path("register/", register, name="register"),
    path("user/<str:username>/", user, name="user"),
    path("login/", log_in, name="log_in"),
    path("logout/", log_out, name="log_out"),
    path("delete_user", delete_user, name="delete_user"),
    path("update_user", update_user, name="update_user"),
    path("feed/", feed, name="feed"),
    path("post/<int:id>/", post_view, name="post"),
    path("add_post", add_post, name="add_post"),
    path("delete_post/<int:pk>/", delete_post, name="delete_post"),
    path("post_comment/<int:pk>/", post_comment, name="post_comment"),
    path("post_share/<int:pk>/", post_share, name="post_share"),
    path("follow_profile/<str:username>/", follow_profile, name="follow_status")
]

# Servir archivos de media en modo depuración
# if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
