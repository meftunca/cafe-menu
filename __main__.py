import requests
import json
from bs4 import BeautifulSoup
from slugify import slugify

collection = {}
urlCollection = [
    {"title": "Yemekler", "url": "", "alt": "Yemek"},
    {"title": "Tatlılar", "url": "tatlilar", "alt": "Tatlı"},
    {"title": "İçecekler", "url": "icecekler", "alt": "İçecek"}
]


for item in urlCollection:
    subCollection = {
        "subList": []
    }
    r = requests.get('https://thehousecafe.com/menu/'+item["url"])
    source = BeautifulSoup(r.content, "html.parser")
    pageData = source.find_all("div", attrs={"class": "foodpress_menu"})
    for head in pageData:
        subCollectionWrapper = {
            "title": "",
            "list": []
        }
        subCollectionWrapper["title"] = head.find("h2").text
        # print(len(head.find_all("div", attrs={"class": "fp_inner_box"})))
        for sub in head.find_all("div", attrs={"class": "fp_inner_box"}):
            price = ""
            if sub.find("span") == None:
                print(type(sub.find("span")))
            else:
                price = sub.find("span").text
            # print(sub.find("span"), i)
            # break
            newSub = {
                "title": sub.find("h3")["title"],
                "price": price,
                "description": sub.find("div", attrs={"class": "menu_description"}).text.replace("Read More", ""),
            }
            subCollectionWrapper["list"].append(newSub)
        subCollection["subList"].append(subCollectionWrapper)
    img = source.find("img", attrs={"alt": item["alt"]})["src"]
    collection[item["title"]] = {
        "img": img,
        "title": item["title"],
        "category": subCollection
    }

with open('collection.json', 'w') as json_file:
    json.dump(collection, json_file, ensure_ascii=False)
