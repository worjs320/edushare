from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from urllib.parse import urlparse, parse_qs
from django.core import serializers
import json
from .models import Content
from .models import Note
import re

def content_list(request):
  contents = Content.objects
  return render(request, 'content/content_list.html', {'contents': contents})

def content_add(request):
  if request.method == 'POST':
    content = Content()
    if request.user.is_authenticated:
      content.user_id = User.objects.get(username=request.user.username)
      content.user_name = User.objects.get(username=request.user.username).first_name
    content.title = request.POST['title']
    description = request.POST['description']

    hour_pattern = re.findall('\[[1-9]:[0-5][0-9]:[0-5][0-9]\]', description)
    for pattern in hour_pattern:
	    description = description.replace(pattern, '<a class="time-move-btn cursor-pointer">' + pattern.strip("[""]") + '</a>')

    minute_pattern_one = re.findall('\[[0-9]:[0-5][0-9]\]', description)
    for pattern in minute_pattern_one:
	    description = description.replace(pattern, '<a class="time-move-btn cursor-pointer">' + pattern.strip("[""]") + '</a>')
		
    minute_pattern_two = re.findall('\[[0-5][0-9]:[0-5][0-9]\]', description)
    for pattern in minute_pattern_two:
	    description = description.replace(pattern, '<a class="time-move-btn cursor-pointer">' + pattern.strip("[""]") + '</a>')

    content.description = description
    content.view_count = 0
    content.like_count = 0
    
    youtube_link = request.POST['youtube_link']
    parsed_youtube_link = urlparse(youtube_link)
    content.youtube_id = parse_qs(parsed_youtube_link.query)['v'][0]
    
    content.save()

    return redirect('/content')
  else:
    return render(request, 'content/content_add.html', {})

def content_info(request, content_pk):
    content = Content.objects.get(pk=content_pk)
    notes = Note.objects.filter(content=content_pk)
    content.view_count += 1
    content.save()
    return render(request, 'content/content_info.html', {'content': content, 'notes': notes})

def note_add(request, content_pk):
  if request.method == 'POST':
    note = Note()
    content = Content.objects.get(pk=content_pk)
    request_data = json.loads(request.body)

    note.title = request_data["title"]
    description = request_data['description']

    hour_pattern = re.findall('\[[1-9]:[0-5][0-9]:[0-5][0-9]\]', description)
    for pattern in hour_pattern:
	    description = description.replace(pattern, '<a class="time-move-btn cursor-pointer">' + pattern.strip("[""]") + '</a>')

    minute_pattern_one = re.findall('\[[0-9]:[0-5][0-9]\]', description)
    for pattern in minute_pattern_one:
	    description = description.replace(pattern, '<a class="time-move-btn cursor-pointer">' + pattern.strip("[""]") + '</a>')
		
    minute_pattern_two = re.findall('\[[0-5][0-9]:[0-5][0-9]\]', description)
    for pattern in minute_pattern_two:
	    description = description.replace(pattern, '<a class="time-move-btn cursor-pointer">' + pattern.strip("[""]") + '</a>')

    note.description = description
    note.content = content

    if request.user.is_authenticated:
      note.user_id = User.objects.get(username=request.user.username)
      note.user_name = User.objects.get(username=request.user.username).first_name

    note.save()

    return JsonResponse({"result":"success"})

def note_list(content_pk):
  notes = Note.objects.filter(content=content_pk)
  notes = serializers.serialize('json', notes)
  return HttpResponse(notes, content_type="application/json")

def like(request, content_pk):
  content = Content.objects.get(pk=content_pk) 
  
  if not request.user.is_authenticated:
      message = "로그인을 해주세요"
      context = {'like_count' : content.like.count(), "message": message}
      return HttpResponse(json.dumps(context), content_type='application/json')

  user = request.user
  
  if content.like.filter(id = user.id).exists():
      content.like.remove(user)
      action = "like_cancle"
  else:
      content.like.add(user)
      action = "like" 

  context = {"result": "success", "action": action, "like_count" : content.like.count()}
  return HttpResponse(json.dumps(context), content_type='application/json') 