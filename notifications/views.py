from django.shortcuts import render
from accounts.models import Profile

# Create your views here.
def notification(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    
    return