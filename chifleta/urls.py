"""
URL configuration for chifleta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import register, user, log_in, log_out, delete_user,update_user
from posts.views import feed, post_view, add_post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name="register"),
    path('user/<str:username>/', user, name="user"),
    path('login/', log_in, name="login"),
    path('logout/', log_out, name="logout"),
    path('delete_user', delete_user, name="delete_user"),
    path("update_user",update_user, name="update_user"),
    path("feed/",feed, name="feed"),
    path("post/<int:id>/",post_view, name="post"),
    path("add_post",add_post, name="add_post")
]

# Servir archivos de media en modo depuración
#if settings.DEBUG: 
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)