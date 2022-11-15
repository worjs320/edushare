from django.urls import path, re_path
from app import views


app_name = 'app'
urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.signin, name='signin'),
]