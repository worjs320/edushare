from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from urllib.parse import urlparse, parse_qs
from django.core import serializers
import json
from .models import Playlist
from .models import PlaylistNote
import re

def playlist_list(request):
  title = request.GET.get('title', None)
  if title == None:
    playlists = Playlist.objects
  else:
    playlists = Playlist.objects.filter(title__icontains=title)
  
  return render(request, 'playlist/playlist_list.html', {'playlists': playlists})

def playlist_add(request):
  if request.method == 'POST':
    playlist = Playlist()
    if request.user.is_authenticated:
      playlist.user_id = User.objects.get(username=request.user.username)
      playlist.user_name = User.objects.get(username=request.user.username).first_name
    playlist.title = request.POST['title']
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

    playlist.description = description
    playlist.view_count = 0
    playlist.like_count = 0
    
    youtube_links = request.POST.getlist('youtube_links')
    youtube_ids = ''
    for youtube_link in youtube_links:
      parsed_youtube_link = urlparse(youtube_link)
      youtube_id = parse_qs(parsed_youtube_link.query)['v'][0]
      youtube_ids += youtube_id + ','

    playlist.youtube_ids = youtube_ids
    playlist.youtube_ids_count = len(youtube_ids.split(',')) - 1
    playlist.thumnail_id = youtube_ids.split(',')[0]

    playlist.save()

    return redirect('/playlist')
  else:
    return render(request, 'playlist/playlist_add.html', {})

def playlist_info(request, playlist_pk):
    playlist = Playlist.objects.get(pk=playlist_pk)
    playlistnotes = PlaylistNote.objects.filter(playlist=playlist_pk)
    first_id = playlist.youtube_ids.split(',')[0]
    playlist.view_count += 1
    playlist.save()
    return render(request, 'playlist/playlist_info.html', {'playlist': playlist, 'first_id': first_id, 'notes': playlistnotes})

def playlistnote_add(request, playlist_pk):
  if request.method == 'POST':
    playlistnote = PlaylistNote()
    playlist = Playlist.objects.get(pk=playlist_pk)
    request_data = json.loads(request.body)

    playlistnote.title = request_data["title"]
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

    playlistnote.description = description
    playlistnote.playlist = playlist

    if request.user.is_authenticated:
      playlistnote.user_id = User.objects.get(username=request.user.username)
      playlistnote.user_name = User.objects.get(username=request.user.username).first_name

    playlistnote.save()

    return JsonResponse({"result":"success"})

def playlistnote_list(request, playlist_pk):
  playlistnotes = PlaylistNote.objects.filter(playlist=playlist_pk)
  playlistnotes = serializers.serialize('json', playlistnotes)
  return HttpResponse(playlistnotes, content_type="application/json")

def like(request, playlist_pk):
  playlist = Playlist.objects.get(pk=playlist_pk) 
  
  if not request.user.is_authenticated:
      message = "로그인을 해주세요"
      context = {'like_count' : playlist.like.count(), "message": message}
      return HttpResponse(json.dumps(context), content_type='application/json')

  user = request.user
  
  if playlist.like.filter(id = user.id).exists():
      playlist.like.remove(user)
      action = "like_cancle"
  else:
      playlist.like.add(user)
      action = "like" 

  context = {"result": "success", "action": action, "like_count" : playlist.like.count()}
  return HttpResponse(json.dumps(context), content_type='application/json') 