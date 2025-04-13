from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.decorators.http import require_POST
from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # id로 게시물 조회
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # 폼이 제출되었다면
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 유효성 검사를 통과한 폼 필드들
            cd = form.cleaned_data
            # 이메일 전송
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read " \
                    f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                    f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])
            sent = True
    
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
                    {'post': post, 'form': form, 'sent': sent})

# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    # 페이지당 3개의 게시물로 페이지 매김
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # page_number가 정수가 아닌 경우 첫 번째 페이지 전달
        posts = paginator.page(1)
    except EmptyPage:
        # 페이지 번호가 범위를 벗어난 경우 결과의 마지막 페이지를 전달
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})
    
def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.published.get(id = id)
    
    # except Post.DoesNotExist:
    #     raise Http404("No Post found.")

    post = get_object_or_404(Post,
                             status = Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # 이 글의 active 댓글 목록
    comments = post.comments.filter(active=True)
    # 사용자가 댓글을 달 수 있는 폼
    form = CommentForm()
    
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                  'comments': comments,
                  'form': form})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # 댓글이 달림
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # 데이터베이스에 저장하지 않고 Comment 객체 생성
        comment = form.save(commit=False)
        # 댓글에 게시물 할당하기
        comment.post = post
        # 댓글을 데이터베이스에 저장
        comment.save()
    
    return render(request, 'blog/post/comment.html',
    {'post': post, 'form': form, 'comment': comment})
