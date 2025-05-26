import feedparser
from dateutil import parser as date_parser
from django.core.management.base import BaseCommand
from django.utils import timezone
from curator_app.models import NewsSource, NewsItem, Category

class Command(BaseCommand):
    help = 'Fetches new news items from all registered RSS feeds.'

    def handle(self, *args, **kwargs):
        """
        The main logic of the command.
        """
        self.stdout.write(self.style.SUCCESS('Starting news fetch process...'))
        
        sources = NewsSource.objects.all()
        if not sources:
            self.stdout.write(self.style.WARNING('No news sources found in the database. Please add some via the admin panel.'))
            return

        total_new_items = 0
        for source in sources:
            self.stdout.write(f'Fetching news from: {source.name}')
            
            # Parse RSS feed URL
            feed = feedparser.parse(source.rss_url)

            items_from_this_source = 0
            for entry in feed.entries:
                # Check if news item exists, avoid duplicates
                if NewsItem.objects.filter(link=entry.link).exists():
                    continue

                # Parse publication date
                published_date = timezone.now() # Default if it fails
                if hasattr(entry, 'published'):
                    try:
                        published_date = date_parser.parse(entry.published)
                    except date_parser.ParserError:
                        self.stdout.write(self.style.WARNING(f"Could not parse date '{entry.published}' for item '{entry.title}'"))
                
                # Create NewsItem object
                try:
                    NewsItem.objects.create(
                        title=entry.title,
                        link=entry.link,
                        summary=entry.get('summary', ''), 
                        published_date=published_date,
                        source=source,
                        category=source.category
                    )
                    items_from_this_source += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error saving item '{entry.title}': {e}"))

            if items_from_this_source > 0:
                self.stdout.write(self.style.SUCCESS(f'--> Found and saved {items_from_this_source} new items from {source.name}'))
                total_new_items += items_from_this_source
            
            # Update last_fetched timestamp for source
            source.last_fetched = timezone.now()
            source.save()

        self.stdout.write(self.style.SUCCESS(f'\nNews fetch process complete. Total new items saved: {total_new_items}'))