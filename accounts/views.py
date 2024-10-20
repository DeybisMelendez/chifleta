from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from .models import Profile

# Create your views here.
def register(request):
    User = get_user_model()

    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        password = request.POST.get('password1', '')
        
        user = User.objects.create_user(username = username,
                                        password = password,
                                        first_name = first_name,
                                        last_name = last_name,)
        profile = Profile.objects.create(user = user)
        profile.save()

        user = authenticate(username=username,password=password)    
        if user is not None:
            login(request,profile)
        return redirect("home")
    
    return render(request,"register.html")
