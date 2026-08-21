from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Post
from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login


# Create your views here.

def home_page(request):
    latest_blogs = Post.objects.all().order_by("-date")[:2]
    return render(request,"blogs/index.html", {"l_blogs": latest_blogs})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            user = form.save()
            login(request, user) 
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'blogs/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'blogs/login.html', {'form': form})


def blogposts(request):
    blog_details = Post.objects.all()
    return render(request, "blogs/allposts.html", {"blogs": blog_details})



def blog_post(request, blog):
        post_data = Post.objects.get(slug =blog)
        tag_caption = post_data.tags.all()
        all_comments = post_data.comments.all().order_by("-id")
        
        if request.method == "POST":
            commented_data = request.POST
            form = CommentForm(commented_data)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post =post_data
                comment.save()
                return HttpResponseRedirect(reverse("blog-post", args=[blog]))
            return render(request,"blogs/posts.html",{
                "post":post_data, "tags": tag_caption, "comment_form": form, "comments": all_comments})
        else:
            try:
                form_data = CommentForm()
                return render(request,"blogs/posts.html",{
                    "post":post_data, "tags": tag_caption, "comment_form": form_data, "comments": all_comments})
            except Exception:
                raise Http404()
        

