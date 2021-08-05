import time, math, jieba
from django.http.response import HttpResponse
from SearchEngine.models.Search import News
from django.db.models import Q
from django.shortcuts import redirect, render

def merge(listA, listB):
    result = listA
    for keyB in listB:
        found = False
        for resultKey in result:
            if(keyB['article']==resultKey['article']):
                found = True
                resultKey['weight'] += keyB['weight']
                break
        if not found:
            result.append(keyB)
    return result

def SingleSearch(query):
    q1 = News.objects.filter(
        Q(title__contains=query) | Q(content__contains=query))
    result = []
    for article in q1:
        # Retrieve Data and Calculate Weight
        title_weight = article.title.count(query) * 10
        content_weight = article.content.count(query)
        result.append({"article": article.id, "weight": (
            title_weight + content_weight)})
    return result

def SearchNews(req, query, fuzzy, page, props):
    START_SEARCH = time.time()
    if fuzzy != 'disabled':
        searchList = jieba.cut_for_search(query)
        result = []
        for keyword in searchList:
            result = merge(result, SingleSearch(keyword))
    else:
        result = SingleSearch(query)
        
    result.sort(key=lambda s: s['weight'], reverse=True)

    props['search'] = {
        'resultCount': len(result),
        'currPage': page,
        'totalPage': math.ceil(len(result)/10),
        'lastPage': "/search?q=%s&fuzzy=%s&page=%s" % (query, fuzzy, page-1),
        'nextPage': "/search?q=%s&fuzzy=%s&page=%s" % (query, fuzzy, page+1),
        'currEntry': []
    }
    for entry in result[(page-1)*10: page*10]:
        article = News.objects.get(id=entry['article'])
        title = ("<a href='%s'>%s</a>" % ("/news?id="+str(entry['article'])+"&highlight="+query,
                                            article.title.replace(query, "<span style='background-color: yellow'>%s</span>" % query)))
        # TODO
        excerpt = article.content[0:50]
        excerpt = excerpt.replace(
            query, "<span style='background-color: yellow'>%s</span>" % query)
        if len(article.content) > 50:
            excerpt += "..."
            

        currObject = {
            "title": title,
            "excerpt": excerpt
        }
        props['search']['currEntry'].append(currObject)

    if fuzzy != "disabled":
        props['search']['fuzzy'] = "(Fuzzy)"
    else:
        props['search']['fuzzy'] = "<a href='%s'>Enable fuzzy search.</a>" % ("/search?q=%s&fuzzy=%s&page=%s" % (query, "enabled", page))
    
    END_SEARCH = time.time()
    props['search']['timeCost'] = round(END_SEARCH - START_SEARCH, 6)
    return render(req, "search/result.html", props)
