from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from haystack.query import SearchQuerySet

# Create your views here.

#class PostListView(ListView):
#  queryset = Post.published.all()
#  context_object_name = 'posts'
#  paginate_by = 3
#  template_name = 'blog/post/list.html'
  
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

def post_list(request, tag_slug=None):
  object_list = Post.published.all()
  tag = None
  
  if tag_slug:
    tag = get_object_or_404(Tag, slug=tag_slug)
    object_list = object_list.filter(tags__in=[tag])
  
  paginator = Paginator(object_list, 3) # 3 posts in each page
  page = request.GET.get('page')
  
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer deliver the first page
    posts = paginator.page(1)
  except EmptyPage:
    # If page is out of range deliver last page of results
    posts = paginator.page(paginator.num_pages)
    
  return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})
  
  
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
    
  ## VIMP TBR CONFUSED
  #post_tags_id = post.tags.values_list('id', flat=True)
  #similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
  ## how come it counts only the similar tags not all the tags of the respectibve posts
  #similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
  
  return render(request, 'blog/post/detail.html', {'post': post, 'comment_form': comment_form, 'comments': comments, 'new_comment': new_comment})#, 'similar_posts': similar_posts})
  
  
def post_search(request):

  results = None
  total_results = None
  cd = None

  if 'query' in request.GET :
    form = SearchForm(request.GET)
    
    if form.is_valid():
      cd = form.cleaned_data
      results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
      total_results = results.count()
      
  else :
    form = SearchForm()
    
  return render(request, 'blog/post/search.html', {'form': form, 'results': results, 'total_results': total_results, 'cd': cd})
