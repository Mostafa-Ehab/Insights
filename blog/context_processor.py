from .models import *

def get_sidebar(request):
    categories = Category.objects.all()
    posts = Blog.objects.order_by("-created_date")[:5]
    tags = Tag.objects.all()

    return {
        "all_categories": categories,
        "recent_posts": posts,
        "all_tags": tags
    }
