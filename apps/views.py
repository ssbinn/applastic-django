from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import render
from elasticsearch import Elasticsearch


def home(request):
    # apps/urls.py

    app_name = request.GET.get("app", "Anywhere")
    app_name = str.capitalize(app_name)

    context = {"app": app_name}
    return render(request, "home.html", context)


def list_API():
    es = Elasticsearch("http://34.64.163.90:9200", basic_auth=("kyj", "210is1024"))

    index = es.search(index="chart-apple-iphone-kr-topfree-6005")
    size = index["hits"]["total"]

    resp = es.search(
        index="chart-apple-iphone-kr-topfree-6005",
        body={"size": size["value"], "query": {"match_all": {}}},
    )

    list = []
    i = 0
    while i < size["value"]:
        temp = resp["hits"]["hits"][i]["_source"]
        temp["id"] = resp["hits"]["hits"][i]["_source"]["trackId"]
        # temp["genre"] = resp["hits"]["hits"][i]["_source"]["genres"]

        list.append(temp)
        i += 1

    return list


def all_apps(request):
    # apps/urls.py

    page = request.GET.get("page", 1)
    app_list = list_API()

    paginator = Paginator(app_list, 10, orphans=5)  # per_page: 10

    try:
        apps = paginator.page(int(page))  # get_page vs page

        context = {"page": apps}
        return render(request, "apps/all_apps.html", context)
    except EmptyPage:  # url에 엉뚱한 page number를 검색했을 때
        raise Http404


def genre_API(genre):  # 장르 태그 선택 시 앱 리스트 불러오는 함수
    es = Elasticsearch("http://34.64.163.90:9200", basic_auth=("kyj", "210is1024"))
    index = es.search(index="chart-apple-iphone-kr-topfree-6005")

    resp = es.search(
        index="chart-apple-iphone-kr-topfree-6005",
        body={"size": 10000, "query": {"match": {"genres": genre}}},
    )
    size = resp["hits"]["total"]["value"]

    list = []
    i = 0
    while i < size:
        if i == size:
            break
        temp = resp["hits"]["hits"][i]["_source"]
        temp["id"] = resp["hits"]["hits"][i]["_source"]["trackId"]
        list.append(temp)
        i += 1

    return list


def tag(request, tag):
    page = request.GET.get("page", 1)

    data_list = genre_API(tag)

    paginator = Paginator(data_list, 10, orphans=5)  # per_page: 10

    try:
        apps = paginator.page(int(page))

        context = {"data_list": apps, "tag": tag}
        return render(request, "apps/all_apps.html", context)
    except EmptyPage:
        raise Http404


def detail_API(id):
    es = Elasticsearch("http://34.64.163.90:9200", basic_auth=("kyj", "210is1024"))
    index = es.search(index="chart-apple-iphone-kr-topfree-6005")

    resp = es.search(
        index="chart-apple-iphone-kr-topfree-6005",
        body={"query": {"match": {"trackId": id}}},
    )

    for hit in resp["hits"]["hits"]:
        return hit["_source"]


def app_detail(request, id):
    # apps/urls.py

    app = detail_API(id)

    if app == None:  # url에 엉뚱한 앱 고유 id를 검색했을 때
        raise Http404

    context = {"app": app}
    return render(request, "apps/detail.html", context)


def about(request):
    return render(request, "apps/about.html")


def analysis(request):
    return render(request, "apps/analysis.html")
