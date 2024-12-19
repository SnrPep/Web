from django.shortcuts import render
from django.http import HttpResponse

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