import hashlib
from django.contrib.auth.models import AnonymousUser, User

def getProps(req, title):
    result = {}
    result['title'] = title + " | SAST Search"
    result['login'] = {}
    
    if req.user.username:
        result['login']['success'] = '1'
        md5 = hashlib.md5()
        md5.update(req.user.username.encode(encoding='utf-8'))
        result['login']['avatar'] = 'https://www.gravatar.com/avatar/' + \
            md5.hexdigest()
        
    else:
        result['login']['success'] = '0'
    return result
