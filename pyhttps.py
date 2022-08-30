import sys
import os
import subprocess
import argparse

import http.server
import ssl


def runcmd(cmd):
    ret = os.system(cmd)
    if ret == 0:
        return 0
    else:
        raise Exception('Make certificate error')


def makeCert():
    try:
        cmd = 'openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem'
        runcmd(cmd)
    except Exception as e:
        return -1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="the ip of the server(default localhost)",default='localhost', type=str)
    parser.add_argument("-p", "--port", help="the server port",default=8080, type=int)
    parser.add_argument("-c", "--cert", help="the server certificate",default='./cert.pem',type=str)
    parser.add_argument("-k", "--key", help="the server certificate",default='./key.pem',type=str)
    parser.add_argument("-m", "--make", help="make server certificate and key", action="store_true")
    args = parser.parse_args()

    if args.make:
        if makeCert():
            args.cert = '.\cert.pem'
            args.key = '.\key.pem'
        else:
            exit(-1)

    server_address = (args.ip, args.port)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile=args.cert, keyfile=args.key, ssl_version=ssl.PROTOCOL_TLS)
    print('Listening on {}:{}......'.format(args.ip,args.port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt as e:
        httpd.close()
