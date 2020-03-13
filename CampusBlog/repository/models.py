from django.db import models

# Create your models here.

class UserInfo(models.Model):
    """
    用户表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像')

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    fans = models.ManyToManyField(verbose_name="粉丝们",
                                  to='UserInfo',
                                  through='UserFans',
                                  related_name='f',
                                  through_fields=('user','follower')
                                  )
    def __str__(self):
        return "%s"%self.username
class Blog(models.Model):
    """
    博客信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客前缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)       #用于改变个人博客的样式
    user = models.OneToOneField(to='UserInfo', to_field='nid',on_delete=models.CASCADE)

    def __str__(self):
        return "%s"%(self.title)

class UserFans(models.Model):
    """
    互粉关系表
    """
    user =models.ForeignKey(verbose_name='博主',to='UserInfo',to_field='nid',related_name='users',on_delete=models.CASCADE)
    follower = models.ForeignKey(verbose_name='粉丝',to='UserInfo',to_field='nid',related_name='followers',on_delete=models.CASCADE)

    class Meta:
        unique_together =[
            ('user', 'follower')
        ]
        #有1：1之后  不能再有1：1

class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid',on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.title)

class ArticleDetail(models.Model):
    """
    文章详细表
    """
    content = models.TextField(verbose_name='文章内容', )

    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid',on_delete=models.CASCADE)

    def __str__(self):
        return "%s" %(self.article.title)

class UpDown(models.Model):
    """
    文章顶或踩
    """
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid',on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='赞或踩用户', to='UserInfo', to_field='nid',on_delete=models.CASCADE)
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together =[
            ('article','user'),
        ]

class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    reply = models.ForeignKey(verbose_name="回复评论",to='self',related_name='back',null=True,on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid',on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid',on_delete=models.CASCADE)

class Tag(models.Model):
    """
    标签表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid',on_delete=models.CASCADE)

    def __str__(self):
        return "%s"%(self.title)

class Article(models.Model):
    """
    文章表
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章简介', max_length=255)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid',on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', null=True,on_delete=models.CASCADE)

    type_choices =[
        (1,"学校区"),
        (2,"学院区"),
        (3,"专业区"),
        (4,"表白墙"),
    ]
    article_type_id = models.IntegerField(choices=type_choices,default=None)
    tags = models.ManyToManyField(to="Tag",through='Article2Tag',through_fields=('article','tag'))

    def __str__(self):
        return "%s"%(self.title)

class Article2Tag(models.Model):
    article =models.ForeignKey(verbose_name='文章', to="Article", to_field='nid',on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid',on_delete=models.CASCADE)

    class Meta:
        unique_together =[
            ('article','tag')
        ]


class Trouble(models.Model):
    title = models.CharField(max_length=32)
    detail = models.TextField()
    user = models.ForeignKey(UserInfo,related_name='u',on_delete=models.CASCADE)
    # ctime = models.CharField(max_length=32) # 1491527007.452494
    ctime = models.DateTimeField()
    status_choices = (
        (1,'未处理'),
        (2,'处理中'),
        (3,'已处理'),
    )
    status = models.IntegerField(choices=status_choices,default=1)

    processer = models.ForeignKey(UserInfo,related_name='p',null=True,blank=True,on_delete=models.CASCADE)
    solution = models.TextField(null=True)
    ptime = models.DateTimeField(null=True)
    pj_choices = (
        (1, '不满意'),
        (2, '一般'),
        (3, '活很好'),
    )
    pj = models.IntegerField(choices=pj_choices,null=True,default=2)





###########

class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "用户表"
    def __str__(self):
        return self.username

class Role(models.Model):
    caption = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "角色表"
    def __str__(self):
        return self.caption


class User2Role(models.Model):
    u = models.ForeignKey("User",on_delete=models.CASCADE)
    r = models.ForeignKey("Role",on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "角色分配表"

    def __str__(self):
        return "%s--%s" %(self.u.username,self.r.caption)


class Action(models.Model):
    caption = models.CharField(max_length=32)
    code = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural="操作表"

    def __str__(self):
        return self.caption


class Menu(models.Model):
    caption = models.CharField(max_length=32)
    parent = models.ForeignKey('self',related_name='p',null=True,blank=True,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="菜单表"
    def __str__(self):
        return "%s" %(self.caption)


class Permission(models.Model):
    caption = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    menu = models.ForeignKey("Menu",null=True,blank=True,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="URL表"

    def __str__(self):
        return "%s--%s" %(self.caption,self.url)


class Permission2Action(models.Model):
    a = models.ForeignKey("Action", on_delete=models.CASCADE)
    p = models.ForeignKey("Permission",on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "权限表"

    def __str__(self):
        return "%s-%s:%s?t=%s"%(self.p.caption,self.a.caption,self.p.url,self.a.code)

class Permission2Action2Role(models.Model):
    p2a =models.ForeignKey("Permission2Action",on_delete=models.CASCADE)
    r =models.ForeignKey("Role",on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='角色分配权限'

    def __str__(self):
        return "%s===>%s"%(self.r.caption,self.p2a)










