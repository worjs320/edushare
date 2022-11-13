from django.shortcuts import render, HttpResponse, redirect
from .models import Content

# Create your views here.

def index():
  return redirect('/content')

def post_list(request):
  contents = Content.objects
  return render(request, 'content/content_list.html', {'contents': contents})