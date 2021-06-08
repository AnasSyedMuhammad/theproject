#!/usr/bin/env python3
# coding: utf-8

import re
import sys
import argparse
import multiprocessing
import threading
import socket
import urllib.parse as urlparse
import urllib.parse as urllib
import time

try:
    import requests.packages.urllib3

    requests.packages.urllib3.disable_warnings()
except:
    pass


def banner():
    print()

def subdomain_sorting_key(domain_name):  # hostname changed to domain name - domain name
    parts = domain_name.split('.')[::-1]
    if parts[-1] == 'www':
        return parts[:-1], 1
    return parts, 0


class enumratorBase(object):
    def __init__(self, base_url, search_engine, domain, subdomains=None):  # engine_name changed to search_engine
        subdomains = subdomains or []
        self.domain = urlparse.urlparse(domain).netloc
        self.session = requests.Session()
        self.subdomains = []
        self.timeout = 25
        self.base_url = base_url
        self.search_engine = search_engine
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept-Encoding': 'gzip',
        }
        self.print_banner()

    def print_(self, text):
        print(text)
        return text

    def print_banner(self):
        self.print_("Searching %s.." % (self.search_engine))
        return "Searching %s.." % (self.search_engine)

    def send_req(self, query, page_no=1):

        url = self.base_url.format(query=query, page_no=page_no)
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None
        return self.get_response(resp)

    def get_response(self, response):
        if response is None:
            return 0
        return response.text if hasattr(response, "text") else response.content


class enumratorBaseThreaded(multiprocessing.Process, enumratorBase):
    def __init__(self, base_url, search_engine, domain, subdomains=None, q=None):
        subdomains = subdomains or []
        enumratorBase.__init__(self, base_url, search_engine, domain, subdomains)
        multiprocessing.Process.__init__(self)
        self.q = q
        return

    def run(self):
        domain_list = self.enumerate()
        for domain in domain_list:
            self.q.append(domain)


class CrtSearch(enumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None):
        subdomains = subdomains or []
        base_url = 'https://crt.sh/?q=%25.{domain}'
        self.search_engine = "SSL Certificates"
        self.q = q
        super(CrtSearch, self).__init__(base_url, self.search_engine, domain, subdomains, q=q)
        return

    def req(self, url):
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None

        return self.get_response(resp)

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        resp = self.req(url)
        if resp:
            self.extract_domains(resp)
        return self.subdomains

    def extract_domains(self, resp):
        link_regx = re.compile('<TD>(.*?)</TD>')
        try:
            links = link_regx.findall(resp)
            for link in links:
                link = link.strip()
                subdomains = []
                if '<BR>' in link:
                    subdomains = link.split('<BR>')
                else:
                    subdomains.append(link)

                for subdomain in subdomains:
                    if not subdomain.endswith(self.domain) or '*' in subdomain:
                        continue

                    if '@' in subdomain:
                        subdomain = subdomain[subdomain.find('@') + 1:]

                    if subdomain not in self.subdomains and subdomain != self.domain:
                        self.subdomains.append(subdomain.strip())
        except Exception as e:
            print(e)
            pass


class Scan_Ports():
    def __init__(self, subdomains, ports):
        self.subdomains = subdomains
        self.ports = ports
        self.lock = None

    def port_scan(self, host, ports):
        openports = []
        self.lock.acquire()
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                result = s.connect_ex((host, int(port)))
                if result == 0:
                    openports.append(port)
                s.close()
            except Exception:
                pass
        self.lock.release()
        if len(openports) > 0:
            print("%s - Currently Open ports : %s" % (host, ", ".join(openports)))
            return "%s - Currently Open ports : %s" % (host, ", ".join(openports))

    def run(self):
        self.lock = threading.BoundedSemaphore(value=20)
        for subdomain in self.subdomains:
            t = threading.Thread(target=self.port_scan, args=(subdomain, self.ports))
            t.start()


def main(domain):  # ports changed to port_no in main function
    s_domainLen=None
    s_port=None
    search_list = set()
    subdomains_queue = multiprocessing.Manager().list()
    domain_check = re.compile("^(http|https)?[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$")
    if not domain_check.match(domain):
        print("Error: Please enter a valid domain")
        return ["Error: Please enter a valid domain"]

    if not domain.startswith('http://') or not domain.startswith('https://'):
        domain = 'http://' + domain

    parsed_domain = urlparse.urlparse(domain)

    print("Finding subdomains for %s" % parsed_domain.netloc)

    find="Finding subdomains for %s" % parsed_domain.netloc


    supported_engines = {'ssl': CrtSearch}

    chosenEnums = []

    chosenEnums = [
        CrtSearch
    ]

    enums = [enum(domain, [], q=subdomains_queue) for enum in chosenEnums]
    for enum in enums:
        enum.start()
    for enum in enums:
        enum.join()

    subdomains = set(subdomains_queue)
    for subdomain in subdomains:
        search_list.add(subdomain)

    if subdomains:
        subdomains = sorted(subdomains, key=subdomain_sorting_key)

        print("Subdomains: %s" % len(subdomains))
        s_domainLen="Subdomains: %s" % len(subdomains)


        for subdomain in subdomains:
            print(subdomain)
    return find,s_domainLen,subdomains



