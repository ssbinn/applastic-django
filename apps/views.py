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
    es = Elasticsearch(
        cloud_id="Applastic:YXAtbm9ydGhlYXN0LTIuYXdzLmVsYXN0aWMtY2xvdWQuY29tOjkyNDMkZTU4ZGM0YTBhMWRlNDc1N2ExY2I5ZjUxNzIzODA5MjgkYjhkMDA2NmY4YTU0NDY1MTg1MTA5ZDczNWIyMjQ4NmQ=",
        http_auth=("elastic", "bSiGnlanK5wQgs8UOYV2u1dJ"),
    )

    index = es.search(index="testtest-topfree-apple-2022-03-13")
    # index = es.indices.get_template("topfree-apple-mapping")
    size = index["hits"]["total"]

    resp = es.search(
        index="testtest-topfree-apple-2022-03-13",
        body={"size": size["value"], "query": {"match_all": {}}},
    )

    list = []
    i = 0
    while i < size["value"]:
        temp = resp["hits"]["hits"][i]["_source"]
        temp["id"] = resp["hits"]["hits"][i]["_source"]["trackId"]

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
    es = Elasticsearch(
        cloud_id="Applastic:YXAtbm9ydGhlYXN0LTIuYXdzLmVsYXN0aWMtY2xvdWQuY29tOjkyNDMkZTU4ZGM0YTBhMWRlNDc1N2ExY2I5ZjUxNzIzODA5MjgkYjhkMDA2NmY4YTU0NDY1MTg1MTA5ZDczNWIyMjQ4NmQ=",
        http_auth=("elastic", "bSiGnlanK5wQgs8UOYV2u1dJ"),
    )
    index = es.search(index="testtest-topfree-apple-2022-03-13")

    resp = es.search(
        index="testtest-topfree-apple-2022-03-13",
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
    es = Elasticsearch(
        cloud_id="Applastic:YXAtbm9ydGhlYXN0LTIuYXdzLmVsYXN0aWMtY2xvdWQuY29tOjkyNDMkZTU4ZGM0YTBhMWRlNDc1N2ExY2I5ZjUxNzIzODA5MjgkYjhkMDA2NmY4YTU0NDY1MTg1MTA5ZDczNWIyMjQ4NmQ=",
        http_auth=("elastic", "bSiGnlanK5wQgs8UOYV2u1dJ"),
    )
    index = es.search(index="testtest-topfree-apple-2022-03-13")

    resp = es.search(
        index="testtest-topfree-apple-2022-03-13",
        body={"query": {"match": {"trackId": id}}},
    )

    for hit in resp["hits"]["hits"]:
        return hit["_source"]


def app_detail(request, id):
    # apps/urls.py

    app = detail_API(id)
    print(app)

    if app == None:  # url에 엉뚱한 앱 고유 id를 검색했을 때
        raise Http404

    context = {"app": app}
    return render(request, "apps/detail.html", context)


def about(request):
    return render(request, "apps/about.html")


def analysis(request):
    return render(request, "apps/analysis.html")
