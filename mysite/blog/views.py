from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag

# Create your views here.

class PostListView(ListView):
  queryset = Post.published.all()
  context_object_name = 'posts'
  paginate_by = 3
  template_name = 'blog/post/list.html'
  
def post_share(request, post_id):
  post = get_object_or_404(Post, id=post_id, status='published')
  
  sent = False
  cd = None
  
  if request.method == 'POST':
    # form was submitted
    form = EmailPostForm(request.POST)
    if form.is_valid():
      # form fields passed validation
      cd = form.cleaned_data # have no idea what does this do 
      post_url = request.build_absolute_uri(post.get_absolute_url()) # TBR
      subject = '{0} ({1}) recommends you reading "{2}"'.format(cd['name'], cd['email'], post.title)
      message = 'Read "{0}" at\n\n{1}\'s, comments: {2}'.format(post.title, post_url, cd['name'], cd['comments'])
      send_mail(subject, message, 'rajatvijay5@gmail.com', [cd['to']])
      sent = True
      
      # ... send mail
  else:
    form = EmailPostForm()
    
  return render(request, 'blog/post/share.html', {'form': form, 'post': post, 'sent': sent, 'cd': cd})

#def post_list(request):
#  posts_list = Post.published.all()
#  paginator = Paginator(posts_list, 3)
#  
#  # page_number --> gets the number of current page
#  page_number = request.GET.get('page')
#  
#  try:
#   
#    # paginator.page() --> the page object having methods to retrieve objects(object_list)
#    # of page no indicated by page variable   
#    page = paginator.page(page_number)
#    
#  except PageNotAnInteger :
#    #If page_number is not an integer deliver the first page
#    page = paginator.page(1)
#  except EmptyPage:
#    # If page_number is out of range deliver last page of results
#    page = paginator.page(paginator.num_pages)
#    
#  # rather than passing a posts quesry set we pass a page object
#  # page object has all the query set objects for the given page number only 
#  # https://docs.djangoproject.com/en/1.9/topics/pagination/
#  return render(request, 'blog/post/list.html', {'page': page})
  
  
def post_detail(request, year, month, day, post):
  post = get_object_or_404(Post, status='published', slug=post, publish__year=year, publish__month=month, publish__day=day)
  
  comments = post.comment.filter(active=True)
  new_comment = None
  
  if request.method == 'POST':
    comment_form = CommentForm(data=request.POST)
    
    if comment_form.is_valid():
      new_comment = comment_form.save(commit=False)
      new_comment.post = post
      new_comment.save()
      
  else:
    comment_form = CommentForm()
  
  return render(request, 'blog/post/detail.html', {'post': post, 'comment_form': comment_form, 'comments': comments, 'new_comment': new_comment})
  
