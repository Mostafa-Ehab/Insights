from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, JsonResponse, Http404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.contrib import messages

from .models import Blog, Tag, Category, Comment, Reply
from user_profile.models import Follow
from .forms import *

# Create your views here.
def home(request: HttpRequest):
    blogs = Blog.objects.order_by("-created_date")

    return render(request, "pages/home.html", {
        "blogs": blogs,
        "title": "Insights | Homepage | Mostafa Ehab"
        # "tags": tags,
    })

def about_us(request: HttpRequest):
    return render(request, "pages/about.html", {
        "title": "Insights | About us | Mostafa Ehab"
    })

def blogs_view(request: HttpRequest):
    queryset = Blog.objects.order_by("-created_date")
    # tags = Tag.objects.order_by("-created_date")

    paginator = Paginator(queryset, 20)
    page = request.GET.get("page", 1)

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        return redirect("blogs")
    except UnboundLocalError:
        return redirect("blogs")

    return render(request, "pages/blogs.html", {
        "blogs": blogs,
        "title": "Insights | Blogs | Mostafa Ehab"
        # "tags": tags,
    })

def post_view(request: HttpRequest, slug: str):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Blog, slug=slug)

            Comment.objects.create(
                text = form.cleaned_data.get("comment"),
                user = request.user,
                blog = post
            )

            return redirect(reverse("post", kwargs={"slug": post.slug}))
    else:
        form = CommentForm()

    post = get_object_or_404(Blog, slug=slug)
    related_posts = Blog.objects.filter(category=post.category).exclude(pk=post.pk)
    # tags = Tag.objects.order_by("-created_date")

    return render(request, "pages/post.html", {
        "post": post,
        "related_posts": related_posts,
        "comment_form": form,
        "reply_form": ReplyForm(),
        "title": f"Insights | {post.title} | Mostafa Ehab"
        # "tags": tags,
    })

def category(request: HttpRequest, slug: str):
    category = get_object_or_404(Category, slug=slug)
    queryset = category.category_blogs.all().order_by("-created_date")
    # tags = Tag.objects.order_by("-created_date")

    paginator = Paginator(queryset, 20)
    page = request.GET.get("page", 1)

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        return redirect(reverse("category", kwargs={"slug": category.slug}))
    except UnboundLocalError:
        return redirect(reverse("category", kwargs={"slug": category.slug}))

    return render(request, "pages/category.html", {
        "category": category,
        "blogs": blogs,
        "title": f"Insights | {category.title} | Mostafa Ehab"
        # "tags": tags,
    })


def tag(request: HttpRequest, slug: str):
    tag = get_object_or_404(Tag, slug=slug)
    queryset = tag.tag_blogs.all().order_by("-created_date")
    # tags = Tag.objects.order_by("-created_date")

    paginator = Paginator(queryset, 20)
    page = request.GET.get("page", 1)

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        return redirect(reverse("tag", kwargs={"slug": tag.slug}))
    except UnboundLocalError:
        return redirect(reverse("tag", kwargs={"slug": tag.slug}))

    return render(request, "pages/tag.html", {
        "tag": tag,
        "blogs": blogs,
        "title": f"Insights | {tag.title} | Mostafa Ehab"
        # "tags": tags,
    })


def search(request: HttpRequest):
    search = request.GET.get("search")

    if search:
        blogs = Blog.objects.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(tags__title__icontains=search) |
            Q(category__title__icontains=search) | 
            Q(author__username__icontains=search)
        ).distinct().order_by("-created_date")

        return render(request, "pages/search.html", {
            "query": search,
            "blogs": blogs,
            "title": f"Insights | {search} | Mostafa Ehab"
        })

    raise Http404()
    # return render(request, "errors/not-found.html", {
    #     "title": f"Insights | Page not found | Mostafa Ehab"
    # })


def author_profile(request: HttpRequest, slug: str):
    author = get_object_or_404(User, slug=slug)

    if author == request.user:
        return redirect(reverse("profile"))

    return render(request, "pages/author.html", {
        "author": author,
        "following": author in [user.followed for user in request.user.user_followed.all()],
        "title": f"Insights | {author.username}"
    })


