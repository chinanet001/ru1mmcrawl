import requests
s = requests.Session()

host = 'http://www.ru1mm.com'
# host = 'http://127.0.0.1:8888'
login = '/user/login'

headers = {'Host': 'www.ru1mm.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate'}

# NOTE: deprecated cookies
cookies0 = {
    'Hm_lvt_45e31f483c965dbbceecd5f26390d8f6': '1442715462',
    'Hm_lpvt_45e31f483c965dbbceecd5f26390d8f6': '1442725058',
    'bdshare_firstime': '1442715462237'
}

r0 = s.get('http://www.ru1mm.com', headers=headers)
username = raw_input('username:')
password = raw_input('password:')
payload = {'username': username, 'password': password, 'current_url': 'http://www.ru1mm.com'}
h = headers.copy()
h['Content-Type'] = 'application/x-www-form-urlencoded'
h['Referer'] = 'http://www.ru1mm.com/'
# cookies = cookies0.copy()
# for cookie in s.cookies:
#     cookies[cookie.name] = cookie.value
# print cookies
r1 = s.post('%s%s' % (host, login), data=payload, headers=h)#, cookies=cookies)
r2 = s.get(host, headers=headers, cookies=s.cookies)
print r2.content.find(username)
import ipdb; ipdb.set_trace()

print(r1.text)
# '{"cookies": {"sessioncookie": "123456789"}}'