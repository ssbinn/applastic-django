# from django.views.generic import ListView
import urllib.request
from django.shortcuts import render
from django.core.paginator import Paginator
import requests

# def home(request):
#     page = request.GET.get('page', '1')  # 페이지
#     kw = request.GET.get('kw', '')  # 검색어
#     so = request.GET.get('so', 'recent')  # 정렬기준
#     context = {'page': page, 'kw': kw, 'so': so}

#     return render(request, "home.html", context)


# def listAPI(n, so, kw):
#     URL = "http://" + url + ":9200/" + index + "/_search?size=" + str(n)

#     if so == "recent":
#         URL += "&sort=ModDate:desc"
#     else:
#         URL += "&sort=Category:asc"

#     if kw:
#         URL += "&q=" + kw

#     data = requests.get(URL).json()["hits"]["hits"]
#     list = []
#     for d in data:
#         a = d["_source"]
#         a["id"] = d["_id"]
#         list.append(a)
#     return list


# def detailAPI(id):
#     URL = "http://" + url +":9200/" + index + "/_doc/" + id
#     data = requests.get(URL).json()['_source']
#     return data

# def list(request):
#     page = request.GET.get('page', '1')  # 페이지
#     kw = request.GET.get('kw', '')  # 검색어
#     so = request.GET.get('so', 'recent')  # 정렬기준
#     reword = ''

#     data_list = listAPI(10000, so, kw)

#     if not data_list:
#         reword = search_error(kw)
#         data_list = listAPI(10000, so, search_error(kw))

#     paginator = Paginator(data_list, 5)
#     page_obj = paginator.get_page(page)
#     length = format(len(data_list), ',')
#     context = {"data_list":page_obj, 'page': page, 'kw': kw, 'so': so, 'reword':reword, 'length':length}

#     return render(request, 'pybo/list.html', context)

# def list_detail(request, id):
#     data = detailAPI(id)
#     context = {"data":data}
#     return render(request, 'pybo/detail.html', context)

# def all_apps_API(n):
# URL = ""
# data = request.get(URL).json()['hits']['hits']


def all_apps_API(n):
    URL = "http://34.64.163.90:9200/my_index/_search?size=" + str(n)
    data = requests.get(URL).json()  # ["hits"]["hits"]

    list = []
    for d in data:
        a = d["_source"]
        a["id"] = d["_id"]
        list.append(a)

    return list


def all_apps(request):
    # core url

    data_list = all_apps_API(10000)
    # URL = "http://34.64.163.90:9200/chart-apple-iphone-kr-topfree-6005/_search?size=1"
    # URL = "http://34.64.163.90:9200/my_index/_search?size=1"

    context = {"apps": data_list}

    return render(request, "apps/all_apps.html", context)


def app_detail(request, pk):
    # app url

    print(pk)
    return render(request, "apps/app_detail.html")
