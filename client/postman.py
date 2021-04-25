import requests
import json
from datetime import datetime as dt
import sys


def get_server(server="http://localhost:5000"):
    print(f"SERVER default: {server}")
    try:
        with open("../server.json") as fp:
            config = json.load(fp)
            # print(config)
            server = config["SERVER"]
            print(f"SERVER from ../server.json: {server}")
    except Exception as e:
        print(repr(e))

    try:
        server = sys.argv[1]
        print(f"SERVER from sys.argv[1]: {server}")
    except IndexError:
        pass

    return server


SERVER = get_server()
# HOME_ENDPOINT = f"{SERVER}/"

HTTP_GET = requests.get
HTTP_POST = requests.post
HTTP_PATCH = requests.patch
HTTP_PUT = requests.put
HTTP_DEL = requests.delete


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
    endpoint = f"{SERVER}/random"
    response = api_call(HTTP_GET, endpoint)
    return response


def get_allcafes():
    endpoint = f"{SERVER}/all"
    response = api_call(HTTP_GET, endpoint)
    return response


def search_cafes(location, querystring=True):
    params = dict(location=location)
    if querystring:
        endpoint = f"{SERVER}/search"  # ?location=<location>
        response = api_call(HTTP_GET, endpoint, params=params)
    else:
        endpoint = f"{SERVER}/search/{{}}"  # /search/<location>
        url = endpoint.format(location)
        response = api_call(HTTP_GET, url)
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
    endpoint = f"{SERVER}/add"
    payload = locals()
    response = api_call(HTTP_POST, endpoint, data=payload)
    pass


def update_price(id, price):
    endpoint = f"{SERVER}/update-price/{{}}"  # ?price=<price>
    url = endpoint.format(id)
    payload = dict(price=price)
    response = api_call(HTTP_PATCH, url, data=payload)
    return response


if __name__ == '__main__':
    # get_randomcafe()
    get_allcafes()
    # search_cafes("London Bridge", False)
    # search_cafes("London Bridge")
    # add_cafe("name")
    # update_price(1, 10.0)
