from django.shortcuts import render, get_object_or_404
from .models import NewsItem, AiTool
import requests
import os
import re
import feedparser
from datetime import datetime, timezone
from django.http import HttpResponse, HttpResponseForbidden
from django.core.management import call_command
from .ai_client import get_explanation


# ─── RSS feeds ───────────────────────────────────────────────────────────────
AI_RSS_FEEDS = [
    {'url': 'https://techcrunch.com/category/artificial-intelligence/feed/', 'source': 'TechCrunch'},
    {'url': 'https://venturebeat.com/category/ai/feed/', 'source': 'VentureBeat'},
    {'url': 'https://www.theverge.com/rss/ai-artificial-intelligence/index.xml', 'source': 'The Verge'},
    {'url': 'https://feeds.arstechnica.com/arstechnica/technology-lab', 'source': 'Ars Technica'},
    {'url': 'https://www.wired.com/feed/category/artificial-intelligence/latest/rss', 'source': 'Wired'},
]


def fetch_youtube_tutorial(tool_name, api_key):
    """
    Fetch the top truly-embeddable YouTube tutorial for a given tool.
    Step 1: Search for 5 candidates. Step 2: Verify embeddability via videos API.
    """
    if not api_key:
        return None
    try:
        search_params = {
            'part': 'snippet',
            'q': f"{tool_name} tutorial",
            'maxResults': 5,
            'type': 'video',
            'relevanceLanguage': 'en',
            'videoDuration': 'medium',
            'videoEmbeddable': 'true',
            'key': api_key,
        }
        search_resp = requests.get(
            "https://www.googleapis.com/youtube/v3/search",
            params=search_params, timeout=5
        )
        search_data = search_resp.json()
        if 'items' not in search_data or not search_data['items']:
            return None

        video_ids = [item['id']['videoId'] for item in search_data['items']]

        verify_resp = requests.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={'part': 'status,snippet', 'id': ','.join(video_ids), 'key': api_key},
            timeout=5
        )
        verify_data = verify_resp.json()

        for video in verify_data.get('items', []):
            if video.get('status', {}).get('embeddable', False):
                snippet = video['snippet']
                return {
                    'video_id':  video['id'],
                    'title':     snippet['title'],
                    'channel':   snippet['channelTitle'],
                    'thumbnail': snippet['thumbnails']['high']['url'],
                }
    except Exception as e:
        print(f"YouTube API error for '{tool_name}': {e}")
    return None


def fetch_real_time_news(search_query='', category='', api_key=''):
    """Fetch AI news from RSS feeds."""
    news_items = []
    for feed_info in AI_RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_info['url'])
            for entry in feed.entries:
                title   = entry.get('title', '')
                summary = entry.get('summary', entry.get('description', ''))
                link    = entry.get('link', '#')
                summary = re.sub(r'<[^>]+>', '', summary)
                summary = summary[:250].strip()
                if len(summary) == 250:
                    summary += '...'
                published = entry.get('published_parsed') or entry.get('updated_parsed')
                pub_date = datetime(*published[:6], tzinfo=timezone.utc) if published else datetime.now(timezone.utc)
                if search_query:
                    q = search_query.lower()
                    if q not in title.lower() and q not in summary.lower():
                        continue
                news_item = type('NewsItem', (), {
                    'title': title, 'summary': summary, 'link': link,
                    'published_date': pub_date,
                    'source': type('Source', (), {'name': feed_info['source']})(),
                    'id': abs(hash(title)) % 100000,
                })()
                news_items.append(news_item)
                if len(news_items) >= 15:
                    break
        except Exception as e:
            print(f"RSS feed error ({feed_info['source']}): {e}")
            continue
        if len(news_items) >= 15:
            break
    news_items.sort(key=lambda x: x.published_date, reverse=True)
    return news_items


def create_sample_news():
    from datetime import timedelta
    sample_articles = [
        {'title': 'OpenAI Releases GPT-4 Turbo with Enhanced Reasoning', 'summary': 'OpenAI announced a major update to GPT-4 Turbo featuring improved reasoning and faster response times.', 'source': 'TechCrunch', 'link': 'https://techcrunch.com', 'date': datetime.now() - timedelta(hours=2)},
        {'title': 'Google DeepMind Unveils Breakthrough in AI Protein Folding', 'summary': 'Researchers at DeepMind announced a new system that predicts protein structures with unprecedented accuracy.', 'source': 'Nature', 'link': 'https://nature.com', 'date': datetime.now() - timedelta(hours=5)},
        {'title': 'Microsoft Copilot Integration Expands to Enterprise', 'summary': 'Microsoft expanded Copilot across its enterprise suite with AI assistance for Excel, PowerPoint, and Teams.', 'source': 'Microsoft Blog', 'link': 'https://blogs.microsoft.com', 'date': datetime.now() - timedelta(hours=8)},
    ]
    news_items = []
    for i, a in enumerate(sample_articles):
        news_items.append(type('NewsItem', (), {
            'title': a['title'], 'summary': a['summary'], 'link': a['link'],
            'published_date': a['date'],
            'source': type('Source', (), {'name': a['source']})(),
            'id': i + 1000,
        })())
    return news_items


