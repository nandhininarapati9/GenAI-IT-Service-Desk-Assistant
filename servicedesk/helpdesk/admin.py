from django.contrib import admin
from .models import Incident, KnowledgeArticle

admin.site.register(Incident)
admin.site.register(KnowledgeArticle)