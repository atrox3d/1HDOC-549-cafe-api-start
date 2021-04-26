import json
import sys

import util.network
from client.debug import Debug


@Debug.decorator
def get_server(server="http://localhost:5000"):
    Debug.info(f"default SERVER: {server}")

    jsonfile = "server.json"
    for path in [f"../{jsonfile}", jsonfile]:
        try:
            Debug.info(f"trying {path}...")
            with open(path) as fp:
                Debug.info(f"found {path}")
                config: dict = json.load(fp)
                Debug.info("config content:", config)
                protocol = config.get("PROTOCOL", "http")
                host = config.get("HOST", util.network.get_ipaddress())
                port = config.get("PORT", 5000)
                server = f"{protocol}://{host}:{port}"
                Debug.info(f"SERVER from {path}: {server}")
        except Exception as e:
            Debug.info(repr(e))

    try:
        Debug.info(f"trying sys.argv[1]...")
        protocol = "http"
        host = sys.argv[1]
        port = sys.argv[2]
        server = f"{protocol}://{host}:{port}"
        Debug.info(f"SERVER from sys.argv[1]: {server}")
    except IndexError as ie:
        Debug.info(repr(ie))

    return server