# coding: utf-8
import requests
import urllib
from lxml import html
import gevent
from gevent import monkey
import json
monkey.patch_all()
import csv

douban_cookie_str = r'll="119088"; bid=Seow47BBwvU; ps=y; ue="469886000@qq.com"; dbcl2="57858884:wYz2Fw3QFBw"; ck=nPgK; __utmt=1; ap=1; __utma=30149280.644121503.1513760093.1513760093.1513761703.2; __utmb=30149280.13.9.1513765142684; __utmc=30149280; __utmz=30149280.1513761703.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.5785; __utma=223695111.2011756647.1513760093.1513760093.1513761703.2; __utmb=223695111.0.10.1513761703; __utmc=223695111; __utmz=223695111.1513761703.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_id.100001.4cf6=2255e3c5b36bd2f3.1513760093.1.1513765335.1513760093.; _pk_ses.100001.4cf6=*; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=413E7A5E5C24F6EADBA62CE05C070C68|4900066aa80768c5f3eaf637ccf16a96'
cookies = {}
for line in douban_cookie_str.split(';'):
    name, value = line.strip().split('=', 1)
    cookies[name] = value


def load(index):
    global count
    global result
    page = ''
    while not page:
        try:
            page = requests.get(url='https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28287&from_mid=1&format=json&ie=utf-8&oe=utf-8&query=%E7%BE%8E%E5%89%A7%E5%A4%A7%E5%85%A8&sort_key=16&sort_type=1&pn=' + str(index),
                                headers={"connection": "close"}).text
        except:
            print 'list error'
            continue
    page = json.loads(page)['data'][0]['result']
    for item in page:
        name = item['name']
        pos = -1
        if name.find(u'4400') >= 0:
            season = name[-1]
            name = '4400'
        else:
            while u'0' <= name[pos] <= u'9':
                pos -= 1
            if pos == -1:
                season = '1'
            else:
                season = name[pos + 1:]
                name = name[:pos + 1]
        pic = item['pic_6n_161']
        addit = item['additional']
        if addit.find(u'全') >= 0 and addit.rfind(u'集') >= 0:
            addit = addit[addit.find(u'全') + len(u'全') : addit.rfind(u'集')]
        else:
            addit = '0'

        douban = ''
        while not douban:
            try:
                douban = requests.get(url='https://www.baidu.com/s?wd=' + urllib.quote((name + u' 第' + season + u'季 site:movie.douban.com').encode('utf-8')),
                                      headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                                               'connection': 'close'}).text
            except Exception, e:
                print repr(e)
                print name, season
                continue
        try:
            douban = html.fromstring(douban).xpath('//div[@id="1"]/h3/a/@href')[0]
        except:
            print name, season
            continue
        resp = ''
        while not resp:
            try:
                resp = requests.get(url=douban,
                                    cookies=cookies,
                                    headers={"connection": "close"})
            except Exception, e:
                print douban
                print repr(e)
                raw_input('input checkcode')
                continue
        douban_link = resp.url
        douban = html.fromstring(resp.text)
        try:
            douban_score = douban.xpath('//strong[@property="v:average"]/text()')[0]
        except:
            douban_score = '0'
        try:
            desc = douban.xpath('//span[@property="v:summary"]')[0].xpath('string()').strip()
        except:
            desc = ' '
        try:
            imdb_link = douban.xpath('//a[contains(@href, "www.imdb.com/title/")]/@href')[0]
            imdb = html.fromstring(requests.get(url=imdb_link,
                                                headers={"connection": "close"}).text)
            ename = imdb.xpath('//h1[@itemprop="name"]/text()')[0].strip()
            imdb_score = imdb.xpath('//span[@itemprop="ratingValue"]/text()')[0]
            edesc = imdb.xpath('//div[@itemprop="description"]/text()')[0].strip()
        except:
            imdb_link = ename = imdb_score = edesc = ' '
        #print name, ename, season, douban_score, imdb_score, desc, edesc
        result.writerow([name.encode('utf-8'), ename.encode('utf-8'), season.encode('utf-8'), addit.encode('utf-8'), douban_link.encode('utf-8'), douban_score.encode('utf-8'), imdb_link.encode('utf-8'), imdb_score.encode('utf-8'), pic.encode('utf-8'), desc.encode('utf-8'), edesc.encode('utf-8')])
        count += 1
        print count
        gevent.sleep(2)

count = 0
result = csv.writer(open('meiju2.csv', 'wb'))
event_list = []
for i in range(0, 10):
    event_list.append(gevent.spawn(load, i * 8))
gevent.joinall(event_list)

#load(0)
