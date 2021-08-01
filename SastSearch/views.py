from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(req):
    return HttpResponse("HWD!")

def news(req):
    return render(req, "search/detail.html")

def signup(req):
    return render(req, "search/signup.html")