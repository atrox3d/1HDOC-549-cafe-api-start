import requests
import json
import sys
import os

if not __package__:
    """
    running this script directly
    """
    print("not package")
    import parentimport

    parentimport.parent_import()
    # parentimport.show_syspath()
    from debug import Debug
    from config import get_server
else:
    """
    importing this script from another script
    """
    print("__package__: ", __package__)
    from . import parentimport

    parentimport.parent_import()
    # parentimport.show_syspath()
    from .debug import Debug  # ok
    from .config import get_server

import util.network

GET = requests.get
POST = requests.post
PATCH = requests.patch
PUT = requests.put
DEL = requests.delete


@Debug.decorator
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
    Debug.info(f"calling request.{http_method.__name__} {endpoint}")
    # if params:
    Debug.info(f"\twith params: {json.dumps(params, indent=4)}")
    Debug.info(f"\twith data: {json.dumps(data, indent=4)}")
    # authentication via headers, not in the url
    # headers = {"X-USER-TOKEN": token}
    headers = {}
    # add more header keys, if available
    if moreheaders:
        headers.update(moreheaders)
    Debug.info(f"\twith headers: {json.dumps(headers, indent=4)}")
    #
    if Debug.enabled:
        response = Debug.response
    else:
        response = http_method(url=endpoint, data=data, params=params, headers=headers)
    Debug.info(f"final URL {response.url}")
    if response.status_code == 200:
        Debug.success("status: ", response.status_code)
    else:
        Debug.error("status: ", response.status_code)
    Debug.info("response: ", response.text)
    return response


@Debug.decorator
def get_randomcafe():
    endpoint = f"{get_server()}/random"
    response = api_call(GET, endpoint)
    return response


@Debug.decorator
def get_allcafes():
    endpoint = f"{get_server()}/all"
    response = api_call(GET, endpoint)
    return response


@Debug.decorator
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


@Debug.decorator
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


@Debug.decorator
def update_price(id, price):
    endpoint = f"{get_server()}/update-price/{{}}"  # ?price=<price>
    url = endpoint.format(id)
    payload = dict(price=price)
    response = api_call(PATCH, url, data=payload)
    return response


if __name__ == '__main__':
    # get_server()
    # print(Debug)
    # Debug.printlogger("INFO", api_call, "test")
    # Debug.info("test")
    # Debug.disable()
    get_randomcafe()
    # get_allcafes()
    # search_cafes("London Bridge", False)
    # search_cafes("London Bridge")
    # add_cafe("name")
    # update_price(1, 10.0)
