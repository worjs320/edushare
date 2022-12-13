from django.urls import path, re_path
from app import views

app_name = 'app'
urlpatterns = [
    path('', views.index),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('my-content', views.mycontent, name='my-content'),
    path('my-note', views.mynote, name='my-note'),
    path('my-note-list', views.mynote_list, name='my-note-list'),
    path('my-like', views.mylike, name='myliket'),
    path('rank', views.rank, name='rank'),
]