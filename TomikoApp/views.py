from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Hello Lexa, а макс хуй')

def mainPage(request):
    return render(request, "mainPage.html")