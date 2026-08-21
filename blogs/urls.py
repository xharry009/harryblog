from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home_page, name= "home"),
    path("allposts", views.blogposts, name= "all-posts"),
    path("allposts/<slug:blog>", views.blog_post, name="blog-post"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="blogs/login.html"),name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
