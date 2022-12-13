from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout as django_logout
from django.core import serializers
from django.db.models import Count
from django.contrib.auth.models import User
from content.models import Content
from content.models import Note

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

def mycontent(request):
  user = User.objects.get(username=request.user.username)
  contents = Content.objects.filter(user_id=user)
  return render(request, 'app/my-content.html', {'contents': contents})

def mynote(request):
  user = User.objects.get(username=request.user.username)
  notes = Note.objects.filter(user_id=user)

  return render(request, 'app/my-note.html', {'notes': notes })

def mylike(request):
  contents = Content.objects.filter(like=request.user)
  return render(request, 'app/my-like.html', {'contents': contents})

def mynote_list(request):
  user = User.objects.get(username=request.user.username)
  notes = Note.objects.filter(user_id=user)
  notes = serializers.serialize('json', notes)
  return HttpResponse(notes, content_type="application/json")

def rank(request):
  content_rank = Content.objects.all().values('user_name').annotate(count=Count('user_name')).order_by('-count')
  note_rank = Note.objects.all().values('user_name').annotate(count=Count('user_name')).order_by('-count')
  return render(request, 'app/rank.html', {'content_rank': content_rank, 'note_rank': note_rank})