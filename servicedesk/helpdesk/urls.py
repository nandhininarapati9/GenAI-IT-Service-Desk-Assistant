from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'dashboard/',
        views.incident_list,
        name='incident_list'
    ),

    path(
        'create/',
        views.create_incident,
        name='create_incident'
    ),

    path(
        'knowledge/',
        views.knowledge_base,
        name='knowledge_base'
    ),

    path(
        'search/',
        views.search_knowledge,
        name='search_knowledge'
    ),

    path(
        'assistant/',
        views.ai_assistant,
        name='ai_assistant'
    ),
]