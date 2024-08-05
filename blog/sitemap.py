from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Blog, Category, Tag
from user_profile.models import User

class Site:
    domain = "insights.mostafa-ehab.com"
    name = "insights.mostafa-ehab.com"

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.8

    def get_urls(self, site=None, **kwargs):
        return super(BlogSitemap, self).get_urls(site=Site(), **kwargs)

    def items(self):
        return Blog.objects.order_by("-id")

    def lastmod(self, obj):
        return obj.created_date
    
    def location(self, obj: Blog) -> str:
        return reverse("post", kwargs={"slug": obj.slug})


class CategorySiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def get_urls(self, site=None, **kwargs):
        return super(CategorySiteMap, self).get_urls(site=Site(), **kwargs)

    def items(self):
        return Category.objects.order_by("-id")
    
    def location(self, obj: Category) -> str:
        return reverse("category", kwargs={"slug": obj.slug})
    
    
class TagSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def get_urls(self, site=None, **kwargs):
        return super(TagSiteMap, self).get_urls(site=Site(), **kwargs)

    def items(self):
        return Tag.objects.order_by("-id")
    
    def location(self, obj: Tag) -> str:
        return reverse("tag", kwargs={"slug": obj.slug})
    

class AuthorSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def get_urls(self, site=None, **kwargs):
        return super(AuthorSiteMap, self).get_urls(site=Site(), **kwargs)

    def items(self):
        return User.objects.exclude(author_blogs=None).order_by("-id")
    
    def location(self, obj: User) -> str:
        return reverse("author", kwargs={"slug": obj.slug})


class HomePageSiteMap(Sitemap):
    priority = 0.9
    changefreq = "daily"

    def get_urls(self, site=None, **kwargs):
        return super(HomePageSiteMap, self).get_urls(site=Site(), **kwargs)

    def items(self):
        return ["home", "blogs"]

    def location(self, item):
        return reverse(item)
    

class StaticPageSiteMap(Sitemap):
    priority = 0.3
    changefreq = "monthly"

    def get_urls(self, site=None, **kwargs):
        return super(StaticPageSiteMap, self).get_urls(site=Site(), **kwargs)

    def items(self):
        return ["about"]

    def location(self, item):
        return reverse(item)
    

sitemaps = {
    "home": HomePageSiteMap,
    "authors": AuthorSiteMap,
    "blogs": BlogSitemap,
    "categories": CategorySiteMap,
    "tags": TagSiteMap,
    "static": StaticPageSiteMap,
}

