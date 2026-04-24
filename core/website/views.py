from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import login
from django.contrib.auth import logout, password_validation
from django.contrib import messages
from django.http import HttpResponseForbidden

# Create your views here.
def login_required(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)
        else:
            return redirect('/login/')
    return wrapper

def login_view(request):
    if request.method == 'POST':
        # Прилетели данные
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        # Просто открыли страничку
        form = CustomAuthenticationForm()
    data = {
        'form': form
    }
    return render(request, 'registration/login.html', data)

def register_view(request):
    if request.method == 'POST':
        # Прилетели данные
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        # Просто открыли страничку
        form = CustomUserCreationForm()
    data = {
        'form': form
    }
    return render(request, 'registration/register.html', data)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

def index(request, id=None):
    data = {
        'categories': Category.objects.all(),
        'news': News.objects.filter(is_published=True)
    }
    if id:
        category = Category.objects.get(id=id)
        data['news'] = [i.news for i in NewsCategory.objects.filter(category=category)]
        data['category_id'] = id
    return render(request, "index.html", data)

@login_required
def news(request, id):
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        comment = Comment()
        if form.is_valid():
            comment.user = request.user
            comment.news = News.objects.get(id=id)
            comment.message = form.data['message']
            comment.save()
    data = {
        'categories': Category.objects.all(),
        'news': News.objects.get(id=id),
        'comments': Comment.objects.filter(news=id),
        'form': CommentForm()
    }
    return render(request, "news.html", data)

@login_required
def profile(request, id=None):
    if id is not None:
        comment = Comment.objects.get(id=id)
        if request.user == comment.user:
            comment.delete()
            return redirect('/profile/')
    data = {
        'categories': Category.objects.all(),
        'comments': Comment.objects.filter(user=request.user)
    }
    return render(request, 'profile.html', data)