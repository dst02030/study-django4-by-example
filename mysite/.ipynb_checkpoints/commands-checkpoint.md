# 1. manage.py

## 1장

### 프로젝트 생성
django-admin startproject mysite

### app 생성
python manage.py startapp blog


### 서버 실행
python manage.py runserver 222.109.225.128:8000 --settings=mysite.settings

### shell 열기
python manage.py shell

### superuser 생성
python manage.py createsuperuser



### makemigrations
python manage.py makemigrations blog

### sqlmigrate
python manage.py sqlmigrate {app명:-blog} {번호:-0001}


### migrate
python manage.py migrate


#### in shell
```{python}
from django.contrib.auth.models import User
from blog.models import Post

# 유저 정보 가져오기
user = User.objects.get(username='admin')

# 게시글 등록
post = Post(title = 'Another post',
            slug = 'another-post',
            body = 'Post body.',
            author = user)
post.save()

Post.objects.crate(title = 'One more post',
                    slug = 'one-more-post',
                    body = 'Post body.',
                    author = user)

# 업데이트
post.title = 'New title'
post.save()

# 전체 목록
Post.objects.all()

# filter
Post.objects.filter(publish__year = 2023, author__username = 'admin') # 방법 1
Post.objects.filter(publish__year = 2023).filter(author__username = 'admin') # 방법 2

# exclude
Post.objects.exclude(title__startswith = 'Who')

# order_by
Post.objects.order_by('title') # -title로 내림차순 가능

# 객체 삭제
post = Post.objects.get(id = 1)
post.delete()

# published 관리자 실행
from blog.models import Post
Post.published.filter(title__startswith = 'Who')

```

# 2. 