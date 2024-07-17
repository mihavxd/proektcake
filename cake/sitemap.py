from django.contrib.sitemaps import Sitemap
from .models import Post
from django.shortcuts import reverse


class StaticViewsSitemap(Sitemap):
    def items(self):
        return ['home', 'contactforms', 'dostavka']

    def location(self, item):
        return reverse(item)


class DynamicViewsSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.created_at

