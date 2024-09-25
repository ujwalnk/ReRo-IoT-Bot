import socket, select, time, network

import requests

from common import DataSentinel as ds

our_handlers = []

def route(path, methods=['GET']):
    def wrapper(handler):
        our_handlers.append((path, methods, handler))
        return handler
    return wrapper

def req_handler(cs):
    try:
        line = cs.readline()
        print('line:', line)
        parts = line.decode().split()
        if len(parts) < 3:
            raise ValueError
        r={}
        r['method'] = parts[0]
        r['path'] = parts[1]
        parts = r['path'].split('?', 1)
        if len(parts) < 2:
            r['query'] = None
        else:
            r['path'] = parts[0]
            r['query'] = parts[1]
        r['headers'] = {}
        while True:
            line = cs.readline()
            if not line:
                break
            line = line.decode()
            if line == '\r\n':
                break
            key, value = line.split(':', 1)
            r['headers'][key.lower()] = value.strip()
        handled = False
        for path, methods, handler in our_handlers:
            if r['path'] != path:
                continue
            if r['method'] not in methods:
                continue
            handled = True
            handler(cs,r)
        if not handled:
            cs.write(b'HTTP/1.0 404 Not Found\r\n\r\nNot Found')
            print('No handler found')
    except Exception as e:
        print('Err:', e)
    cs.close()

def cln_handler(srv):
    cs,ca = srv.accept()
    print('Serving:', ca)
    cs.setblocking(False)
    cs.setsockopt(socket.SOL_SOCKET, 20, req_handler) # 20 = _SO_REGISTER_HANDLER
    # the above allows for waiting for something that is sent later.

def start():

    """
    Function to setup the webserver for the REST API implementation

    Starts the webserver on the port 8080 and exposes the port to the network
    """

    # Set & expose the port to the network
    addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]

    # Start the socket stream over http
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the address & accept 1 client at most
    srv.bind(addr)
    srv.listen(1)

    # Enable non-blocking calls
    srv.setblocking(False)
    srv.setsockopt(socket.SOL_SOCKET, 20, cln_handler)  # 20 = _SO_REGISTER_HANDLER

@route('/get_code')
def get_code_handler(cs, r):  
    """
    Function to handle to the alert from the server & make a request to the server for the code

    @param:
        cs (socket): the socket to read/write from/to
        r (dict): dict with additional info
    """

    # Return a OK message
    cs.write(b'HTTP/1.0 200 OK\r\n')
    print("Getting code from server")

    # Make a request to the server to get the code
    code_file = requests.get(ds.SERVER_IP_ADDRESS + "/get_code/iotbot", headers={"accept": "text/x-python"})
    code_file.save("user.py")

    # TODO: Call 2 create a new thread & run the user.py file

@route('/stop')
def stop_user_thread(cs, r):
    cs.write(b'HTTP/1.0 200 OK\r\n')
    print("Stopping user code")

print('our_handlers:', our_handlers)