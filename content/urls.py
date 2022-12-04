from django.urls import path, re_path
from content import views

app_name = 'content'
urlpatterns = [
    path('', views.content_list, name='content_list'),
    path('add', views.content_add, name='content_add'),
    path('<int:content_pk>', views.content_info, name="content_info"),
    path('<int:content_pk>/note/add', views.note_add, name="note_add"),
    path('<int:content_pk>/note/', views.note_list, name="note_list"),
]