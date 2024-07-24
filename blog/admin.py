from typing import Any
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from .models import *

class CategoryBlogInline(admin.TabularInline):
    model = Blog
    extra = 0
    max_num = 0
    fields = ["title"]
    readonly_fields = ["title"]
    show_change_link = True

class TagBlogInline(admin.TabularInline):
    model = Blog.tags.through
    extra = 2

class BlogAdmin(ModelAdmin):
    exclude = ["slug", "author", "like"]
    filter_horizontal = ["tags"]

    list_display = ['title', 'created_date']

    fields = ['title', 'content', ('banner', 'show_banner'), 'category', 'tags', 'slug']

    readonly_fields = ['show_banner', 'slug']

    formfield_overrides = { 
        models.TextField: {'widget': TinyMCE()}, # optional, set Textarea attributes `attrs={'rows':2, 'cols':8}`
        # models.ImageField: {'widget': }
    }

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.author = request.user
        return super().save_model(request, obj, form, change)

class CategoryAdmin(ModelAdmin):
    exclude = ["slug"]
    list_display = ["__str__", "blogs_number"]

    inlines = [
        CategoryBlogInline
    ]

class TagAdmin(ModelAdmin):
    exclude = ["slug"]
    list_display = ["__str__", "blogs_number"]

    inlines = [
        TagBlogInline
    ]


# Register your models here.
admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)
admin.site.register(Reply)
