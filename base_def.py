import requests
import json
import socket
import argparse


#该脚本中存储所有全局函数、常量
#该项目计划最终实现漏洞扫描和利用自动化进行
#所有漏洞利用均包含自动探测和利用
#利用形式以返回远程命令为主，其他利用情况根据漏洞特性决定
#ps：祝我顺利通过OSWE

def start_help(parser):
    parser.description = "Hello to use the script to pentest"
    parser.add_argument("-i", "--ip", help="IP address of target", type=str, default="127.0.0.1")
    parser.add_argument("-p", "--port", help="Port of target", type=str, default="8080")
    parser.add_argument("-a", "--args", help="Parameter as dict,like {'key1':'value1','key2':'value2'}", type=dict,
                        default={"username": "a", "password": "b"})
    parser.add_argument("-t", "--target", help="Target args", type=str, default="username")
    parser.add_argument("-s", "--script", help="script name", type=str)
    parser.add_argument("-c", "--csv", help="The csv file path", type=str)
    return parser.parse_args()


def default_header():
    header = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept-Encoding': 'gzip, deflate, br, zstd'
    }
    return header

def default_proxies():
    proxies = {
        "http": 'http://127.0.0.1:9003',
        "https": 'http://127.0.0.1:9003'
    }
    return proxies