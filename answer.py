import threading
import requests

from keeper import URLS


def make_request(url):
    return requests.get(url)


def make_threads():
    for i in range(len(URLS[:5])):
        url = URLS.pop(i)
        thread = threading.Thread(target=make_request, kwargs={"url": url})
        thread.start()


def run():
    while True:
        if URLS:
            make_threads()