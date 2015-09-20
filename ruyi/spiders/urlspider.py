from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.http.cookies import CookieJar
from urlparse import urlparse
from ruyi.items import RuyiItem
from json import loads as jloads

class UrlSpider(InitSpider):
    name = "ruyiurls"
    main_page = 'http://www.ru1mm.com'
    login_page = 'http://www.ru1mm.com/user/login'
    download_page = 'http://www.ru1mm.com/album/download'
    captcha_refresh_page = 'http://www.ru1mm.com/rcaptcha/refresh'
    allowed_domains = ["ru1mm.com"]
    # start_urls = [
    #     "http://www.ru1mm.com/album",
    # ]
    start_urls = []
    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.main_page, callback=self.login, dont_filter=True)
 
    def login(self, response):
        """Generate a login request."""
        self.username = raw_input('username:')
        self.password = raw_input('password:')
        return FormRequest(url=self.login_page,
            formdata={'username': self.username, 'password': self.password,
                      'current_url': 'http://www.ru1mm.com'},
                      # headers={'Content-Type':'application/x-www-form-urlencoded'},
                    callback=self.redirect_home) 

    def redirect_home(self, response):
        return Request(url=self.main_page, callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        # print self.username in response.body
        # import ipdb; ipdb.set_trace()
        if self.username in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            return Request(url=self.captcha_refresh_page, callback=self.captcha_confirm)
        else:
            self.log("Bad times :(")

    def captcha_confirm(self, response):
        self.captcha_url = response.body.strip()
        print(self.captcha_url)
        self.captcha = raw_input('cap word:')
        return self.initialized()

    def start_requests(self):
        # items = jloads(open('items.json').read())
        # ids = [ item['urlid'] for item in items ]
        for viewid in range(970):
        # for viewid in range(20):
            # if str(viewid) in ids: continue
            self.start_urls.append('http://www.ru1mm.com/album/view/%s' % viewid)
        # if len(self.start_urls) == 0:
        #     return
        # print '-=====> %s' % len(self.start_urls)
        # print self.start_urls
        return super(UrlSpider, self).start_requests()

    def parse(self, response):
        print(response.url)
        urlobj = urlparse(response.url)
        if urlobj.path.startswith('/album/view/'):
            urlid = urlobj.path.split('/')[-1]
            herosrclst = response.xpath('//div[@class="hero"]/img/@src')
            if herosrclst:
                herosrc = herosrclst[0].extract()
            else:
                herosrc = ''
            # construct a form
            return FormRequest(url=self.download_page, formdata={'cap_img': self.captcha_url,
                'cap_word': self.captcha,
                'album_id': urlid,
                },
                meta={'handle_httpstatus_list': [302], 'dont_redirect': True, '__urlid': urlid,
                      '__herosrc': herosrc},
                callback=self.process_download_response)

        # # print self.start_urls
        # return 
        # t = response.xpath('//button[@id="pre_download_btn"]')
        # import ipdb; ipdb.set_trace()
        # for url in response.xpath('//a/@href').extract():
        #     urlobj = urlparse(url)
        #     if urlobj.path.startswith('/album/view/'):
        #         urlid = urlobj.path.split('/')[-1]
        #         item = RuyiItem()
        #         item['urlid'] = urlid
        #         yield item
        #     if urlobj.path.startswith('/album/ls/'):
        #         yield Request(url=urlobj.geturl(), callback=self.parse,priority=1)

    def process_download_response(self, response):
        item = RuyiItem()
        item['urlid'] = response.meta['__urlid']
        item['dpath'] = response.headers['Location']
        item['cover'] = response.meta['__herosrc']
        return item
