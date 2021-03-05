from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Model for Post related data
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    content = models.TextField()
    slug = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    timestamp = models.DateTimeField( blank=True)
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return  self.title +" by -  " + self.author

# Model for Post comment related data
class Blogcomment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    parent = models.ForeignKey('self' , on_delete=models.CASCADE , null=True)
    timestamp = models.DateTimeField( default=now)
    
    def __str__(self):
        return  self.comment[0:15] + "... " + " by -  "  + self.user.username

        