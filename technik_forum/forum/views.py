from django.shortcuts import render, get_object_or_404, redirect
from .models import Thread, Comment
from .forms import ThreadForm, CommentForm

def thread_list(request):
    threads = Thread.objects.all()
    return render(request, 'forum/thread_list.html', {'threads': threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    comments = Comment.objects.filter(thread=thread)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.save()
            return redirect('thread_detail', thread_id=thread_id)
    else:
        form = CommentForm()

    return render(request, 'forum/thread_detail.html', {'thread': thread, 'comments': comments, 'form': form})

def new_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = ThreadForm()

    return render(request, 'forum/new_thread.html', {'form': form})

