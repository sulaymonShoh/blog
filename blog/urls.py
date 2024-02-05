from django.urls import path

from blog.views import HomePageView, AboutView, NewPostView, UserPostView, PostDetailView, PostDeleteView, \
    PostUpdateView, RegisterView, LoginView, LogoutView

app_name = 'blog'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', HomePageView.as_view(), name="home-page"),
    path('about/', AboutView.as_view(), name="about"),
    path('new-post/', NewPostView.as_view(), name="new-post"),
    path('user-post/<str:author>/', UserPostView.as_view(), name="user-post"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
