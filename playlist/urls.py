from django.urls import path
from playlist import views

app_name = 'playlist'
urlpatterns = [
    path('', views.playlist_list, name='playlist_list'),
    path('add', views.playlist_add, name='playlist_add'),
    path('<int:playlist_pk>', views.playlist_info, name="playlist_info"),
    path('<int:playlist_pk>/note/add', views.playlistnote_add, name="note_add"),
    path('<int:playlist_pk>/note/', views.playlistnote_list, name="note_list"),
    path('<int:playlist_pk>/like', views.like, name="like"),
]