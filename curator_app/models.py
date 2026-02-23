from django.db import models
from django.utils import timezone


class NewsSource(models.Model):
    name = models.CharField(max_length=200)
    rss_url = models.URLField(unique=True)
    website_url = models.URLField(blank=True, null=True)
    last_fetched = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class NewsItem(models.Model):
    title = models.CharField(max_length=300)
    link = models.URLField(unique=True)
    summary = models.TextField(blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    fetched_date = models.DateTimeField(default=timezone.now)
    source_name = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date', '-fetched_date']


class AiTool(models.Model):

    CATEGORY_CHOICES = [
        ('nlp',             'NLP'),
        ('image',           'Image'),
        ('code',            'Code'),
        ('machine_learning','Machine Learning'),
        ('vision',          'Vision'),
        ('audio',           'Audio'),
    ]

    name        = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    link        = models.URLField(help_text="Official website or product page.")
    category    = models.CharField(
                    max_length=50,
                    choices=CATEGORY_CHOICES,
                    blank=True,
                    default='',
                  )
    is_featured = models.BooleanField(default=False)
    is_popular  = models.BooleanField(default=False)
    added_date  = models.DateTimeField(default=timezone.now)

    # Kept for compatibility — auto-generated in views.py if blank
    perplexity_query = models.CharField(
        max_length=500, blank=True, null=True,
        help_text="Optional custom AI query for this tool."
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-added_date']