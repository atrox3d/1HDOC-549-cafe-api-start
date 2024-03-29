import json
import sys
import argparse
import dataclasses
import requests

if not __package__:
    """
    running this script directly
    """
    print("not package")
    import parentimport

    parentimport.parent_import()
    # parentimport.show_syspath()
    import util.network
    from client.debug import Debug
else:
    """
    importing this script from another script
    """
    print("__package__: ", __package__)
    from . import parentimport

    parentimport.parent_import()
    # parentimport.show_syspath()
    import util.network
    from client.debug import Debug


@dataclasses.dataclass
class Endpoint:
    """
    represents a end point and its parameters
    """
    url: str = None
    route: str = None
    params: list[str] = None


@dataclasses.dataclass
class Config:
    """
    configuration class
    """
    available_servers: list[str] = None
    server: str = None
    endpoint: Endpoint = None


# TODO: remove?
CONFIG = None


# IPADDRESS = util.network.get_ipaddress()


@Debug.decorator
def get_working_server(servers):
    """
    test each server until doesnt get a connection or fails
    """
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
    """
    loops through the local adapters and build a list of possible servers
    """
    servers = []
    ips = util.network.get_localips()
    for host in ips:
        server = f"{protocol}://{host}:{port}"
        servers.append(server)
    return servers


@Debug.decorator
def get_server_from_args(args) -> str:
    """
    creates a string representation of a server
    based on command line arguments
    """
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
    """
    builds a string representation of a server
    from a json file
    """
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
def get_endpoint_from_args(args):
    url = getattr(args, "endpoint.url", None)
    route = getattr(args, "endpoint.route", None)
    params = getattr(args, "endpoint.params", None)

    if any([url, route]):
        endpoint = Endpoint(url, route, params)
        return endpoint
    else:
        return None


@Debug.decorator
def parse_arguments() -> Config:
    """
    creates a parser for command line arguments
    populates a Config object with the results
    """
    global CONFIG

    Debug.info("Creating parser")

    parser = argparse.ArgumentParser(
        prog="postman",
        description="change the program configuration",
        epilog="epilog",
        usage="%(prog)s [-f file] | [-p protocol -a addreass -P port]"
    )

    parser.add_argument("-p", "--protocol", help="set protocol", )
    parser.add_argument("-a", "--address", help="set address", )
    parser.add_argument("-P", "--port", help="set port", )
    parser.add_argument("-f", "--file", help="reads config from file", )

    subparsers = parser.add_subparsers()
    endpoint = subparsers.add_parser("endpoint")

    group = endpoint.add_mutually_exclusive_group()
    group.add_argument("-u", "--url", dest="endpoint.url")
    group.add_argument("-r", "--route", dest="endpoint.route")

    endpoint.add_argument("-p", "--params", dest="endpoint.params", action="extend", nargs='+')

    args = parser.parse_args()

    Debug.info(f"{args=}")
    #
    print(getattr(args, 'endpoint.url'))
    #
    notfile = [value for name, value in vars(args).items() if name in ["protocol", "host", "port"]]
    if args.file and any(notfile):
        parser.error("cannot specify -f and [-paP]")
        exit()

    config = Config()

    if args.file:
        Debug.info(f"{args.file=}")
        server = get_server_from_file(args.file)
    elif any(notfile):
        Debug.info(f"{vars(args)=}")
        server = get_server_from_args(args)
        # Debug.info(f"{server=}")
    else:
        available_servers = get_available_servers()
        Debug.info(f"{available_servers=}")
        config.available_servers = available_servers
        server = get_working_server(available_servers)

    Debug.info(f"{server=}")
    config.server = server

    config.endpoint = get_endpoint_from_args(args)
    # config.endpoint = Endpoint()
    CONFIG = config
    return config


if __name__ == '__main__':
    args = input("arguments: ").split()
    sys.argv.extend(args)
    config = parse_arguments()
    print(f"{config=}")
