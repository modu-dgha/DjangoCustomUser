# Database Schema

![](https://user-images.githubusercontent.com/117153297/199434078-50baeaa3-c488-48dd-aa36-4b5f51584844.svg)

## User
```py
class User(AbstractUser):
    username = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    good = models.ManyToManyField('board.Board', related_name='user_good')
    following = models.ManyToManyField('self', related_name='following')
    followers = models.ManyToManyField('self', related_name='followers')
    profile_image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    first_name = None
    last_name = None
```

## Board
```py
class Tag(models.Model):
    tag_name = models.CharField(unique=True, max_length=50, blank=False, null=False)


class Board(models.Model):
    title = models.TextField(blank=False)
    content = models.TextField(blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    username = models.TextField(blank=False)
    good = models.ManyToManyField('users.User', related_name='board_good')
    good_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, models.CASCADE)
    command = models.ManyToManyField('Command', related_name='command')
    visit = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag, related_name='board_tag')


class Command(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=False)
    user = models.ForeignKey(User, models.CASCADE)
```

# Work
## User
 - [x] 회원가입
 - [x] 로그인, 로그아웃
 - [x] 팔로잉, 팔로우
 - [ ] 자신 팔로우 방지 구현
 - []
 
## Board
