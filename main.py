import threading

from answer import run as run_answer
from server import run as run_server
from json_processing import run as run_json

answer = threading.Thread(target=run_answer)
server = threading.Thread(target=run_server)
json = threading.Thread(target=run_json)

answer.start()
server.start()
json.start()