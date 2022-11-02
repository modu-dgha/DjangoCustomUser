# Database Schema
<details>
    <summary>Text Schema</summary>

```sql
Table board_board {
   title: text
   content: text
   create_date: datetime
   update_date: datetime
   user_id: bigint
   username: text
   good_count: integer
   visit: integer
   id: integer
}
Table board_board_command {
   board_id: bigint
   command_id: bigint
   id: integer
}
Table board_board_good {
   board_id: bigint
   user_id: bigint
   id: integer
}
Table board_board_tag {
   board_id: bigint
   tag_id: bigint
   id: integer
}
Table board_command {
   content: text
   user_id: bigint
   create_date: datetime
   update_date: datetime
   id: integer
}
Table board_tag {
   tag_name: varchar(50)
   id: integer
}
Table users_user {
   last_login: datetime
   is_superuser: bool
   username: varchar(256)
   email: varchar(254)
   is_staff: bool
   is_active: bool
   date_joined: datetime
   password: varchar(256)
   profile_image: varchar(100)
   id: integer
}
Table users_user_followers {
   from_user_id: bigint
   to_user_id: bigint
   id: integer
}
Table users_user_following {
   from_user_id: bigint
   to_user_id: bigint
   id: integer
}
Table users_user_good {
   user_id: bigint
   board_id: bigint
   id: integer
}
Table users_user_groups {
   user_id: bigint
   group_id: integer
   id: integer
}
```

</details>

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
 - [x] 회원가입 구현
 - [x] 로그인 구현
 - [x] 로그인, 로그아웃 구현
 - [x] 팔로잉, 팔로우 구현
 - [ ] 자신 팔로잉 방지 구현
 - [x] 프로필 사진 변경
 - [ ] 파일 다운로드 구현하기
 
## Board
