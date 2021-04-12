#!/usr/bin/python3

import os
import re
import sys
import traceback
import requests

from retry import retry

DOMAIN_NAME = [
    "github.com", "github.io", "api.github.com",
    "avatars.githubusercontent.com", "avatars0.githubusercontent.com",
    "avatars1.githubusercontent.com", "avatars2.githubusercontent.com",
    "avatars3.githubusercontent.com", "avatars4.githubusercontent.com",
    "avatars5.githubusercontent.com", "favicons.githubusercontent.com",
    "raw.githubusercontent.com", "user-images.githubusercontent.com",
    "github.githubassets.com", "central.github.com",
    "desktop.githubusercontent.com", "assets-cdn.github.com",
    "camo.githubusercontent.com", "github.map.fastly.net",
    "github.global.ssl.fastly.net", "gist.github.com", "codeload.github.com",
    "github-cloud.s3.amazonaws.com", "github-com.s3.amazonaws.com",
    "github-production-release-asset-2e65be.s3.amazonaws.com",
    "github-production-user-asset-6210df.s3.amazonaws.com",
    "github-production-repository-file-5c1aeb.s3.amazonaws.com",
    "githubstatus.com", "github.community", "media.githubusercontent.com"
]

IPADDRESS_URL = "https://www.ipaddress.com/ip-lookup"
HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}

HOSTS_BEGIN = "# GitHub Host Begin"
HOSTS_END = "# GitHub Host End"
HOSTS_TEMPLATE = """{}{}
{}\n"""

HOSTS_PATH_WIN = "C:\\Windows\\System32\\drivers\\etc\\hosts"
HOSTS_PATH_LINUX = "/etc/hosts"


def write_hosts_file(hosts_content: str):
    hosts_file_path = ""
    if sys.platform.startswith("win32"):
        hosts_file_path = HOSTS_PATH_WIN
    elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        hosts_file_path = HOSTS_PATH_LINUX

    with open(hosts_file_path, "r+") as f:
        old_content = f.read()
        f.truncate(0)
        f.seek(0)
        begin_pos = old_content.find(HOSTS_BEGIN)
        end_pos = old_content.find(HOSTS_END)
        if begin_pos != -1:
            f.write(old_content[:begin_pos])
        else:
            f.write(old_content)
        f.write(hosts_content)
        if end_pos != -1:
            f.write(old_content[end_pos + len(HOSTS_END) + 1:len(old_content)])


@retry(tries=3)
def get_ip(session: requests.session, domain: str):
    payload = {"host": domain}
    try:
        res = session.post(IPADDRESS_URL,
                           headers=HEADERS,
                           data=payload,
                           timeout=5)
        html = res.text
        begin = html.find("<main>")
        end = html.find("</main>")
        if begin == -1 or end == -1:
            raise Exception("ip address is empty!")
        html = html[begin:end]
        pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        ip_list = re.findall(pattern, html)
        if len(ip_list) != 0:
            return list(set(ip_list))
        raise Exception("ip address is empty!")
    except Exception as ex:
        print("get: {}, error: {}".format(domain, ex))
        raise


def main():
    session = requests.session()
    content = ""
    i = 0
    size = len(DOMAIN_NAME)
    while i < size:
        print("{}/{}  {}".format(i + 1, size, DOMAIN_NAME[i]))
        try:
            ip_list = get_ip(session, DOMAIN_NAME[i])
            for ip in ip_list:
                content += "\n" + ip.ljust(30) + DOMAIN_NAME[i]
        except Exception:
            pass
        i += 1

    if not content:
        return

    hosts_content = HOSTS_TEMPLATE.format(HOSTS_BEGIN, content, HOSTS_END)
    write_hosts_file(hosts_content)
    print("update completed!")
    if sys.platform.startswith("win32"):
        os.system("ipconfig /flushdns")


if __name__ == '__main__':
    main()
