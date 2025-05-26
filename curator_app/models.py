from django.db import models
from django.utils import timezone

# Python's Next Top Models

class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True, help_text="URL-friendly version of the name. Auto-Generated if left blank.")

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class NewsSource(models.Model):
    name = models.CharField(max_length=200)
    rss_url = models.URLField(unique=True, help_text="The URL of the RSS feed.")
    website_url = models.URLField(blank=True, null=True, help_text="The main website URL (optional).")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="news_sources")
    last_fetched = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class NewsItem(models.Model):
    title = models.CharField(max_length=300)
    link = models.URLField(unique=True)
    summary = models.TextField(blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    fetched_date = models.DateTimeField(default=timezone.now)
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE, related_name="news_items")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="news_items")

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_date', '-fetched_date']

class AiTool(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    link = models.URLField(help_text="Link to the tool's official website or page.")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="ai_tools")
    documentation_link = models.URLField(blank=True, null=True)
    tutorial_link = models.URLField(blank=True, null=True)
    added_date = models.DateTimeField(default=timezone.now)

    # Predefined question for Perplexity API about the tool
    perplexity_query = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="A specific question to ask Perplexity about this tool (e.g. 'What is [Tool Name] and how does it work?')."
    )

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-added_date']

