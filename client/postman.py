import requests
import json
from datetime import datetime as dt
import sys


GET = requests.get
POST = requests.post
PATCH = requests.patch
PUT = requests.put
DEL = requests.delete


def get_server(server="http://localhost:5000"):
    print("INFO    |", f"default SERVER: {server}")

    jsonfile = "server.json"
    for path in [f"../{jsonfile}", jsonfile]:
        try:
            print("INFO    |", f"trying {path}...")
            with open(path) as fp:
                print("INFO    |", f"found {path}")
                config = json.load(fp)
                print("INFO    |", "config content:", config)
                server = config["SERVER"]
                print("INFO    |", f"SERVER from {path}: {server}")
        except Exception as e:
            print("INFO    |", repr(e))

    try:
        print("INFO    |", f"trying sys.argv[1]...")
        server = sys.argv[1]
        print("INFO    |", f"SERVER from sys.argv[1]: {server}")
    except IndexError as ie:
        print("INFO    |", repr(ie))

    return server


def api_call(
        http_method,
        endpoint,
        username=None,
        token=None,
        params=None,  # GET querystring
        data=None,  # POST payload
        moreheaders=None
):
    """
    call flask api, generalized
    """
    print(f"calling request.{http_method.__name__} {endpoint}")
    # if params:
    print(f"\twith params: {json.dumps(params, indent=4)}")
    print(f"\twith data: {json.dumps(data, indent=4)}")
    # authentication via headers, not in the url
    # headers = {"X-USER-TOKEN": token}
    headers = {}
    # add more header keys, if available
    if moreheaders:
        headers.update(moreheaders)
    print(f"\twith headers: {json.dumps(headers, indent=4)}")
    #
    response = http_method(url=endpoint, data=data, params=params, headers=headers)
    print(f"final URL {response.url}")
    if response.status_code == 200:
        print("SUCCESS|status: ", response.status_code)
    else:
        print("ERROR  |status: ", response.status_code)
    print("response: ", response.text)
    return response


def get_randomcafe():
    endpoint = f"{get_server()}/random"
    response = api_call(GET, endpoint)
    return response


def get_allcafes():
    endpoint = f"{get_server()}/all"
    response = api_call(GET, endpoint)
    return response


def search_cafes(location, querystring=True):
    params = dict(location=location)
    if querystring:
        endpoint = f"{get_server()}/search"  # ?location=<location>
        response = api_call(GET, endpoint, params=params)
    else:
        endpoint = f"{get_server()}/search/{{}}"  # /search/<location>
        url = endpoint.format(location)
        response = api_call(GET, url)
    return response


def add_cafe(
        name,
        map_url="https://some.maps.url",
        img_url="https://some.image.url",
        location="here",
        seats=1,
        has_toilet=True,
        has_wifi=True,
        has_sockets=True,
        can_take_calls=False,
        coffee_price=1.0
):
    endpoint = f"{get_server()}/add"
    payload = locals()
    response = api_call(POST, endpoint, data=payload)
    pass


def update_price(id, price):
    endpoint = f"{get_server()}/update-price/{{}}"  # ?price=<price>
    url = endpoint.format(id)
    payload = dict(price=price)
    response = api_call(PATCH, url, data=payload)
    return response


if __name__ == '__main__':
    pass
    get_server()
    # get_randomcafe()
    # get_allcafes()
    # search_cafes("London Bridge", False)
    # search_cafes("London Bridge")
    # add_cafe("name")
    # update_price(1, 10.0)
