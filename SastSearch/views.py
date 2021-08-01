from django.shortcuts import  render
import django.contrib.auth.models as AuthModels
from django.contrib.auth import authenticate, login
from utils import MailVerify

# Create your views here.
def index(req):
    return render(req, "search/index.html")

def news(req):
    return render(req, "search/detail.html")

def signup(req):    
    if req.method == "GET":
        return render(req, "search/signup.html")
    if req.method == "POST":
        # Retrive data
        email = req.POST['email']
        password = req.POST['password']
        password_repeat = req.POST['password_repeat']
        if password != password_repeat:
            return render(req, "search/signup.html", {"message":  "The repeated password didn't match."})
        
        # Check if email is available
        try:
            user = AuthModels.User.objects.get(username=email)
            user = authenticate(username=email, password=password)
            if user:
                if (user.has_perm('auth.EmailVerified')):
                    return render(req, "search/signup.html", {"message": "This email address is not available.<br/><br/>Please use another email address."})
                else:
                    MailVerify.sendMail(email)
                    return render(req, "search/signup.html", {"message": "A new verification email has been sent."})
            else:
                return render(req, "search/signup.html", {"message": "This email address is not available.<br/><br/>Please check your password."})
            
        except:
            # No matching Record. Create User.
            AuthModels.User.objects.create_user(username=email, password=password)
            # Send verification email
            MailVerify.sendMail(email)
            return render(req, "search/signup.html", {"message": "An verification email has been sent."})

def signup_verify(req, code):
    if MailVerify.verifyCode(code):
        return render(req, "search/signup_feedback.html", {"message": "Your email address has been verified!", "OK": True})
    else:
        # Code not found or expired
        return render(req, "search/signup_feedback.html", {"message": "Could not verify your email address. <br/><br/>This link was invalid or expired. <br/><br/>Please sign up again with the same password.", "OK": False})

def login(req):
    if req.method == "GET":
        return render(req, "search/login.html")
    if req.method == "POST":
        return render(req, "search/login.html")