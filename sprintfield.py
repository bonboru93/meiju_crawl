# coding: utf-8
import requests
from lxml import html
from googletrans import Translator
import time


def trans(origin):
    result = ''
    translator = Translator()
    translated = '-1'
    while translated == '-1':
        try:
            translated = translator.translate(origin, src='en', dest='zh-CN').text
        except:
            time.sleep(10)
            continue
    sentence_count = 0
    origin_sentence = origin.split('\n')
    for sentence_translated in translated.split('\n'):
        result += origin_sentence[sentence_count] + '\n'
        result += '=>' + sentence_translated + '\n'
        sentence_count += 1
    return result


def springfiledfetch(sname, season):
    print 'Now guessing the script page url'
    page = requests.get(url='https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=' + sname,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}).text
    if page.find('href="view_episode_scripts.php?') < 0:
        year = 2017
        while True:
            page = requests.get(url='https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=' + sname + '-' + str(year),
                                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}).text
            if page.find('href="view_episode_scripts.php?') >= 0 or year < 2000:
                break
            year -= 1
    if page.find('href="view_episode_scripts.php?') < 0:
        para = raw_input('Script no found, please manually type the parameter: ')
        page = ''
        while not page:
            page = requests.get(url='https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=' + para,
                                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}).text
    else:
        print 'Script page found'
    try:
        url = html.fromstring(page).xpath('//div[@class="season-episodes"]/h3[@id="season' + season + '"]/../a/@href')[0].lower()
    except:
        print 'Current season no found, use the first link instead'
        url = html.fromstring(page).xpath('//a[contains(@href, "view_episode_scripts.php?")]/@href')[0].lower()
    page = requests.get(url='https://www.springfieldspringfield.co.uk/' + url,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}).text
    page = html.fromstring(page).xpath('//div[@class="scrolling-script-container"]/text()')

    result = ''
    origin = ''
    for sentence in page:
        new_sentence = sentence.replace('\n', '').replace('\r', '').replace('\t', '') + '\n'
        if len(origin) + len(new_sentence) < 5000:
            origin += new_sentence
        else:
            result += trans(origin)
            origin = ''
    result += trans(origin)
    return result

if __name__ == '__main__':
    springfiledfetch('blindspot', '10')