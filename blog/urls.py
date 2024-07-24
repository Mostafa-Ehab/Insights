from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('blogs', blogs_view, name="blogs"),
    path('post/<slug:slug>', post_view, name="post"),
    path('category/<slug:slug>', category, name="category"),
    path('tag/<slug:slug>', tag, name="tag"),
    # path('add_comment/<int:post_id>', add_comment, name="add_comment"),
    path('add-reply/<int:comment_id>', add_reply, name="add_reply"),
    path('like-post/<int:post_id>', like_post, name="like-post"),
    path('search', search, name="search"),
    path('user/<slug:slug>', author_profile, name="author"),
    path('follow/<int:user_id>', follow, name="follow"),
    path('profile', profile, name="profile"),
    path('my-blogs', my_blogs_view, name="my_blogs"),
    path('add-post', add_post_view, name="add_post"),
    path('edit/<slug:slug>', edit_post_view, name="edit_post"),
    path('delete/<slug:slug>', delete_post, name="delete_post"),
    path('about', about_us, name="about")
]

handler404 = "blog.views.not_found"
