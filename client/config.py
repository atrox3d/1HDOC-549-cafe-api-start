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
def get_available_servers(protocol="http", port="5000"):
    servers = []
    ips = util.network.get_localips()
    for host in ips:
        server = f"{protocol}://{host}:{port}"
        servers.append(server)
    return servers


@Debug.decorator
def get_server_from_args(args) -> str:
    Debug.info(f"{args=}")
    protocol = args.protocol or "http"
    host = args.address or "localhost"
    port = args.port or 5000
    # servers = get_available_servers(protocol, host, port)
    # Debug.info(f"{servers=}")

    server = f"{protocol}://{host}:{port}"
    return server


@Debug.decorator
def get_server_from_file(file):
    try:
        Debug.info(f"trying {file}...")
        with open(file) as fp:
            Debug.info(f"found {file}")
            config: dict = json.load(fp)
            Debug.info("config content:", config)
            protocol = config.get("protocol", "http")
            port = config.get("port", 5000)
            host = config.get("host", "localhost")
            return f"{protocol}://{host}:{port}"
    except FileNotFoundError as e:
        Debug.error(f"file '{file}' not found")
        raise SystemExit()


@Debug.decorator
def parse_arguments() -> Config:
    global CONFIG

    Debug.info("Creating parser")
    parser = argparse.ArgumentParser(
        prog="postman",
        description="change the program configuration",
        epilog="epilog",
        usage="%(prog)s [-f file] | [-p protocol -a addreass -P port]"
    )

    subparsers = parser.add_subparsers()
    # subparsers.add_parser()

    parser.add_argument("-p", "--protocol", help="set protocol", )
    parser.add_argument("-a", "--address", help="set address", )
    parser.add_argument("-P", "--port", help="set port", )
    parser.add_argument("-f", "--file", help="reads config from file", )

    args = parser.parse_args()
    Debug.info(f"{args=}")
    notfile = [value for name, value in vars(args).items() if name != "file"]
    if args.file and any(notfile):
        parser.error("cannot specify -f and [-paP]")
        exit()

    config = Config()

    if args.file:
        Debug.info(f"{args.file=}")
        server = get_server_from_file(args.file)
    elif any(notfile):
        Debug.info(f"{vars(args)}")
        server = get_server_from_args(args)
        # Debug.info(f"{server=}")
    else:
        available_servers = get_available_servers()
        Debug.info(f"{available_servers=}")
        config.available_servers = available_servers
        server = get_working_server(available_servers)

    Debug.info(f"{server=}")
    config.server = server

    # config.endpoint = Endpoint()
    CONFIG = config
    return config


if __name__ == '__main__':
    parse_arguments()
