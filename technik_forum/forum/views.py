from django.shortcuts import render, get_object_or_404, redirect
from .models import Thread, Comment
from .forms import ThreadForm, CommentForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
# In views.py

from allauth.account.views import LoginView, SignupView
from django.contrib.auth import logout

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login, authenticate
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required

from .serializers import UserProfileSerializer
from .models import UserProfile
from django.shortcuts import get_object_or_404 

def home(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'home.html')

def user_logout(request):
    logout(request)
    return redirect('home')

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  # UserProfile für den Benutzer erstellen
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


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
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('thread_detail', thread_id=thread_id)
    else:
        form = CommentForm()

    return render(request, 'forum/thread_detail.html', {'thread': thread, 'comments': comments, 'form': form})
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully.')
            return redirect('thread_detail', thread_id=comment.thread.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'forum/edit_comment.html', {'form': form})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    thread_id = comment.thread.id

    if request.method == 'POST' and request.POST.get('confirmation') == 'true':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('thread_detail', thread_id=thread_id)

    return render(request, 'forum/delete_comment.html', {'comment': comment})
@login_required
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, user=request.user)

    if request.method == 'POST' and request.POST.get('confirmation') == 'true':
        thread.delete()
        messages.success(request, 'Thread deleted successfully.')
        return redirect('thread_list')

    return render(request, 'forum/delete_thread.html', {'thread': thread})


@login_required
def new_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = request.user  # Setze den Benutzer des Threads auf den aktuellen Benutzer
            thread.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = ThreadForm()

    return render(request, 'forum/new_thread.html', {'form': form, 'thread': None})

@login_required
def user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Abrufen der vom Benutzer veröffentlichten Threads
    user_threads = Thread.objects.filter(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile)

    # Hinzufügen von Name, E-Mail-Adresse und Threads zum Kontext
    user_info = {
        'name': request.user.get_full_name(),
        'email': request.user.email,
        'threads': user_threads,
    }

    return render(request, 'user_profile.html', {'form': form, 'user_info': user_info})
