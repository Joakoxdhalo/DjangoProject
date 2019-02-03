import requests


def get_books(to_search):
    url = "https://www.googleapis.com/books/v1/volumes?q={}".format(to_search)
    print(url)
    r = requests.get(url)
    books = r.json()
    books_list = books["items"]
    return books_list
