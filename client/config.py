import json
import sys
import argparse
import dataclasses
import requests
import util.network
from client.debug import Debug


@dataclasses.dataclass
class Endpoint:
    name: str = None
    args: list[str] = None


@dataclasses.dataclass
class Config:
    available_servers: list[str] = None
    server: str = None
    endpoint: Endpoint = None


CONFIG = None


# IPADDRESS = util.network.get_ipaddress()

@Debug.decorator
def get_working_server(servers):
    workingserver = None
    for server in servers:
        home = f"{server}/"
        Debug.info(f"trying {home}")
        try:
            response = requests.get(home)
            response.raise_for_status()
            workingserver = server
        except Exception:
            continue
    return workingserver


@Debug.decorator
def get_available_servers(protocol, host, port):
    servers = []
    if not host:
        ips = util.network.get_localips()
        for host in ips:
            server = f"{protocol}://{host}:{port}"
            servers.append(server)
    else:
        server = f"{protocol}://{host}:{port}"
        servers.append(server)

    return servers


@Debug.decorator
def get_servers_from_args(args) -> str:
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
                port = config.get("port", 5000)
                host = config.get("host")

                # Debug.info(f"SERVERS from {args.file}: {servers}")
        except FileNotFoundError as e:
            Debug.error(f"file '{args.file}' not found")
            raise SystemExit()
    else:
        protocol = args.protocol or "http"
        port = args.port or 5000
        host = args.address

    servers = get_available_servers(protocol, host, port)
    Debug.info(f"{servers=}")

    return servers


@Debug.decorator
def parse_arguments() -> Config:
    global CONFIG

    Debug.info("Creating parser")
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
    config = Config()

    servers = get_servers_from_args(args)
    Debug.info(f"{servers=}")
    config.available_servers = servers

    server = get_working_server(servers)
    Debug.info(f"{server=}")
    config.server = server

    # config.endpoint = Endpoint()
    CONFIG = config
    return config


if __name__ == '__main__':
    parse_arguments()
