from django.contrib import admin
from .models import Category, NewsSource, NewsItem, AiTool

# Python's Next Top Models II
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'rss_url', 'website_url', 'category', 'last_fetched')
    list_filter = ('category',)
    search_fields = ('name', 'rss_url')

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'category', 'published_date', 'fetched_date')
    list_filter = ('category', 'source', 'published_date')
    search_fields = ('title', 'summary', 'link')
    date_hierarchy = 'published_date'

@admin.register(AiTool)
class AiToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'link', 'added_date', 'perplexity_query')
    list_filter = ('category',)
    search_fields = ('name', 'description')