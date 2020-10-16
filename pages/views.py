import json

from django.contrib.auth.models import User 
from django.http import JsonResponse
from django.shortcuts import render
from pages.models import Node, Exams

def categories(request):
    root = Node.objects.first()
    categories = root.get_descendants()
    serialized = [{'id': c.pk, 'name': c.name, 'text': c.name} for c in categories]
    data = json.dumps(serialized)
    return JsonResponse(data)
