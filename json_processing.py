from importlib import import_module

from keeper import JSON, URLS

def create_urls(j):
    mod = import_module(f"{j['group_id']}.{j['type']}.logic")
    if "object" in j:
        URLS.append(mod.processing(j["object"]))
    JSON.remove(j)

def run():
    while True:
        if JSON:
            for j in JSON:
                create_urls(j)