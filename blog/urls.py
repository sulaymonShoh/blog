from django.urls import path

from blog.views import HomePageView, AboutView, NewPostView, UserPostView, PostDetailView

app_name = 'blog'
urlpatterns = [
    path('', HomePageView.as_view(), name="home-page"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('about/', AboutView.as_view(), name="about"),
    path('new-post/', NewPostView.as_view(), name="new-post"),
    path('user-post/',UserPostView.as_view(), name="user-post"),
]
