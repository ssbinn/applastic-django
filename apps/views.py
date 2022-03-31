from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import render
from elasticsearch import Elasticsearch

# def home(request):
#     page = request.GET.get('page', '1')  # 페이지
#     kw = request.GET.get('kw', '')  # 검색어
#     so = request.GET.get('so', 'recent')  # 정렬기준
#     context = {'page': page, 'kw': kw, 'so': so}

#     return render(request, "home.html", context)


def list_API():
    es = Elasticsearch("http://34.64.163.90:9200", basic_auth=("kyj", "210is1024"))

    index = es.search(index="chart-apple-iphone-kr-topfree-6005")
    size = index["hits"]["total"]

    resp = es.search(
        index="chart-apple-iphone-kr-topfree-6005",
        body={"size": size["value"], "query": {"match_all": {}}},
    )

    list = []
    i = 1
    while i < size["value"]:
        temp = resp["hits"]["hits"][i]["_source"]
        temp["id"] = resp["hits"]["hits"][i]["_source"]["trackId"]

        list.append(temp)
        i += 1

    return list


def all_apps(request):
    # core/urls.py

    page = request.GET.get("page", 1)  # paginator
    app_list = list_API()

    # if not app_list:
    #     print("힝구")
    paginator = Paginator(app_list, 10, orphans=5)  # per_page: 10

    try:
        apps = paginator.page(int(page))  # get_page vs page

        context = {"page": apps}
        return render(request, "apps/all_apps.html", context)
    except EmptyPage:  # url에 엉뚱한 page number를 검색했을 때
        raise Http404


def detail_API(id):
    es = Elasticsearch("http://34.64.163.90:9200", basic_auth=("kyj", "210is1024"))
    index = es.search(index="chart-apple-iphone-kr-topfree-6005")
    # size = index["hits"]["total"]

    resp = es.search(
        index="chart-apple-iphone-kr-topfree-6005",
        # body={"size": size["value"], "query": {"match": {"trackId": id}}},
        body={"query": {"match": {"trackId": id}}},
    )
    # resp = es.get(index="chart-apple-iphone-kr-topfree-6005", id=id)

    for hit in resp["hits"]["hits"]:
        return hit["_source"]


def app_detail(request, id):
    # apps/urls.py

    app = detail_API(id)

    if app == None:  # url에 엉뚱한 앱 고유 id를 검색했을 때
        raise Http404

    context = {"app": app}
    return render(request, "apps/detail.html", context)


def search(request):
    # apps/urls.py

    app_name = request.GET.get("app", "Anywhere")
    # http://127.0.0.1:8000/apps/search/ > 검색창에 Anywhere 뜸
    app_name = str.capitalize(app_name)

    context = {"app": app_name}
    return render(request, "apps/search.html", context)
