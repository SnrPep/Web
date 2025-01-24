from django.shortcuts import render
from django.http import HttpResponse
from .forms import FeedbackForm

from .models import Feedback



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