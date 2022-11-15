from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def signup(request):
  pass

def signin(request):
  if request.method == 'POST':
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('/content')
    else:
      return redirect('/signin?passwordFail=True')
  else:
    return render(request, 'app/signin.html', {})

def logout(request):
  pass