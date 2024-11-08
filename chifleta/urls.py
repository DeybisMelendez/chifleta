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

from accounts.views import (delete_user, follow_profile, log_in, log_out,
                            register, update_user, user)
from notifications.views import (check_all_notification, check_notification,
                                notification,notifications_button)
from posts.views import (add_post, delete_post, feed, list_followers,
                        list_following, post_comment, post_share, post_view)

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
    path("follow_profile/<str:username>/",
        follow_profile, name="follow_status"),
    path("followers/<str:username>/", list_followers, name="list_followers"),
    path("following/<str:username>/", list_following, name="list_following"),
    path("notifications/", notification, name="notifications"),
    path("check_notification/<int:pk>/", check_notification, name="check_notification"),
    path("check_all_notification/", check_all_notification, name="check_all_notification"),
    path("htmx/notification_button/", notifications_button, name="notifications_button")

]

# Servir archivos de media en modo depuración
# if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
