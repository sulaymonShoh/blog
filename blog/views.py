from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from blog.models import Post


class HomePageView(View):
    def get(self, request):
        posts = Post.objects.all().filter(is_active=True).order_by('-created_at')[:10]
        return render(request, 'blog/home.html', {'posts': posts})


class AboutView(TemplateView):
    template_name = 'blog/about.html'


class NewPostView(TemplateView):
    template_name = "blog/post_form.html"


class UserPostView(TemplateView):
    template_name = "blog/user_posts.html"


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'
