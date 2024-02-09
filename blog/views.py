import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, UserRegistrationForm, PostCreateForm
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView, CreateView

from blog.models import Post, User


class HomePageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            posts = Post.objects.exclude(author=request.user).filter(is_active=True).order_by('published')
        else:
            posts = Post.objects.all().filter(is_active=True).order_by('published')
        return render(request, 'blog/home.html', {'posts': posts})


# def home_page(request):
#     if request.user.is_authenticated:
#         posts = Post.objects.exclude(author=request.user).filter(is_active=True).order_by('published')
#     else:
#         posts = Post.objects.all().filter(is_active=True).order_by('published')
#     # posts = posts.filter(is_active=True).order_by('published')
#     return render(request, 'blog/home.html', {'posts': posts})


class AboutView(TemplateView):
    template_name = 'blog/about.html'


class NewPostView(View):
    def get(self, request):
        form = PostCreateForm
        return render(request, 'blog/post_form.html', {"form": form})

    def post(self, request):
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published = datetime.datetime.now().strftime("%Y-%m-%d")
            post.save()
            messages.success(request, "Post successfully created")
            return redirect("blog:home-page")
        else:
            return render(request, "blog/post_form.html", {"form": form})


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_edit.html'
    # success_url = reverse_lazy('blog:post_detail', )
    success_message = "Post updated"


class PostDeleteView(SuccessMessageMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:home-page')
    success_message = "Post deleted"


class UserProfileView(View):
    def get(self, request, username, ):
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(author__username=username)
        first_name = user.first_name
        last_name = user.last_name
        return render(request, 'blog/user_posts.html', {'posts': posts,
                                                        'first_name': first_name,
                                                        'last_name': last_name})


# views.py

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'blog/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:login')
        return render(request, 'blog/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('blog:home-page')

        messages.error(request, 'Username or password wrong')
        return render(request, 'blog/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'Logged out successfully')
        return redirect('blog:home-page')

# function based views

# @login_required
# def user_profile(request, username):
#     user = get_object_or_404(User, username=username)
#     posts = Post.objects.filter(author__username=username)
#     first_name = user.first_name
#     last_name = user.last_name
#     return render(request, 'blog/user_posts.html', {'posts': posts,
#                                                     'first_name': first_name,
#                                                     'last_name': last_name})
#
#
# def post_detail(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})
#
#
# def login_view(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
#             if user is not None:
#                 login(request, user)
#                 return redirect("blog:home-page")
#             else:
#                 messages.warning(request, 'User not found')
#                 return redirect("blog:login")
#         else:
#             return render(request, 'blog/login.html', {"form": form})
#     else:
#         form = LoginForm()
#
#     return render(request, 'blog/login.html', {"form": form})


# def register_view(request):
#     form = UserRegistrationForm()
#     if request.method == "POST":
#         form = UserRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "User successfully registered")
#             return redirect('blog:login')
#         else:
#             return render(request, 'blog/register.html', {"form": form})
#     else:
#         return render(request, 'blog/register.html', {"form": form})


# @login_required
# def logout_view(request):
#     logout(request)
#     messages.info(request, f'{request.user.username} logged out successfully')
#     return redirect('blog:home-page')


# def post_create_view(request):
#     if request.method == "POST":
#         form = PostCreateForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published = datetime.datetime.now().date
#             post.save()
#             messages.success(request, "Post successfully created")
#             return redirect("blog:home-page")
#         else:
#             return render(request, "blog/post_form.html", {"form": form})
#     else:
#         form = PostCreateForm()
#         return render(request, "blog/post_form.html", {"form": form})
