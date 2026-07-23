from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Post,Comment

def author_required(func):
    def wrapper(request,post_id,*args,**kwargs):
        post=get_object_or_404(Post,id=post_id)

        if post.author!=request.user:
            return HttpResponseForbidden("You are not allowed to modify this post!\n")
        
        return func(request,post,*args, **kwargs)
    
    return wrapper


def comment_author(func):
    def wrapper(request,post_id,comment_id,*args,**kwargs):
        post=get_object_or_404(Post,id=post_id)
        comment=get_object_or_404(Comment,post=post,id=comment_id)
        
        if comment.writer!=request.user:
            return HttpResponseForbidden("Not allowed!")
        
        return func(request,post,comment,*args,**kwargs)
    
    return wrapper



    


