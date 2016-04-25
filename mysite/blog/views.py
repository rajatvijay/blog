from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

def post_list(request):
  published_posts = Post.published.all()
  
  return render(request, 'blog/post/list.html', {'posts': published_posts})
  
  
def post_detail(request, year, month, day, post):
  print year, month, day, post
  post = get_object_or_404(Post, status='published', slug=post, publish__year=year, publish__month=month, publish__day=day)
  
  print post
  return render(request, 'blog/post/detail.html', {'post': post})
  
