import requests
import json


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
    'Host':'music.163.com',
    'Origin': 'https://music.163.com',
    'Referer': 'https://music.163.com/song?id=480580003',
}
data = {
    'params':'IGNqvT0rESOaQO9xQ+qHjYhTPThx0ysksHpD3a1vtPRjMwxdAV1Yuq/ndOvf456gS+gq+74NtrVsB6IjifAIMTmbpiITP5/EiS945SYtO9tDUZy6UOj3hQM+h29nFiZrJmi8dIHoSju6qc/0xTB4ep8Q/AcjzYHMAJS0vqwOfGJx7qzWPOcSyKdgZSihKsLf',
    'encSecKey':'6745bf70ca8738fe6abc94f6582fcbc600b51d47dccf816cd7bd742b2b55dd2441dafd485067f7c5df60decce5be7274e776bbe5f5a4aa980f6a232a7040498f049e071bec6d8bc12fd83735f84f2afe3876b642a1d88679bf0d20bb7df96a3bf2f3fcb46d46f35d0068a0b02013eeb493a2d70b6aabb63274eb42e7aa014668'
}


url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_432506345?csrf_token='

comments_json = requests.post(url,data=data).text
comments = json.loads(comments_json)

for i in comments['hotComments']:
    print(i['user']['nickname']+str(i['likedCount'])+i['content'])