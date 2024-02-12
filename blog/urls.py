from django.urls import path

from blog.views import (HomePageView,
                        AboutView,
                        PostCreateView,
                        PostDetailView,
                        PostDeleteView,
                        PostUpdateView,
                        RegisterView,
                        LoginView,
                        LogoutView,
                        UserProfileView,
    # func Based views
    # home_page,post_detail, user_profile, login_view, logout_view, register_view, post_create_view,
    # post_update, post_delete_view
                        )

app_name = 'blog'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', HomePageView.as_view(), name="home_page"),
    path('about/', AboutView.as_view(), name="about"),
    path('post/create', PostCreateView.as_view(), name="post_create"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post_update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('users/<str:username>', UserProfileView.as_view(), name="user_posts"),

    # path('register/', register_view, name='register'),
    # path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),

    # path('', home_page, name="home-page"),
    # path('post/create/', post_create_view, name="new-post"),
    # path('post/<int:pk>/', post_detail, name='post_detail'),
    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    # path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    # path('user-post/<str:username>', user_profile, name="user-post"),

]
