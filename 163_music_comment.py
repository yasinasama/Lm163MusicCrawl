import requests
import json
import dbutil
from datetime import datetime


class comment:
    def __init__(self):
        # self.headers = headers = {
        #     'User-Agent': 'Mozilla/5.0 (
        # Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
        # }
        self.data = {
            'params': 'IGNqvT0rESOaQO9xQ+qHjYhTPThx0ysksHpD3a1vtPRjMwxdAV1Yuq/ndOvf456gS+gq+74NtrVsB6IjifAIMTmbpiITP5/EiS945SYtO9tDUZy6UOj3hQM+h29nFiZrJmi8dIHoSju6qc/0xTB4ep8Q/AcjzYHMAJS0vqwOfGJx7qzWPOcSyKdgZSihKsLf',
            'encSecKey': '6745bf70ca8738fe6abc94f6582fcbc600b51d47dccf816cd7bd742b2b55dd2441dafd485067f7c5df60decce5be7274e776bbe5f5a4aa980f6a232a7040498f049e071bec6d8bc12fd83735f84f2afe3876b642a1d88679bf0d20bb7df96a3bf2f3fcb46d46f35d0068a0b02013eeb493a2d70b6aabb63274eb42e7aa014668'
        }
        self.conn = dbutil.Database(user='root', passwd='', db='wy_music')
        self.limit = 100
        self.column = 'song_id,comment_id,comment_content,comment_count,comment_time'
        self.table = 'hot_comment'
        self._from = 0

    def selectSongId(self):
        res = self.conn.select(column='song_id', table='hot_song', _from=self._from, limit=self.limit)
        if len(res) >= 1:
            self._from += self.limit
            return res
        else:
            return []

    def format_str(self, str):
        if str and len(str) > 0:
            return '\'' + str.replace('\'', '').replace('\\', '\\\\') + '\''
        else:
            return '\'' + '无此信息！！！！！' + '\''

    def loadComment(self):
        done = False
        while not done:
            result = self.selectSongId()
            for res in result:
                url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token=' % res
                req = requests.post(url, data=self.data)
                comments = json.loads(req.text)
                for i in comments['hotComments']:
                    song_id = res[0]
                    comment_id = i['user']['nickname']
                    comment_content = i['content']
                    comment_count = i['likedCount']
                    comment_time = datetime.strftime(datetime.fromtimestamp(i['time'] / 1000), '%Y-%m-%d %H:%M:%S')

                    values = ','.join((self.format_str(str(song_id)),
                                       self.format_str(str(comment_id)),
                                       self.format_str(comment_content),
                                       self.format_str(str(comment_count)),
                                       self.format_str(comment_time)))
                    print(values)
                    self.conn.insert(table=self.table,column=self.column,values=values)

if __name__ == '__main__':
    comment = comment()
    comment.loadComment()
