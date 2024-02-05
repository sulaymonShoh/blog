from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView

from blog.models import Post


class HomePageView(View):
    def get(self, request):
        posts = Post.objects.all().filter(is_active=True).order_by('-created_at')[:10]
        return render(request, 'blog/home.html', {'posts': posts})


class AboutView(TemplateView):
    template_name = 'blog/about.html'


class NewPostView(TemplateView):
    template_name = "blog/post_form.html"


class UserPostView(ListView):
    model = Post
    template_name = "blog/user_posts.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_field = self.request.GET.get('author')
        queryset = queryset.filter(author=filter_field)
        return queryset


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_edit.html'
    success_url = reverse_lazy('blog:post_detail')
    success_message = "Post updated"



class PostDeleteView(SuccessMessageMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:home-page')
    success_message = "Post deleted"


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
        messages.success(request, 'Logged out successfully')
        return redirect('blog:home-page')
