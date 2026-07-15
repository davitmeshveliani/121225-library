from django.shortcuts import render
from django.http import HttpResponse

from apps.library.models import Book


# Create your views here.
def index(request):
    x = Book.objects.last()
    print(x)
    return HttpResponse("Hello, world. You're at the library index.")