from django.shortcuts import render, get_object_or_404
from .models import NewsItem, AiTool, Category

# Gemini client function
from .ai_client import get_explanation

import os
from django.http import HttpResponse, HttpResponseForbidden
from django.core.management import call_command


# Better views than Cape Town

def home_view(request):
    """
    View for the homepage.
    Fetches the 5 most recent news items and 5 most recent AI tools.
    """
    latest_news = NewsItem.objects.all().order_by('-published_date', '-fetched_date')[:5]
    latest_tools = AiTool.objects.all().order_by('-added_date')[:5]
    
    context = {
        'latest_news': latest_news,
        'latest_tools': latest_tools,
    }
    return render(request, 'home.html', context)

def news_list_view(request):
    """
    View to display a full list of all news items, ordered by date.
    """
    news_items = NewsItem.objects.all()
    context = {
        'news_items': news_items,
        'page_title': 'All AI News'
    }
    return render(request, 'curator_app/news_list.html', context)

def tool_list_view(request):
    """
    View to display a full list of all AI tools.
    """
    ai_tools = AiTool.objects.all()
    context = {
        'ai_tools': ai_tools,
        'page_title': 'All AI Tools & Products'
    }
    return render(request, 'curator_app/tool_list.html', context)

def tool_detail_view(request, pk):
    """
    View to display details for a single AI tool and handle AI explanation requests.
    """
    tool = get_object_or_404(AiTool, pk=pk)
    explanation = None

    # Form submission when user clicks "Ask AI" button
    if request.method == 'POST':
        query = tool.perplexity_query
        if query:
            # Call ai_client function to get AI response
            explanation = get_explanation(query)
        else:
            explanation = "No specific query is configured for this tool in the admin panel."

    context = {
        'tool': tool,
        'explanation': explanation,
    }
    return render(request, 'curator_app/tool_detail.html', context)

def trigger_fetch_news_view(request, secret):
    """
    A secure view to trigger the fetch_news management command.
    """
    # Ensure valid credentials
    if secret != os.environ.get('CRON_SECRET'):
        # If they don't match - 'Forbidden' error
        return HttpResponseForbidden('Invalid secret.')

    try:
        print("Cron job triggered: Fetching news...")
        call_command('fetch_news')
        print("Cron job finished successfully.")
        return HttpResponse('News fetch command triggered successfully.')
    except Exception as e:
        # Log errors and throw error response
        print(f"Error running fetch_news command via cron: {e}")
        return HttpResponse(f'Error triggering command: {e}', status=500)