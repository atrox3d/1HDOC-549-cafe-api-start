import socket


def get_ipaddress():
    return socket.gethostbyname(socket.gethostname())
