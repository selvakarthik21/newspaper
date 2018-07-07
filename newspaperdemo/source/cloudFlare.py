from selenium import webdriver
from time import sleep
import cookielib
import requests

def getCloudFlareContent(url):
    print ('Launching Firefox..')
    browser = webdriver.Firefox()
    print ('Entering to skidpaste.org...')
    browser.get('http://skidpaste.org')
    print ('Waiting 10 seconds...')
    sleep(10)
    a = browser.get_cookies()
    print('Got cloudflare cookies:\n')
    print('Closing Firefox..')
    browser.close()
    
    h = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0'}
    
    b = cookielib.CookieJar()
    
    for i in a:
      ck = cookielib.Cookie(name=i['name'], value=i['value'], domain=i['domain'], path=i['path'], secure=i['secure'], rest=False, version=0,port=None,port_specified=False,domain_specified=False,domain_initial_dot=False,path_specified=True,expires=i['expiry'],discard=True,comment=None,comment_url=None,rfc2109=False)
      b.set_cookie(ck)
    
    r = requests.get('http://skidpaste.org', cookies=b, headers=h)
    print(r.content)
    return r.content