@login_required(login_url="/login")
def profile(request: HttpRequest):
    info_form = PersonalInfoForm(instance=request.user)
    password_form = ChangePasswordForm(instance=request.user)
    image_form = ProfileImageForm(request.POST)

    if request.method == "POST":
        if request.GET.get("action") == "info":
            info_form = PersonalInfoForm(request.POST, instance=request.user)

            if info_form.is_valid():
                info_form.save()

                messages.success(request, "Saved successfully")
                return redirect(reverse("profile"))
            
        elif request.GET.get("action") == "password":
            password_form = ChangePasswordForm(request.POST, instance=request.user)

            if password_form.is_valid():
                request.user.set_password(password_form.cleaned_data.get("new_password"))
                password_form.save()

                update_session_auth_hash(request, request.user)
                messages.success(request, "Saved successfully")
                return redirect(reverse("profile"))
            
        elif request.GET.get("action") == "image":
            print(request.FILES)
            image_form = ProfileImageForm(request.POST, request.FILES)
            if image_form.is_valid():
                profile_image = request.FILES["profile_image"]
                request.user.profile_image = profile_image
                request.user.save()

                messages.success(request, "Saved successfully")
                return redirect(reverse("profile"))
            
            print(image_form.errors)
        
        messages.warning(request, "An error occured!")
        return redirect(reverse("profile"))

    return render(request, "pages/profile.html", {
        "profile_form": info_form,
        "password_form": password_form,
        "image_form": image_form,
        "title": f"Insights | {request.user.__str__()}"
    })


@login_required(login_url="/login")
def my_blogs_view(request: HttpRequest):
    queryset = request.user.author_blogs.all().order_by("-created_date")

    paginator = Paginator(queryset, 18)
    page = request.GET.get("page", 1)

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        return redirect(reverse("my_blogs"))
    except UnboundLocalError:
        return redirect(reverse("my_blogs"))

    return render(request, "pages/my_blogs.html", {
        "blogs": blogs,
        "title": "Insights | My blogs"
    })


@login_required(login_url="/login")
def add_post_view(request: HttpRequest):
    form = AddPostForm()

    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()

            tags_list = [tag.strip() for tag in request.POST.get("tags").split(",")]
            for tag in tags_list:
                if tag != "":
                    if not (tag_input := Tag.objects.filter(slug=slugify(tag)).first()):
                        print("Creating...")
                        tag_input = Tag(title = tag)
                        tag_input.save()
                
                    blog.tags.add(tag_input)

            blog.save()

            messages.success(request, "Saved successfully")
            return redirect(reverse("post", kwargs={"slug": blog.slug}))

        print(form.errors)

    return render(request, "pages/add_post.html", {
        "form": form,
        "title": "Insights | Add post"
    })

@login_required(login_url="/login")
def edit_post_view(request: HttpRequest, slug: str):
    blog = get_object_or_404(Blog, slug=slug, author=request.user)
    form = AddPostForm(instance=blog)

    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES, instance=blog)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.save()

            blog.tags.clear()
            tags_list = [tag.strip() for tag in request.POST.get("tags").split(",")]
            for tag in tags_list:
                if tag != "":
                    if not (tag_input := Tag.objects.filter(slug=slugify(tag)).first()):
                        tag_input = Tag(title = tag)
                        tag_input.save()
                
                    blog.tags.add(tag_input)

            blog.save()

            messages.success(request, "Saved successfully")
            # return redirect(reverse("post", kwargs={"slug": blog.slug}))
            return redirect(reverse("my_blogs"))

        print(form.errors)

    return render(request, "pages/edit_post.html", {
        "form": form,
        "post_tags": ",".join([tag.title for tag in blog.tags.all()]),
        "title": f"Insights | Edit: {blog.title}"
    })

@login_required(login_url="/login")
def delete_post(request: HttpRequest, slug: str):
    if request.method == "POST":
        blog = get_object_or_404(Blog, slug=slug, author=request.user)
        blog.delete()

        messages.success(request, "Deleted successfully")

    return redirect(reverse("my_blogs"))

@login_required(login_url="/login")
def add_reply(request: HttpRequest, comment_id: int):
    if request.method == "POST":
        form = ReplyForm(request.POST)

        if form.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)

            Reply.objects.create(
                text = form.cleaned_data.get("reply"),
                user = request.user,
                comment = comment
            )

            return redirect(reverse("post", kwargs={"slug": comment.blog.slug}))
        
    return redirect(reverse("home"))


@login_required(login_url="/login")
def like_post(request: HttpRequest, post_id: int):
    post = get_object_or_404(Blog, pk=post_id)

    if request.user in post.like.all():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)

    return JsonResponse({
        'liked': request.user in post.like.all(),
        'like_count': post.like.all().count(),
    })


@login_required(login_url="/login")
def follow(request: HttpRequest, user_id: int):
    print(request.user.user_followers)
    print(request.user.user_followed)
    if request.method == "POST":
        user = get_object_or_404(User, pk=user_id)

        if request.user != user:
            # Unfollow
            if follow_obj := Follow.objects.filter(
                followed = user, 
                follower = request.user
            ).first():
                follow_obj.delete()

            # Follow
            else:
                follow_obj = Follow(
                    followed = user,
                    follower = request.user
                )

                follow_obj.save()

        return redirect(reverse("author", kwargs={"slug": user.slug}))
    
    return redirect(reverse("home"))


def not_found(request: HttpRequest, exception=None):
    return render(request, "errors/not-found.html")

