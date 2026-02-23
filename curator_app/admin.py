from django.contrib import admin
from .models import NewsSource, NewsItem, AiTool


@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'rss_url', 'website_url', 'last_fetched')
    search_fields = ('name', 'rss_url')


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'source_name', 'published_date', 'fetched_date')
    list_filter = ('source_name', 'published_date')
    search_fields = ('title', 'summary', 'link')
    date_hierarchy = 'published_date'


@admin.register(AiTool)
class AiToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_featured', 'is_popular', 'added_date')
    list_filter = ('category', 'is_featured', 'is_popular')
    search_fields = ('name', 'description')