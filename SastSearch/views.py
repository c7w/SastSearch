from django.shortcuts import  redirect, render
import django.contrib.auth.models as AuthModels
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from utils import MailVerify
from utils import GeneralProperty

# Create your views here.
def index(req):
    return render(req, "search/index.html", GeneralProperty.getProps(req, "Index"))

def news(req):
    raise NotImplementedError
    # return render(req, "search/detail.html", GeneralProperty.getProps(req, "News"))

def signup(req):    
    props = GeneralProperty.getProps(req, "SignUp")
    if req.method == "GET":
        return render(req, "search/signup.html", props)
    if req.method == "POST":
        # Retrive data
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
        # Retrive data
        email = req.POST['email']
        password = req.POST['password']
        
        # Check if email is available
        try:
            user = AuthModels.User.objects.get(username=email)
            user = authenticate(username=email, password=password)
            if user:
                if (user.has_perm('auth.EmailVerified')):
                    # Login success.
                    print(user)
                    auth_login(req, user)
                    return redirect("/")
                else:
                    # Email address was not verified.
                    props['message'] =  "Email address has not been verified."
                    return render(req, "search/login.html")
            else:
                # Login failed. Password did not match.
                props["message"] = "Login failed. Invalid password."
                return render(req, "search/login.html")

        except:
            # No matching Record. Return.
            props["message"] = "Email address has not been registered."
            return render(req, "search/login.html")

def logout(req):
    pass