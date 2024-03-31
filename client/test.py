import requests
import json
def test():
    user = {"user":"0000", "password": "1234"}
    response = requests.post('http://50.16.235.247:8081/login', json=user)
    print(response.text)
test()
