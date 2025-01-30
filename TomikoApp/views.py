from django.shortcuts import render
from django.http import HttpResponse
from .forms import FeedbackForm
from .models import Feedback
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
            review["name"] = review.get("name", "Аноним")
            print(review["name"], review["date"], key)
            review["grade"] = int(review.get("grade", 0))# Подставляем "Аноним", если имени нет
            reviews.append(review)

    return reviews

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
    t = len(reviews)
    middle = round(sum(float(review.get("grade", 0)) for review in reviews) / t if t > 0 else 0, 1)
    clips = get_clips()
    return render(request, "home.html", {"reviews": reviews, "clips": clips, "middle": middle})

# Create your views here.
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():  # Обработка данных только при валидной форме
            # Достаём данные формы
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']

            # Сохраняем данные в базу
            Feedback.objects.create(name=name, phone=phone, message=message)

            # Очищаем форму после успешной отправки
            form = FeedbackForm()

            # Возвращаем сообщение об успешной отправке
            return render(request, 'feedback.html', {'form': form, 'success': True})
        else:
            # Если форма невалидна, отображаем её с ошибками
            return render(request, 'feedback.html', {'form': form})
    else:
        # Отображаем пустую форму для GET-запроса
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form})

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

def about(request):
    return render(request, 'about.html')

def custom_404(request):
    return render(request, 'custom_404.html')