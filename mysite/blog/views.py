from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

def post_list(request):
  posts_list = Post.published.all()
  paginator = Paginator(posts_list, 3)
  
  # page_number --> gets the number of current page
  page_number = request.GET.get('page')
  
  try:
    
    # paginator.page() --> the page object having methods to retrieve objects(object_list)
    # of page no indicated by page variable   
    page = paginator.page(page_number)
    
  except PageNotAnInteger :
    #If page_number is not an integer deliver the first page
    page = paginator.page(1)
  except EmptyPage:
    # If page_number is out of range deliver last page of results
    page = paginator.page(paginator.num_pages)
    
  # rather than passing a posts quesry set we pass a page object
  # page object has all the query set objects for the given page number only 
  # https://docs.djangoproject.com/en/1.9/topics/pagination/
  return render(request, 'blog/post/list.html', {'page': page})
  
  
def post_detail(request, year, month, day, post):
  print year, month, day, post
  post = get_object_or_404(Post, status='published', slug=post, publish__year=year, publish__month=month, publish__day=day)
  
  print post
  return render(request, 'blog/post/detail.html', {'post': post})
  
