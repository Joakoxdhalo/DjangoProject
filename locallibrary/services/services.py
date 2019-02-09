import requests


def get_books(to_search):
    url = "https://www.googleapis.com/books/v1/volumes?q={}".format(to_search)
    MyAPIKey = "AIzaSyC11sce0KPIZ6ryLjrCSGDn9zEDSVbK-XM"
    url = F"{url}&key={MyAPIKey}"
    print(url)
    r = requests.get(url)
    books = r.json()
    books_list = books["items"]
    return books_list
