from django.urls import path, re_path
from content import views


app_name = 'content'
urlpatterns = [
    path('', views.post_list, name='post_list'),
]