from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import render
from elasticsearch import Elasticsearch


# def genre_API(genre):  # 장르 태그 선택 시 앱 리스트 불러오는 함수
#     es = Elasticsearch("http://34.64.163.90:9200", basic_auth=("kyj", "210is1024"))
#     index = es.search(index="chart-apple-iphone-kr-topfree-6005")
#     size = index["hits"]["total"]

#     resp = es.search(
#         index="chart-apple-iphone-kr-topfree-6005",
#         body={"size": size["value"], "query": {"match": {"genres": genre}}},
#     )

#     for hit in resp["hits"]["hits"]:
#         return hit["_source"]


def home(request):
    # apps/urls.py

    app_name = request.GET.get("app", "Anywhere")
    app_name = str.capitalize(app_name)

    # genre_types = [
    #     "소셜 네트워킹",
    #     "생산성",
    #     "게임",
    #     "라이프 스타일",
    #     "사진 및 비디오",
    #     "엔터테인먼트",
    #     "유틸리티",
    #     "금융",
    #     "비즈니스",
    #     "음식 및 음료",
    #     "롤플레잉",
    #     "시뮬레이션",
    # ]

    context = {"app": app_name}  # , "genre_types": genre_types}
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
    i = 1
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


def tag(request, tag):
    page = request.GET.get("page", 1)

    data_list = list_API()
    paginator = Paginator(data_list, 10, orphans=5)  # per_page: 10

    apps = paginator.page(int(page))  # get_page vs page

    context = {"page": apps, "tag": tag}
    return render(request, "apps/all_apps.html", context)


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
