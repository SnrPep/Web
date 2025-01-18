from django.shortcuts import render
from django.http import HttpResponse
from .forms import FeedbackForm

from .models import Feedback



# Create your views here.
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Здесь можно обработать данные формы, например, сохранить их в базу или отправить на почту
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            # Пример сохранения данных:
            # Feedback.objects.create(name=name, phone=phone, message=message)
            return HttpResponse("Спасибо за ваш отзыв!")
    else:
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