from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User

def index(request):
  return redirect('/content')

def signup(request):
  if request.method == 'POST':
    username = request.POST["username"]
    password = request.POST["password"]
    first_name = request.POST["first_name"]

    if User.objects.filter(username=username).count() > 0:
      return render(request, 'app/signup.html', {'username_duplicate': True})

    if User.objects.filter(first_name=first_name).count() > 0:
      return render(request, 'app/signup.html', {'first_name_duplicate': True})

    user = User.objects.create_user(username=username, password=password, first_name=first_name)
    user.save()

    return render(request, 'app/signin.html', {})
  else:
    return render(request, 'app/signup.html', {})

def signin(request):
  if request.method == 'POST':
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('/content')
    else:
      return render(request, 'app/signin.html', {'passwordFail': True})
  else:
    return render(request, 'app/signin.html', {})

def logout(request):
  django_logout(request)
  return redirect('/content')
