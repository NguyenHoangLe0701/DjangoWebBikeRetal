from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from app_admin.models import Article, Bike, Store

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'home',
            'bike-rental',
            'map',
            'weather',
            'dich-vu',
            'khuyen-mai',
            'giai-phap-xe-dap-qua-tang-doanh-nghiep',
        ]

    def location(self, item):
        return reverse(item)

class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Article.objects.filter(publish_date__isnull=False).order_by('-publish_date')

    def lastmod(self, obj):
        return obj.publish_date

class BikeSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Bike.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

class StoreSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Store.objects.all()

