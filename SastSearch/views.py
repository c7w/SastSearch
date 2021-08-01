from django.http import HttpResponse
from django.shortcuts import render
import random, string
from SearchEngine.models import RegVerify

# Create your views here.
def index(req):
    return render(req, "search/index.html")

def news(req):
    return render(req, "search/detail.html")

def signup(req):
    print(req)
    if req.method == "GET":
        return render(req, "search/signup.html")
    if req.method == "POST":
        email = req.POST['email']
        password = req.POST['password']
        password_repeat = req.POST['password_repeat']
        if password != password_repeat:
            return render(req, "search/signup.html", {"message": '<div class="alert alert-warning" style="font-size: 50%"> {ERROR MESSAGE} </div>'.replace("{ERROR MESSAGE}", "The repeated password didn't match.")})
        code = ''.join(random.sample(string.ascii_letters + string.digits, 20))
        print(email)
        verifyEntry = RegVerify.RegVerify(email=email, code=code)
        verifyEntry.save()
        return render(req, "search/signup.html")

def signup_verify(req, code):
    return HttpResponse(code)
