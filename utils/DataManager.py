import json
import sys, os
from datetime import datetime, tzinfo
from SearchEngine.models.Search import News, SearchRecord
from django.http.response import HttpResponse
from django.utils import timezone



def ProcessData():
    BASE_DIR = "./data/"
    fileCount = 0
    
    for fileName in os.listdir(BASE_DIR):
        FILE_DIR = BASE_DIR + fileName
        f = open(FILE_DIR, 'r', encoding="utf-8")
        data = json.load(f)
        f.close()
        
        n = News(title=data['title'], time=timezone.make_aware(datetime.strptime(
            data['time'], "%Y-%m-%d %H:%M:%S"), timezone.get_current_timezone()), content=data['content'], source=data['source'])
        n.save()
        fileCount += 1
        os.remove(FILE_DIR)

    return HttpResponse("OK, processed " + str(fileCount) + " files.")
