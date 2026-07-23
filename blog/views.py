from django.shortcuts import *
from django.http import HttpResponse,HttpResponseForbidden
from .models import Post,Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import author_required,comment_author
"""db -> database it is the ORM(object relational mapper) for creating data base"""
from django.http import JsonResponse
import json
#Creating Author to verify the owner of the blog and fix it 
#so CRUD operations can performed only by the owner


"""render(
request,
template,
context
)"""

def home(request):
    posts=Post.objects.all()
    #every django model has a manager called objects
    #

    # return HttpResponse("Welcome to Blog!")
    return render(request,"blog/home.html",{
        "posts":posts  #context the template can access posts
    })
  #rendering html


def about(request):
    return render(request,"blog/about.html")

def contacts(request):
    return render(request,"blog/contacts.html")

def post_detail(request,post_id):
    post=Post.objects.get(id=post_id)
    #POst.objects.all() give me every post
    #get(id=id) give me exactly whose id matches
    comment=Comment.objects.filter(post=post)

    return render(
        request,
        "blog/post_detail.html",{
            "post":post,
            "comments":comment
        }
    )

@login_required
def create_post(request):
    # return render(request,"blog/create_post.html")
    """There can be two possibilities the user want s to request access to view the
    create_post page which is the case of get request or the user fills out the form whih is the example of 
    post request"""
    
    if request.method=="POST":
        title=request.POST["title"]
        content=request.POST["content"]

        Post.objects.create(
            title=title,
            content=content,
            author=request.user
        )

        return redirect("home")
    
    return render(request,"blog/create_post.html")

@login_required
@author_required
def edit_post(request,post):
    

    #checking if the owner of the post is editing it

    # if post.author!=request.user:
    #     return HttpResponseForbidden()
    

    if request.method=="POST":
        post.title=request.POST["title"]
        post.content=request.POST["content"]

        post.save()

        return redirect("post_detail",post.id)
    
    return render(request,"blog/edit_post.html",{"post":post})
    

@login_required
@author_required
def delete_post(request,post):
    

    # if post.author!=request.user:
    #     return HttpResponseForbidden


    if request.method=="POST":
        post.delete()
        return redirect("home")
    
    return render(
        request,"blog/delete_post.html",{"post":post}
    )


def register(request):
    if request.method=="POST":
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]

        if User.objects.filter(username=username).exists():
            print("Username already exists")
            return render(request,"blog/register.html",{"error":"Username already exists."})

        user=User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")
    
    return render(request,"blog/register.html")

def login_view(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)  #creates the session for user
            return redirect("home")
        
    return render(request,"blog/login.html")


def logout_view(request):
    
    logout(request)
    return redirect("home")


@login_required
def like_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)

    if request.method=="POST":
        if post.author==request.user:
            print("You can't like your own post!")
            
            return redirect("post_detail",post_id=post.id)
        
        post.likes+=1
        post.save()


    # return redirect("post_detail",post_id=post.id)
    return JsonResponse({
        "likes":post.likes
    })

# def comments(request,post_id):
#     post=get_object_or_404(Post,id=post_id)
#     comments=Comment.objects.filter(post=post)

#     return render(
#         request,"blog/post_details.html",{
#             "post":post,
#             "comments":comments
#         }
#     )




@login_required
def add_comment(request,post_id):
    post=get_object_or_404(Post,id=post_id)

    if request.method!="POST":
        return JsonResponse({"error":"Invalid"},status=405)

    data=json.loads(request.body)
    comment=data["comment"]
    Comment.objects.create(
        post=post,
        writer=request.user,
        #senting user object
        comment=comment
    )

    return JsonResponse({
        "author":post.author.username,
        "comment":comment,
        "writer":request.user.username
    })

@login_required
def like_comment(request,post_id,comment_id):
    post=get_object_or_404(Post,id=post_id)
    comment=Comment.objects.get(post=post,id=comment_id)
    
    if request.method=="POST":
        comment.likes+=1
        comment.save()

    return JsonResponse({
        "likes":comment.likes
    })

@login_required
@comment_author
def edit_comment(request,post,comment):
    if request.method=="POST":
        data=json.loads(request.body)
        new_text=data["comment"]

        comment.comment=new_text
        comment.save()

        return JsonResponse({
            "comment":comment.comment
        }
        ) 

    
    return JsonResponse(
        {"error": "Only POST requests are allowed"},
        status=405
    )

@login_required
@comment_author
def delete_comment(request,post,comment):
    if request.method!="POST":
        return JsonResponse(
            {"error":"Only POST requests are allowed!"},
            status=405
        )
    
    comment.delete()
    

    return JsonResponse({
        "sucess":True
    })

    




# def admin(request):
#     return render(request)
# Create your views here.