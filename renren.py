# coding: utf-8
import requests
from lxml import html
import re


def renrenfetch(url):
    print 'Downloading renren page'
    page = requests.get(url).content.decode('utf-8')
    page = html.fromstring(page)
    title = page.xpath('//title/text()')[0]
    name = title[title.find(u'《') + len(u'《'): title.find(u'》')]
    if title.find(u'第') >= 0 and title.find(u'季') >= 0:
        season = title[title.find(u'第') + len(u'《'): title.find(u'季')]
    else:
        season = '1'
    ename = page.xpath(u'//span[text()="原名："]/../strong/text()')[0]
    sname = ''
    for word in re.findall(re.compile('\w+'), ename):
        sname += word + '-'
    sname = sname.lower()[:-1]
    pic = page.xpath('//div[@class="imglink"]//img/@src')[0]
    desc = page.xpath('//div[@class="resource-desc"]')[0].xpath('string()').strip()
    print sname, season, name
    return [sname, season, name, ename, pic, desc]

if __name__ == '__main__':
    renrenfetch('http://www.zimuzu.tv/resource/34004')
