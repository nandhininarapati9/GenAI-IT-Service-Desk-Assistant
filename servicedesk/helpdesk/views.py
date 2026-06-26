from django.shortcuts import render, redirect
from django.db.models import Q

from .forms import IncidentForm
from .models import Incident, KnowledgeArticle
from .ai_engine import (
    get_ai_response,
    categorize_incident
)


def format_solution(content):
    """
    Format solution text into readable lines.
    """

    if not content:
        return ""

    content = content.replace('\r\n', '\n')

    sentences = []

    for part in content.split('.'):
        part = part.strip()

        if part:
            sentences.append(part + '.')

    return '\n'.join(sentences)


def home(request):

    return render(
        request,
        'index.html'
    )


def create_incident(request):

    if request.method == 'POST':

        form = IncidentForm(request.POST)

        if form.is_valid():

            incident = form.save(commit=False)

            try:

                result = categorize_incident(
                    incident.title,
                    incident.description
                )

                category = "Software"
                priority = "Medium"

                for line in result.splitlines():

                    if line.startswith("Category:"):
                        category = line.replace(
                            "Category:",
                            ""
                        ).strip()

                    elif line.startswith("Priority:"):
                        priority = line.replace(
                            "Priority:",
                            ""
                        ).strip()

                incident.category = category
                incident.priority = priority

            except Exception:

                incident.category = "Software"
                incident.priority = "Medium"

            incident.save()

            return redirect(
                'incident_list'
            )

    else:

        form = IncidentForm()

    return render(
        request,
        'incident_form.html',
        {
            'form': form
        }
    )


def incident_list(request):

    incidents = Incident.objects.all()

    total_incidents = incidents.count()

    open_incidents = incidents.filter(
        status='Open'
    ).count()

    solved_incidents = incidents.filter(
        status='Solved'
    ).count()

    total_articles = KnowledgeArticle.objects.count()

    return render(
        request,
        'incident_list.html',
        {
            'incidents': incidents,
            'total_incidents': total_incidents,
            'open_incidents': open_incidents,
            'solved_incidents': solved_incidents,
            'total_articles': total_articles,
        }
    )


def knowledge_base(request):

    articles = KnowledgeArticle.objects.all()

    for article in articles:

        article.formatted_content = format_solution(
            article.content
        )

    return render(
        request,
        'knowledge_base.html',
        {
            'articles': articles
        }
    )


def search_knowledge(request):

    query = request.GET.get('q', '')

    articles = []

    if query:

        articles = KnowledgeArticle.objects.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query) |
            Q(content__icontains=query)
        )

        for article in articles:

            article.formatted_content = format_solution(
                article.content
            )

    return render(
        request,
        'search_knowledge.html',
        {
            'articles': articles,
            'query': query
        }
    )



def ai_assistant(request):

    context = {}

    if request.method == "POST":

        issue = request.POST.get("query")

        try:
            # Get response from Ollama
            response = get_ai_response(issue)

            # Get category from Ollama
            try:
                category = categorize_incident(issue)
            except Exception:
                category = "General"

            context = {
                "response": response,
                "category": category,
                "source": "Ollama AI",
                "issue": issue,
                "success": True
            }

        except Exception as e:

            context = {
                "error": str(e),
                "issue": issue,
                "success": False
            }

    return render(
        request,
        "ai_assistant.html",
        context
    )