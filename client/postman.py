import requests
import json
from datetime import datetime as dt
import sys


# import util.parentimport
# util.parentimport.add_parent_import()
# from _myob.habit_tracker import myob

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
HOME_ENDPOINT = f"{SERVER}/"
GET_RANDOMCAFE_ENDPOINT = f"{SERVER}/random"
GET_ALLCAFES_ENDPOINT = f"{SERVER}/all"
SEARCH_CAFES_QS_ENDPOINT = f"{SERVER}/search"  # ?location=<location>
SEARCH_CAFES_PV_ENDPOINT = f"{SERVER}/search/{{}}"  # /search/<location>
ADD_CAFE_ENDPOINT = f"{SERVER}/add"
UPDATE_COFFEEPRICE_ENDPOINT = f"{SERVER}/update-price/{{}}"  # ?price=<price>

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


def create_user(username: str, token: str):
    """
    create user: one shot
    """
    user_params = {
        "username": username,
        "token": token,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    response = api_call(
        http_method=HTTP_POST,
        endpoint=HOME_ENDPOINT,
        username=username,
        token=token,
        params=user_params
    )
    # response.raise_for_status()
    return response


def create_graph(username, token, graph_id, name, unit, graph_type, color):
    """
    create graph: one shot
    """
    graph_config = {
        "id": graph_id,
        "name": name,
        "unit": unit,
        "type": graph_type,
        "color": color
    }
    GRAPH_ENDPOINT = f"{HOME_ENDPOINT}/{username}/graphs"
    response = api_call(
        http_method=HTTP_POST,
        endpoint=GRAPH_ENDPOINT,
        username=username,
        token=token,
        params=graph_config
    )
    # response.raise_for_status()
    print(f"get the graph here: {GRAPH_ENDPOINT}/{graph_config['id']}.html")
    return response


def post_pixel(username, token, graphid, quantity, date=dt.now()):
    """
    post a single pixel in the specified graph
    """
    if isinstance(date, dt):
        date = date.strftime("%Y%m%d")
    if isinstance(date, str):
        pass

    params = {
        "date": date,
        "quantity": str(quantity)
    }
    POSTPIXEL_ENDPOINT = f"{HOME_ENDPOINT}/{username}/graphs/{graphid}"
    response = api_call(
        http_method=HTTP_POST,
        endpoint=POSTPIXEL_ENDPOINT,
        username=username,
        token=token,
        params=params
    )
    response.raise_for_status()
    return response


def update_pixel(username, token, graphid, quantity, date=dt.now()):
    """
    update a single pixel in the specified graph
    """
    if isinstance(date, dt):
        date = date.strftime("%Y%m%d")
    if isinstance(date, str):
        pass

    params = {
        "quantity": str(quantity)
    }
    UPDATEPIXEL_ENDPOINT = f"{HOME_ENDPOINT}/{username}/graphs/{graphid}/{date}"
    response = api_call(
        http_method=HTTP_PUT,
        endpoint=UPDATEPIXEL_ENDPOINT,
        username=username,
        token=token,
        params=params
    )
    response.raise_for_status()
    return response


def delete_pixel(username, token, graphid, date=dt.now()):
    """
    delete a single pixel in the specified graph
    """
    if isinstance(date, dt):
        date = date.strftime("%Y%m%d")
    if isinstance(date, str):
        pass

    DELETEPIXEL_ENDPOINT = f"{HOME_ENDPOINT}/{username}/graphs/{graphid}/{date}"
    response = api_call(
        http_method=HTTP_DEL,
        endpoint=DELETEPIXEL_ENDPOINT,
        username=username,
        token=token,
    )
    response.raise_for_status()
    return response


def get_randomcafe():
    response = api_call(HTTP_GET, GET_RANDOMCAFE_ENDPOINT)
    return response


def get_allcafes():
    response = api_call(HTTP_GET, GET_ALLCAFES_ENDPOINT)
    return response


def search_cafes(location, querystring=True):
    params = dict(location=location)
    if querystring:
        response = api_call(HTTP_GET, SEARCH_CAFES_QS_ENDPOINT, params=params)
    else:
        url = SEARCH_CAFES_PV_ENDPOINT.format(location)
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
    payload = locals()
    response = api_call(HTTP_POST, ADD_CAFE_ENDPOINT, data=payload)
    pass


def update_price(id, price):
    payload = dict(price=price)
    url = UPDATE_COFFEEPRICE_ENDPOINT.format(id)
    response = api_call(HTTP_PATCH, url, data=payload)
    return response


if __name__ == '__main__':
    # get_randomcafe()
    # get_allcafes()
    # search_cafes("London Bridge", False)
    # search_cafes("London Bridge")
    # add_cafe("name")
    update_price(1, 10.0)
    # create_user(username=myob.PIXELA_USERNAME, token=myob.PIXELA_TOKEN)
    # create_graph(username=myob.PIXELA_USERNAME, token=myob.PIXELA_TOKEN,
    #              graph_id="graph1",
    #              name="Cycling Graph",
    #              unit="km",
    #              graph_type="float",
    #              color="sora"
    # )
    # post_pixel(username=myob.PIXELA_USERNAME, token=myob.PIXELA_TOKEN, graphid="graph1", quantity=1)
    # update_pixel(username=myob.PIXELA_USERNAME, token=myob.PIXELA_TOKEN, graphid="graph1", quantity=100)
    # delete_pixel(username=myob.PIXELA_USERNAME, token=myob.PIXELA_TOKEN, graphid="graph1")
