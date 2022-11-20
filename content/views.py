from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import Content
from urllib.parse import urlparse, parse_qs

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
    content.description = request.POST['description']
    content.view_count = 0
    content.like_count = 0
    
    youtube_link = request.POST['youtube_link']
    parsed_youtube_link = urlparse(youtube_link)
    content.youtube_id = parse_qs(parsed_youtube_link.query)['v'][0]
    
    content.save()

    return redirect('/content')
  else:
    return render(request, 'content/content_add.html', {})

def content_info(request, pk):
    content = Content.objects.get(pk=pk)
    content.view_count += 1
    content.save()
    return render(request, 'content/content_info.html', {'content': content})