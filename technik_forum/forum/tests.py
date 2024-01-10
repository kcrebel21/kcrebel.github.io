from django.test import TestCase
from django.shortcuts import render
from .models import Thread, Comment

def thread_list(request):
    threads = Thread.objects.all()
    return render(request, 'forum/thread_list.html', {'threads': threads})

def thread_detail(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    comments = Comment.objects.filter(thread=thread)
    return render(request, 'forum/thread_detail.html', {'thread': thread, 'comments': comments})


# Create your tests here.
