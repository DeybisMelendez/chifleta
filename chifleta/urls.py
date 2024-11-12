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
from django.contrib import admin
from django.urls import path

from accounts.views import (delete_user, follow, log_in, log_out,
                            register, update_user, user, list_followers,
                        list_following, )
from notifications.views import (check_all_notification, check_notification,
                                notifications,notifications_button)
from posts.views import (add_post, delete_post, feed,post_comment, post_share, post_view)
from search.views import search_all

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("", log_in, name="index"),
    path("login/", log_in, name="log_in"),
    path("register/", register, name="register"),
    path("user/<str:username>/", user, name="user"),
    path("user/<str:username>/follow/",follow, name="follow_status"),
    path("user/<str:username>/followers/", list_followers, name="list_followers"),
    path("user/<str:username>/following/", list_following, name="list_following"),
    path("user/logout", log_out, name="log_out"),
    path("user/delete", delete_user, name="delete_user"),
    path("user/update", update_user, name="update_user"),
    
    path("feed/", feed, name="feed"),
    path("post/add_post", add_post, name="add_post"),
    path("post/<int:id>/", post_view, name="post"),
    path("post/<int:pk>/delete", delete_post, name="delete_post"),
    path("post/<int:pk>/comment", post_comment, name="post_comment"),
    path("post/<int:pk>/share", post_share, name="post_share"),
    
    path("notifications/", notifications, name="notifications"),
    path("notifications/<int:pk>/", check_notification, name="check_notification"),
    path("notifications/check_all", check_all_notification, name="check_all_notification"),
    
    path("htmx/notification_button", notifications_button, name="notifications_button"),
    path("search", search_all, name="search")

]

# Servir archivos de media en modo depuración
# if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
