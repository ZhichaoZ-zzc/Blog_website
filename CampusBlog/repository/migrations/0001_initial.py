# Generated by Django 3.0.2 on 2020-03-03 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='文章标题')),
                ('summary', models.CharField(max_length=255, verbose_name='文章简介')),
                ('read_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('up_count', models.IntegerField(default=0)),
                ('down_count', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article_type_id', models.IntegerField(choices=[(1, 'python'), (2, 'Linux'), (2, 'OpenStack'), (4, 'GoLang')], default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='个人博客标题')),
                ('site', models.CharField(max_length=32, unique=True, verbose_name='个人博客前缀')),
                ('theme', models.CharField(max_length=32, verbose_name='博客主题')),
            ],
        ),
        migrations.CreateModel(
            name='UserFans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('nickname', models.CharField(max_length=32, verbose_name='昵称')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('avatar', models.ImageField(upload_to='', verbose_name='头像')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('fans', models.ManyToManyField(related_name='f', through='repository.UserFans', to='repository.UserInfo', verbose_name='粉丝们')),
            ],
        ),
        migrations.AddField(
            model_name='userfans',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='repository.UserInfo', verbose_name='粉丝'),
        ),
        migrations.AddField(
            model_name='userfans',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='repository.UserInfo', verbose_name='博主'),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='标签名称')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Blog', verbose_name='所属博客')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=255, verbose_name='评论内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Article', verbose_name='评论文章')),
                ('reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='back', to='repository.Comment', verbose_name='回复评论')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.UserInfo', verbose_name='评论者')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='分类标题')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Blog', verbose_name='所属博客')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repository.UserInfo'),
        ),
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repository.Article', verbose_name='所属文章')),
            ],
        ),
        migrations.CreateModel(
            name='Article2Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Article', verbose_name='文章')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Tag', verbose_name='标签')),
            ],
            options={
                'unique_together': {('article', 'tag')},
            },
        ),
        migrations.AddField(
            model_name='article',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Blog', verbose_name='所属博客'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.Category', verbose_name='文章类型'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(through='repository.Article2Tag', to='repository.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='userfans',
            unique_together={('user', 'follower')},
        ),
        migrations.CreateModel(
            name='UpDown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up', models.BooleanField(verbose_name='是否赞')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Article', verbose_name='文章')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.UserInfo', verbose_name='赞或踩用户')),
            ],
            options={
                'unique_together': {('article', 'user')},
            },
        ),
    ]
