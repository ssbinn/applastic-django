from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import render
from elasticsearch import Elasticsearch


def cloud_auth():
    es = Elasticsearch(
        cloud_id="Applastic:YXAtbm9ydGhlYXN0LTIuYXdzLmVsYXN0aWMtY2xvdWQuY29tOjkyNDMkZTU4ZGM0YTBhMWRlNDc1N2ExY2I5ZjUxNzIzODA5MjgkYjhkMDA2NmY4YTU0NDY1MTg1MTA5ZDczNWIyMjQ4NmQ=",
        http_auth=("elastic", "bSiGnlanK5wQgs8UOYV2u1dJ"),
    )
    return es


def pagenation(vari, page):
    paginator = Paginator(vari, 10, orphans=5)
    list = paginator.page(int(page))

    return list


def list_API(size):
    es = cloud_auth()

    index = es.search(index="ssbinn_index")
    resp = es.search(
        index="ssbinn_index",
        body={"size": size, "query": {"match_all": {}}},
    )

    list = []
    i = 0
    while i < size:
        temp = resp["hits"]["hits"][i]["_source"]
        temp["id"] = resp["hits"]["hits"][i]["_source"]["trackId"]

        list.append(temp)
        i += 1

    return list


def home(request):
    app_preview = list_API(10)  # 앱 10개 메인 페이지에서 미리보기
    context = {"app_preview": app_preview}
    return render(request, "home.html", context)


def all_apps(request):
    page = request.GET.get("page", 1)
    app_list = list_API(100)
    # ssbinn_index 내 app data는 100개, elasticsearch는 size 최대 10000까지 가능

    try:
        apps = pagenation(app_list, page)

        context = {"page": apps}
        return render(request, "apps/app_list.html", context)
    except EmptyPage:  # url에 엉뚱한 page number를 검색할 경우
        raise Http404


def detail_API(id):
    es = cloud_auth()

    index = es.search(index="ssbinn_index")
    resp = es.search(
        index="ssbinn_index",
        body={"query": {"match": {"trackId": id}}},
    )

    for hit in resp["hits"]["hits"]:
        return hit["_source"]


def app_detail(request, id):
    app = detail_API(id)

    if app == None:  # url에 엉뚱한 앱 고유 id를 검색할 경우
        raise Http404

    context = {"app": app}
    return render(request, "apps/detail.html", context)


def search_API(keyword):
    es = cloud_auth()

    index = es.search(index="ssbinn_index")
    resp = es.search(
        index="ssbinn_index",
        body={
            "size": 10000,
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["trackName", "description"],
                }
            },
        },
    )
    # fields: 쿼리할 fields들
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


def search(request):
    if request.method == "POST":
        keyword = request.POST["searched"]  # 검색창에 입력된 내용 저장
        answer = search_API(keyword)  # index 내에 검색한 내용이 있는 지 확인

        page = request.GET.get("page", 1)
        apps = pagenation(answer, page)

        if not answer:  # 검색 결과가 없을 경우
            no_result = True
            context = {"keyword": keyword, "answer": apps, "no_result": no_result}
        else:
            context = {"keyword": keyword, "answer": apps}

        return render(request, "apps/app_list.html", context)


def genre_API(genre):  # 장르 태그 선택 시 app list를 불러오는 함수
    es = cloud_auth()

    index = es.search(index="ssbinn_index")
    resp = es.search(
        index="ssbinn_index",
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

    apps = pagenation(data_list, page)

    context = {"data_list": apps, "tag": tag}
    return render(request, "apps/app_list.html", context)


def analysis(request):
    return render(request, "apps/analysis.html")
