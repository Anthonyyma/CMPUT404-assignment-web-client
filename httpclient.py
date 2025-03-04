#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        port = urlparse(url).port
        if (port == None):
            return 80
        return int(port)
    
    def get_host_ip(self, url):
        ip = urlparse(url).hostname
        return ip
    
    def get_host_path(self, url):
        path = urlparse(url).path
        if len(path) == 0:
            return '/'
        return path
            
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        hostPort = self.get_host_port(url)
        hostIp = self.get_host_ip(url)
        hostPath = self.get_host_path(url)
        body = f"GET {hostPath} HTTP/1.1\r\nHost: {hostIp}:{hostPort}\r\nAccept: */*\r\nConnection: close\r\n\r\n"
        self.connect(hostIp, hostPort)
        self.sendall(body)
        fullData = self.recvall(self.socket)
        code = int(fullData.split()[1])
        returnBody = fullData.split("\r\n\r\n")[1]
        self.socket.close()
        return HTTPResponse(code, returnBody)

    def POST(self, url, args=None):
        hostPort = self.get_host_port(url)
        hostIp = self.get_host_ip(url)
        hostPath = self.get_host_path(url)
        self.connect(hostIp, hostPort)
        body = ''
        if args:
            body = urllib.parse.urlencode(args)
        contentLength = str(len(body))
        header = f"POST {hostPath} HTTP/1.1\r\nHost: {hostIp}:{hostPort}\r\nAccept: */*\r\n"
        content = f"Content-Type: application/x-www-form-urlencoded\r\nContent-Length: {contentLength}\r\nConnection: close\r\n\r\n"
        payload = header + content + body
        self.sendall(payload)
        fullData = self.recvall(self.socket)
        code = int(fullData.split()[1])
        returnBody = fullData.split("\r\n\r\n")[1]
        self.socket.close()
        return HTTPResponse(code, returnBody)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
