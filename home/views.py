import requests
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models

BASE_URL = "https://in.indeed.com/jobs?q={}"


# Create your views here.
def home(request):
    return render(request, 'index.html')


def search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    final_url = BASE_URL.format(quote_plus(search))

    response = requests.get(final_url)  # <Response [200]>
    data = response.text  # Everything is in data now

    soup = BeautifulSoup(data, features='html.parser')

    all_post = soup.find_all(
        'div', {'class': 'jobsearch-SerpJobCard'})  # All job posts

    final_posts = []

    for post in all_post:
        post_title = post.find(class_="title").text
        company = post.find(class_="company").text
        location = post.find(class_="location").text

        final_posts.append((post_title, company, location))

    send_searches_to_frontend = {
        'final_url': final_url,
        'search': search.title(),
        'final_posts': final_posts,
    }
    return render(request, 'search.html', send_searches_to_frontend)