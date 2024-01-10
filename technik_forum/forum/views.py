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

def home(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'home.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomSignupView(SignupView):
    template_name = 'signup.html'


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



def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    thread_id = comment.thread.id
    comment.delete()
    messages.success(request, 'Comment deleted successfully.')
    return redirect('thread_detail', thread_id=thread_id)

def new_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = ThreadForm()

    return render(request, 'forum/new_thread.html', {'form': form})

@login_required
def user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'user_profile.html', {'form': form})
