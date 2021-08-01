import random
import string
import django.contrib.auth.models as AuthModels
from django.contrib.contenttypes.models import ContentType
from SearchEngine.models import RegVerify
from django.core.mail import send_mail
import SearchEngine

def sendMail(email):
    code = ''.join(random.sample(
            string.ascii_letters + string.digits, 20))
    verifyEntry = RegVerify.RegVerify(email=email, code=code)
    verifyEntry.save()

    message = '''Hi There,
    
    Thanks for creating an account for this site!
    Please verify your email address by clicking the link below.
    The link would be expired in 10 minutes.
    
    http://localhost:8000/signup/{code}/
    
Best wishes,
c7w

    '''.replace('{code}', code)
    
    send_mail("Welcome to SASTSearchEngine Site! | No Reply", message, 'SAST_SearchEngine@cc7w.cf', [email])

def verifyCode(code):
    try:
        record = RegVerify.RegVerify.objects.get(code=code)
        permission = AuthModels.Permission.objects.get(codename='EmailVerified')
        AuthModels.User.objects.get(username=record.email).user_permissions.add(permission)
        RegVerify.RegVerify.objects.delete(code=code)
        return True
    except:
        return False
