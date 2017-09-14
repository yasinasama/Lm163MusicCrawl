# -*- coding: gbk -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import dbutil
import requests
import json


class Singer:
    def __init__(self):
        self.driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
        self.re_id = re.compile('\d+')
        self.table = 'singer'
        self.column = 'user_id,user_name'
        self.conn = dbutil.Database(user='root', passwd='', db='wy_music')

    def _get_url(self):
        self.cat_ids = ['1001', '1002', '1003',
                        '2001', '2002', '2003',
                        '6001', '6002', '6003',
                        '7001', '7002', '7003',
                        '4001', '4002', '4003']
        self.initial = [-1, 0] + ([65 + i for i in range(26)])
        for i in self.cat_ids:
            for j in self.initial:
                yield 'https://music.163.com/#/discover/artist/cat?id=%s&initial=%s' % (i, j)

    def _get_page_source(self, url):
        try:
            self.driver.get(url)
            self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe"))
            return self.driver.page_source
        except Exception as e:
            print(e)

    def _quit_driver(self):
        self.driver.quit()

    # 你不会知道某些歌手的名字里有单引号-0-
    def format_str(self, str):
        return '\'' + str.replace('\'', '') + '\''

    def crawl(self):
        for url in self._get_url():
            soup = BeautifulSoup(self._get_page_source(url), "html.parser")
            items = soup.find(id='m-artist-box').find_all('li')
            for i in range(len(items)):
                if i < 10:
                    id = re.search(self.re_id, items[i].p.a['href']).group()
                    name = items[i].p.a.text
                else:
                    id = re.search(self.re_id, items[i].a['href']).group()
                    name = items[i].a.text
                values = ','.join((str(id), self.format_str(name)))
                print(values)
                self.conn.insert(table=self.table, column=self.column, values=values)
        self.conn.close()
        self._quit_driver()


class HotSong:
    def __init__(self):
        self.table = 'hot_song'
        self.column = 'singer_id,song_id,song_name,album_id,album_name'
        self.conn = dbutil.Database(user='root', passwd='', db='wy_music')

    def _get_url(self, **kwargs):
        urls = []
        ids = self.conn.select(**kwargs)
        for id in ids:
            urls.append('https://music.163.com/artist?id=%s' % id)
        return urls

    def format_str(self, str):
        if str and len(str) > 0:
            return '\'' + str.replace('\'', '').replace('\\', '\\\\') + '\''
        else:
            return '\'' + '无此信息！！！！！' + '\''

    def crawl(self):
        _from = 0
        limit = 100
        success = False
        while not success:
            res = self._get_url(column='singer_id', table='singer', _from=_from, limit=limit)
            if len(res) >= 1:
                print(_from)
                for url in res:
                    print(url)
                    try:
                        req = requests.get(url, timeout=10)
                        soup = BeautifulSoup(req.text, 'html.parser')
                        text = soup.find(id='song-list-pre-cache').find('textarea').text
                        songs = json.loads(text)
                    except Exception as e:
                        self.conn.insert(table='failure', column='url,note', values=','.join((self.format_str(url), self.format_str(str(e)))))
                        continue
                    for song in songs:
                        singer_id = song['artists'][0]['id']
                        song_id = song['id']
                        song_name = song['name']
                        album_id = song['album']['id']
                        album_name = song['album']['name']
                        print(singer_id, song_id, song_name, album_id, album_name)
                        values = ','.join((self.format_str(str(singer_id)),
                                           self.format_str(str(song_id)),
                                           self.format_str(song_name),
                                           self.format_str(str(album_id)),
                                           self.format_str(album_name)))
                        self.conn.insert(table=self.table, column=self.column, values=values)
                _from += limit
            else:
                success = True
        self.conn.close()


if __name__ == '__main__':
    s = HotSong()
    s.crawl()
