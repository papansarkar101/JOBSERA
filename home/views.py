import requests
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models


# Create your views here.
def home(request):
    return render(request, 'index.html')


def search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    send_searches_to_frontend = {
        'search': search,
    }
    return render(request, 'search.html')