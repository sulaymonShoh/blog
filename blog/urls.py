from django.urls import path

from blog.views import (HomePageView,
                        AboutView,
                        NewPostView,
                        PostDetailView,
                        PostDeleteView,
                        PostUpdateView,
                        RegisterView,
                        LoginView,
                        LogoutView,
                        UserProfileView
                        )
# func Based views
# home_page,post_detail, user_profile, login_view, logout_view, register_view, post_create_view)

app_name = 'blog'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # path('register/', register_view, name='register'),
    # path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),

    path('', HomePageView.as_view(), name="home-page"),
    path('about/', AboutView.as_view(), name="about"),
    path('new-post/', NewPostView.as_view(), name="new-post"),
    path('user-post/<str:username>', UserProfileView.as_view(), name="user-post"),
    # path('user-post/<str:username>', user_profile, name="user-post"),

    # path('', home_page, name="home-page"),
    # path('new-post/', post_create_view, name="new-post"),

    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    # path('post/<int:pk>/', post_detail, name='post_detail'),

    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