def home_view(request):
    try:
        latest_news = fetch_real_time_news()[:3]
        if len(latest_news) < 2:
            db_news = list(NewsItem.objects.all().order_by('-published_date')[:3])
            latest_news = db_news if db_news else create_sample_news()[:3]
    except:
        latest_news = create_sample_news()[:3]

    latest_tools = AiTool.objects.all().order_by('-added_date')[:5]
    conversation_history = request.session.get('ai_conversation', [])

    if request.method == 'POST':
        if request.POST.get('clear_history'):
            request.session['ai_conversation'] = []
            conversation_history = []
        else:
            ai_query = request.POST.get('ai_query')
            if ai_query:
                ai_response = get_explanation(ai_query)
                conversation_history.append({
                    'query': ai_query,
                    'response': ai_response,
                    'timestamp': datetime.now().strftime('%H:%M')
                })
                if len(conversation_history) > 5:
                    conversation_history = conversation_history[-5:]
                request.session['ai_conversation'] = conversation_history

    return render(request, 'home.html', {
        'latest_news': latest_news,
        'latest_tools': latest_tools,
        'conversation_history': conversation_history,
        'news_count': len(latest_news),
    })


def news_list_view(request):
    search_query  = request.GET.get('search', '')
    category      = request.GET.get('category', '')
    error_message = None
    news_source   = "rss"

    try:
        news_items = fetch_real_time_news(search_query, category)
        if not news_items:
            news_items = create_sample_news()
            news_source = "sample"
            error_message = "Could not load RSS feeds. Showing sample articles."
    except Exception as e:
        print(f"News fetch error: {e}")
        news_items = create_sample_news()
        news_source = "sample"
        error_message = "Could not load news feeds right now."

    return render(request, 'curator_app/news_list.html', {
        'news_items': news_items,
        'page_title': 'All AI News',
        'search_query': search_query,
        'category': category,
        'error_message': error_message,
        'news_source': news_source,
        'news_count': len(news_items),
    })


def tool_list_view(request):
    ai_tools     = AiTool.objects.all()
    search_query = request.GET.get('search', '')
    category     = request.GET.get('category', '')
    sort_order   = request.GET.get('sort', 'name')

    if search_query:
        ai_tools = ai_tools.filter(name__icontains=search_query)
    if category:
        ai_tools = ai_tools.filter(category=category)

    sort_map = {'-name': '-name', 'popular': '-id', 'recent': '-added_date'}
    ai_tools = ai_tools.order_by(sort_map.get(sort_order, 'name'))

    return render(request, 'curator_app/tool_list.html', {
        'ai_tools': ai_tools,
        'page_title': 'All AI Tools & Products',
        'search_query': search_query,
        'category': category,
        'sort_order': sort_order,
    })


def tool_detail_view(request, pk):
    tool        = get_object_or_404(AiTool, pk=pk)
    explanation = None

    # Fetch embeddable YouTube tutorial on every page load
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    youtube = fetch_youtube_tutorial(tool.name, youtube_api_key) if youtube_api_key else None

    if request.method == 'POST':
        query = tool.perplexity_query
        if not query:
            query = f"Explain what {tool.name} is, what it does, and who it's most useful for."
            if tool.description:
                query += f" Here's a brief description: {tool.description}"
        explanation = get_explanation(query)

    return render(request, 'curator_app/tool_detail.html', {
        'tool': tool,
        'explanation': explanation,
        'youtube': youtube,
    })


def trigger_fetch_news_view(request, secret):
    if secret != os.environ.get('CRON_SECRET'):
        return HttpResponseForbidden('Invalid secret.')
    try:
        call_command('fetch_news')
        return HttpResponse('News fetch triggered successfully.')
    except Exception as e:
        return HttpResponse(f'Error: {e}', status=500)
    
def article_detail_view(request):
    """Article detail page with Gemini 'Why This Matters' summary."""
    title   = request.GET.get('title', '')
    summary = request.GET.get('summary', '')
    source  = request.GET.get('source', '')
    link    = request.GET.get('link', '#')
    pub_ago = request.GET.get('pub_ago', '')

    why_it_matters = None
    error = None

    if title:
        try:
            prompt = (
                f"You are an AI analyst writing for developers and tech professionals. "
                f"Given the article title and summary below, write a 'Why This Matters' "
                f"explanation in exactly 3 clear, insightful sentences. Be specific — "
                f"explain the real-world impact, who is affected, and why this development "
                f"is significant right now. Do not be generic. Do not start with 'This article'.\n\n"
                f"Title: {title}\n"
                f"Summary: {summary}"
            )
            why_it_matters = get_explanation(prompt)
        except Exception as e:
            error = str(e)

    return render(request, 'curator_app/article_detail.html', {
        'title':          title,
        'summary':        summary,
        'source':         source,
        'link':           link,
        'pub_ago':        pub_ago,
        'why_it_matters': why_it_matters,
        'error':          error,
    })