from django.db import models
from django.contrib.auth.models import User 
# Create your models here.
class Post(models.Model):
    #models.Model creates a database table
    title=models.CharField(max_length=200)
    content=models.TextField(blank=True,null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    #cascade if author is deleted delete evey post he made thats what cascade do
    #we use PROTECT if we dont want to delete the changes (eg.CUSTOMER-ORDERS)
    likes=models.IntegerField(default=0)
    #every post will remember who created it

    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    #if someoe asks string version of object 
    #makes the  object human-readable


class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment=models.TextField(null=True)
    writer=models.ForeignKey(User,on_delete=models.CASCADE)
    likes=models.IntegerField(default=0)

    time=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.writer.username}:{self.comment[:20]}"
    


    

    

    