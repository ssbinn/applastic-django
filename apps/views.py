from django.shortcuts import render
from django.core.paginator import Paginator
from elasticsearch import Elasticsearch

# def home(request):
#     page = request.GET.get('page', '1')  # 페이지
#     kw = request.GET.get('kw', '')  # 검색어
#     so = request.GET.get('so', 'recent')  # 정렬기준
#     context = {'page': page, 'kw': kw, 'so': so}

#     return render(request, "home.html", context)


# def detailAPI(id):
#     URL = "http://" + url +":9200/" + index + "/_doc/" + id
#     data = requests.get(URL).json()['_source']
#     return data


# def list_detail(request, id):
#     data = detailAPI(id)
#     context = {"data":data}
#     return render(request, 'pybo/detail.html', context)


def search_apps_API():
    es = Elasticsearch("http://34.64.163.90:9200", basic_auth=("kyj", "210is1024"))

    index = es.search(index="chart-apple-iphone-kr-topfree-6005")
    size = index["hits"]["total"]

    resp = es.search(
        index="chart-apple-iphone-kr-topfree-6005",
        body={"size": size["value"], "query": {"match_all": {}}},
        # body={"size": size["value"], "query": {"match": {"trackName":"당근마켓"}}},
    )

    list = []
    i = 1
    while i < size["value"]:
        temp = resp["hits"]["hits"][i]["_source"]
        temp["id"] = resp["hits"]["hits"][i]["_id"]

        list.append(temp)
        i += 1

    return list


def all_apps(request):
    # core url

    page = request.GET.get("page")  # paginator
    app_list = search_apps_API()

    if not app_list:
        print("힝구")

    paginator = Paginator(app_list, 10)  # per_page: 10
    apps = paginator.get_page(page)

    context = {"page": apps}
    return render(request, "apps/all_apps.html", context)


def app_detail(request, pk):
    # app url

    print(pk)
    return render(request, "apps/app_detail.html")
