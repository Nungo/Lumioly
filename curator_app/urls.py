from django.urls import path
from . import views

app_name = 'curator_app'

urlpatterns = [
    path('news/', views.news_list_view, name='news_list'),
    path('tools/', views.tool_list_view, name='tool_list'),
    path('tools/<int:pk>/', views.tool_detail_view, name='tool_detail'),
    path(f'tasks/fetch-news/<str:secret>/', views.trigger_fetch_news_view, name='trigger_fetch_news'),
]