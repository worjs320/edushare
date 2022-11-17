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
    
    youtube_link = request.POST['youtube_link']
    parsed_youtube_link = urlparse(youtube_link)
    
    content.youtube_link = youtube_link
    youtube_thumbnail = 'https://img.youtube.com/vi/' + parse_qs(parsed_youtube_link.query)['v'][0] + '/0.jpg'
    content.youtube_thumbnail = youtube_thumbnail
    content.view_count = 0
    content.like_count = 0

    content.save()

    # insert 후에는 꼭 redirect 처리!
    return redirect('/content')
  else:
    return render(request, 'content/content_add.html', {})