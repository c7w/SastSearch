import time, math, datetime
from django.http.response import HttpResponse, HttpResponseNotFound
from SearchEngine.models.RegVerify import RegVerify, PassReset
from SearchEngine.models.Search import SearchRecord, News
from django.shortcuts import  redirect, render
import django.contrib.auth.models as AuthModels
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from utils import DataManager, GeneralProperty, MailVerify, Search
from django.db.models import Q
from django.utils import timezone

# Create your views here.
def index(req):
    return render(req, "search/index.html", GeneralProperty.getProps(req, "Index"))

def news(req):
    props = GeneralProperty.getProps(req, "News")
    id = str(req.GET.get("id", "0"))
    highlight = req.GET.get("highlight", "")
    try:
        news = News.objects.get(id=id)
        props['title'] = news.title + " | SAST Search"
        props['article'] = {}
        props['article']['title'] = news.title
        props['article']['source'] = news.source
        # props['article']['time'] = news.time.strftime("%Y-%m-%d %H:%M:%S")
        props['article']['time'] = news.time
        props['article']['content'] = news.content.replace("\xa0", " ").replace("\t", " ").replace("\r", "\n").replace(" ", "&nbsp;").split("\n")
        if highlight != "":
            props['article']['title'] = news.title.replace(
                highlight, "<span style='background-color: yellow'>" + highlight + "</span>")
            props['article']['content'] = map(lambda section: section.replace(
                highlight, "<span style='background-color: yellow'>" + highlight + "</span>"), props['article']['content'])
        return render(req, "search/detail.html", props)
    except:
        return HttpResponseNotFound()
        
def signup(req):    
    props = GeneralProperty.getProps(req, "SignUp")
    if req.method == "GET":
        return render(req, "search/signup.html", props)
    if req.method == "POST":
        # Retrieve data
        email = req.POST['email']
        password = req.POST['password']
        password_repeat = req.POST['password_repeat']
        if password != password_repeat:
            props['message'] = "The repeated password didn't match."
            return render(req, "search/signup.html", props)
        
        # Check if email is available
        try:
            user = AuthModels.User.objects.get(username=email)
            user = authenticate(username=email, password=password)
            if user:
                if (user.has_perm('auth.EmailVerified')):
                    props['message'] = "This email address is not available.<br/><br/>Please use another email address."
                    return render(req, "search/signup.html", props)
                else:
                    MailVerify.sendMail(email)
                    props["message"] = "A new verification email has been sent."
                    return render(req, "search/signup.html", props)
            else:
                props["message"] = "This email address is not available.<br/><br/>Please check your password."
                return render(req, "search/signup.html", props)
            
        except:
            # No matching Record. Create User.
            AuthModels.User.objects.create_user(username=email, password=password)
            # Send verification email
            MailVerify.sendMail(email)
            props["message"] = "An verification email has been sent."
            return render(req, "search/signup.html", props)

def signup_verify(req, code):
    props = GeneralProperty.getProps(req, "Email Verification")
    if MailVerify.verifyCode(code):
        props['message'] = "Your email address has been verified!"
        return render(req, "search/signup_feedback.html", props)
    else:
        # Code not found or expired
        props['message'] = "Could not verify your email address. <br/><br/>This link was invalid or expired. <br/><br/>Please sign up again with the same password."
        return render(req, "search/signup_feedback.html", props)

def login(req):
    props = GeneralProperty.getProps(req, "Login")
    if req.method == "GET":
        return render(req, "search/login.html", props)
    if req.method == "POST":
        # Retrieve data
        email = req.POST['email']
        password = req.POST['password']
        
        # Check if email is available
        try:
            user = AuthModels.User.objects.get(username=email)
            user = authenticate(username=email, password=password)
            if user:
                if (user.has_perm('auth.EmailVerified')):
                    # Login success.
                    auth_login(req, user)
                    return redirect("/")
                else:
                    # Email address was not verified.
                    props['message'] =  "Email address has not been verified."
                    return render(req, "search/login.html", props)
            else:
                # Login failed. Password did not match.
                props["message"] = "Login failed. Invalid password."
                return render(req, "search/login.html", props)

        except:
            # No matching Record. Return.
            props["message"] = "Email address has not been registered."
            return render(req, "search/login.html", props)

def logout(req):
    auth_logout(req)
    return redirect("/")

def reset_password(req):
    props = GeneralProperty.getProps(req, "Reset")
    if req.method == 'GET':
        props['email_input'] = True
        return render(req, "search/reset_password.html", props)
    if req.method == 'POST':
        email = req.POST.get("email")
        password = req.POST.get("password")
        try:
            user = AuthModels.User.objects.get(username=email)
            MailVerify.sendResetMail(email)
            props['message'] = "An email has been sent for resetting your password."
            return render(req, "search/reset_password.html", props)
        except:
            # No Matching Records for this email.
            props['message'] = "No matching email was found."
            props['email_input'] = True
            return render(req, "search/reset_password.html", props)
        
def reset_password_verify(req, code):
    props = GeneralProperty.getProps(req, "Reset")
    if req.method == "GET":
        try:
            email = PassReset.objects.get(code=code).email
            props['message'] = "Resetting password for:<br/>"+email
            props['password_reset'] = True
            return render(req, "search/reset_password.html", props)
        except:
            # No matching Records
            props['message'] = "The link was invalid or expired."
            return render(req, "search/reset_password.html", props)
    if req.method == "POST":
        # Retrieve data
        email = PassReset.objects.get(code=code).email
        password = req.POST['password']
        password_repeat = req.POST['password_repeat']
        
        if password != password_repeat:
            props['message'] = "The repeated password didn't match."
            props['password_reset'] = True
            return render(req, "search/reset_password.html", props)
        else:
            # Reset password for user
            user = AuthModels.User.objects.get(username=email)
            user.set_password(password)
            user.save()
            PassReset.objects.get(code=code).delete()
            return redirect("/")

def process_data(req):
    return DataManager.ProcessData()

def search(req):
    props = GeneralProperty.getProps(req, "Result")
    if props['login']['success'] == '0':
        return redirect("/login")
    query = req.GET.get("q")
    fuzzy = req.GET.get("fuzzy", "disabled")
    page = int(req.GET.get("page", "1"))
    
    new_record = SearchRecord(email=props['login']['email'], record=query, fuzzy=(fuzzy!="disabled"),\
                              time=timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone()))
    new_record.save()
    
    return Search.SearchNews(req, query, fuzzy, page, props)
