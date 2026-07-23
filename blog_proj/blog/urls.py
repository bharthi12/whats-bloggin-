from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("about/",views.about),
    path("contacts/",views.contacts),
    # path("admin/",views.admin)
    path("post/<int:post_id>/",views.post_detail,name="post_detail"),
    #captures integer from url and stores in a variale called id
    path("create/",views.create_post,name="create_post"),
    path("post/<int:post_id>/editpost/",views.edit_post,name="edit_post"),
    path("post/<int:post_id>/deletepost/",views.delete_post,name="delete"),
    path("login/",views.login_view,name="login"),
    path("register/",views.register,name="register"),
    path("logout/",views.logout_view,name="logout"),
    path("post/<int:post_id>/like_post/",views.like_post,name="like_post"),
    path("post/<int:post_id>/comment/",views.add_comment,name="comment"),
    path('post/<int:post_id>/commentlike/<int:comment_id>',views.like_comment,name="like_comment"),
    path("post/<int:post_id>/editcomment/<int:comment_id>",views.edit_comment,name="edit_comment"),
    path("post/<int:post_id>/deletecomment/<int:comment_id>",views.delete_comment,name="delete_comment")
    
]

