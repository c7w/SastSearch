import random
import string
import django.contrib.auth.models as AuthModels
from django.contrib.contenttypes.models import ContentType
from SearchEngine.models import RegVerify
from django.core.mail import send_mail
import SearchEngine

BASE_URL = 'http://121.5.165.232:10086'

def sendMail(email):
    code = ''.join(random.sample(
            string.ascii_letters + string.digits, 20))
    verifyEntry = RegVerify.RegVerify(email=email, code=code)
    verifyEntry.save()

    message = '''Hi There,
    
    Thanks for creating an account for this site!
    Please verify your email address by clicking the link below.
    The link would be expired in 10 minutes.
    
    {BASE}/signup/{code}/
    
Best wishes,
c7w

    '''.replace('{code}', code).replace('{BASE}', BASE_URL)
    
    send_mail("Welcome to SASTSearchEngine Site! | No Reply", message, 'SAST_SearchEngine@cc7w.cf', [email])
    
def sendResetMail(email):
    code = ''.join(random.sample(
            string.ascii_letters + string.digits, 20))
    verifyEntry = RegVerify.PassReset(email=email, code=code)
    verifyEntry.save()

    message = '''Hi There,
    
    The email was sent for resetting your password on SAST Search Site.
    Please ignore this email if you had not requested a password reset.
    
    Please click the link below to reset your password.
    The link will be expired in 10 minutes.
    
    {BASE}/reset_password/{code}/
    
Best wishes,
c7w

    '''.replace('{code}', code).replace('{BASE}', BASE_URL)
    
    send_mail("Password Reset | No Reply", message, 'SAST_SearchEngine@cc7w.cf', [email])

def verifyCode(code):
    # Init the permission
    # AuthModels.Permission.objects.create(
    #     name='EmailVerified', codename='EmailVerified', content_type=ContentType.objects.get(app_label='auth', model='user'))
    
    try:
        record = RegVerify.RegVerify.objects.get(code=code)
        permission = AuthModels.Permission.objects.get(codename='EmailVerified')
        AuthModels.User.objects.get(username=record.email).user_permissions.add(permission)
        record.delete()
        return True
    except:
        return False
