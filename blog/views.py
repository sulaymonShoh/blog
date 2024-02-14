import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import TemplateView, DetailView, DeleteView, UpdateView

from blog.models import Post, User
from blog.forms import LoginForm, UserRegistrationForm, PostCreateForm, PostUpdateForm


class HomePageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            posts = Post.objects.exclude(author=request.user).filter(is_active=True).order_by('published')
        else:
            posts = Post.objects.all().filter(is_active=True).order_by('published')

        size = request.GET.get("size", 6)
        page = request.GET.get("page", 1)
        paginator = Paginator(posts, size)
        page_obj = paginator.get_page(page)
        return render(request, 'blog/home.html', {'page_obj': page_obj, "num_pages": paginator.num_pages})


# def home_page(request):
#     if request.user.is_authenticated:
#         posts = Post.objects.exclude(author=request.user).filter(is_active=True).order_by('published')
#     else:
#         posts = Post.objects.all().filter(is_active=True).order_by('published')
#     # posts = posts.filter(is_active=True).order_by('published')
#     return render(request, 'blog/home.html', {'posts': posts})


class AboutView(TemplateView):
    template_name = 'blog/about.html'


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
    success_url = reverse_lazy('blog:home_page')
    success_message = "Post deleted"


class PostCreateView(View):
    def get(self, request):
        form = PostCreateForm()
        return render(request, 'blog/post_form.html', {"form": form})

    def post(self, request):
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published = datetime.datetime.now().strftime("%Y-%m-%d")
            post.save()
            messages.success(request, "Post successfully created")
            return redirect("blog:home_page")
        else:
            return render(request, "blog/post_form.html", {"form": form})


class UserProfileView(View):
    def get(self, request, username, ):
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(author__username=username)
        first_name = user.first_name
        last_name = user.last_name

        size = request.GET.get("size", 6)
        page = request.GET.get("page", 1)
        paginator = Paginator(posts, size)
        page_obj = paginator.get_page(page)
        return render(request, 'blog/user_posts.html', {'page_obj': page_obj,
                                                        'first_name': first_name,
                                                        'last_name': last_name})


# views.py

class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'blog/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            messages.success(request, "User Successfully created")
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
                return redirect('blog:home_page')

        messages.warning(request, 'Username or password wrong')
        return render(request, 'blog/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'Logged out successfully')
        return redirect('blog:home_page')


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


@login_required
def post_update(request, pk: int):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = PostUpdateForm(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully")
            return redirect(reverse("blog:post_detail", kwargs={"pk": post.id}))
        else:
            return render(request, 'blog/post_update.html', {"form": form})
    else:
        form = PostUpdateForm(instance=post)
        return render(request, "blog/post_update.html", {"form": form})


@login_required
def post_delete_view(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully")
        return redirect("blog:home-page")
    else:
        return render(request, "blog/post_confirm_delete.html", {"post": post})
