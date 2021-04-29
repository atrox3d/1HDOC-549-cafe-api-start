import json
import sys
import argparse
import dataclasses
import util.network
from client.debug import Debug


@dataclasses.dataclass
class Endpoint:
    name: str = None
    args: list[str] = None


@dataclasses.dataclass
class Config:
    server: str = None
    endpoint: Endpoint = None


IPADDRESS = util.network.get_ipaddress()


def get_server_from_args(args) -> str:
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
                host = config.get("host", IPADDRESS)
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


def parse_arguments() -> Config:
    global CONFIG

    parser = argparse.ArgumentParser(
        prog="postman",
        description="change the program configuration",
        epilog="epilog"
    )

    subparsers = parser.add_subparsers()
    # subparsers.add_parser()

    parser.add_argument("-p", "--protocol", help="set protocol", )
    parser.add_argument("-a", "--address", help="set address", )
    parser.add_argument("-P", "--port", help="set port", )
    parser.add_argument("-f", "--file", help="reads config from file", )

    args = parser.parse_args()
    server = get_server_from_args(args)

    config = Config()
    config.server = server
    # config.endpoint = Endpoint()
    CONFIG = config
    return config
