import json
import sys
import argparse

import util.network
from client.debug import Debug

IPADDRESS = util.network.get_ipaddress()

@Debug.decorator
def get_server(server=f"http://{IPADDRESS}:5000"):
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


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="postman",
        description="change the program configuration",
        epilog="epilog"
    )

    parser.add_argument("-p", "--protocol", help="set protocol",)
    parser.add_argument("-a", "--address", help="set address",)
    parser.add_argument("-P", "--port", help="set port",)
    parser.add_argument("-f", "--file", help="reads config from file",)

    args = parser.parse_args()

    # print(args)
    # print(args.protocol)
    # for k, v in vars(args).items():
    #     print(f"{k=}, {v=}")
    Debug.info(f"{args=}")
    if args.file:
        Debug.info(f"{args.file=}")
        try:
            Debug.info(f"trying {args.file}...")
            with open(args.file) as fp:
                Debug.info(f"found {args.file}")
                config: dict = json.load(fp)
                Debug.info("config content:", config)
                protocol = config.get("protocol", "http")
                host = config.get("host", util.network.get_ipaddress())
                port = config.get("port", 5000)
                server = f"{protocol}://{host}:{port}"
                Debug.info(f"SERVER from {args.file}: {server}")
        except FileNotFoundError as e:
            Debug.error(f"file '{args.file}' not found")
            raise SystemExit()
    else:
        protocol = args.protocol or "http"
        host = args.address or util.network.get_ipaddress()
        port = args.port or 5000

    server = f"{protocol}://{host}:{port}"
    Debug.info(f"{server=}")
    return server

