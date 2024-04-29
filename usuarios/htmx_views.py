from django.shortcuts import render
from django.contrib.auth.models import User

def check_user(request):
    username = request.GET.get('username')
    usernames = User.objects.filter(username=username)
    
    return render(request, 'partials/htmx_components/check_user.html', {'usernames': usernames})

def check_email(request):
    email = request.GET.get('email')
    emails = User.objects.filter(email=email)
    
    return render(request, 'partials/htmx_components/check_email.html', {'emails': emails})