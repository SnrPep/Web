from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import redis
import json
import itertools

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

def get_reviews():
    reviews = []
    keys = itertools.chain(
        redis_client.scan_iter("2Gis_review:*"),
        redis_client.scan_iter("VL_review:*"),
        redis_client.scan_iter("Yandex_review:*")
    )
    for key in keys:
        data = redis_client.get(key)
        if data:
            review = json.loads(data)
            reviews.append(review)

    return reviews[:10]  # Ограничим число отзывов

def get_clips():
    clips = []
    keys = itertools.chain(
        redis_client.scan_iter("VK_clip:*")
    )
    for key in keys:
        data = redis_client.get(key)
        if data:
            clip = json.loads(data)
            clips.append(clip)

    return clips  # Ограничим число отзывов


def home_view(request):
    reviews = get_reviews()
    clips = get_clips()
    return render(request, "home.html", {"reviews": reviews, "clips": clips})

# Create your views here.

# Create your views here.
def home(request):
    """homepage of learning logs"""
    return render(request, 'home.html')

def economy(request):
    return render(request, 'economy.html')

def catalog(request):
    return render(request, 'catalog.html')

def card(request):
    return render(request, 'card.html')

def contacts(request):
    return render(request, 'contacts.html')

def politicy(request):
    return render(request, 'politicy.html')

def akcii(request):
    return render(request, 'akcii.html')