from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
# Create your models here.
class BlogAuthor(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(max_length=400, help_text="输入博主的个人经历")

    class Meta:
        ordering = ["user", "bio"]

    def get_absolute_url(self):
        #点击一个具体的作者 就会进入到链接blogs-by-author的映射，参数为id
        return reverse('blogs-by-author', args=[str(self.id)])
    def __str__(self):
        return self.user.username


class Blog(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(BlogAuthor, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=2000, help_text="输入博客的详细内容")
    post_date = models.DateField(default=date.today)

    class Meta:
        ordering = ["-post_date"]   #按照上传时间 降序排列 也就是最新上传的显示

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class BlogComment(models.Model):
    description = models.TextField(max_length=1000, help_text="输入您的评论")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    #auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间。
    #auto_now_add为添加时的时间，更新对象时不会有变动。
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        ordering = ["post_date"]

    def __str__(self):
        len_title = 75
        if len(self.description) > len_title:
            titlestring = self.description[:len_title] + '...'
        else:
            titlestring = self.description
        return titlestring