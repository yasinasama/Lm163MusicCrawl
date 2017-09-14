**网易云歌手信息、歌手HOT SONG、评论抓取**

| singer---歌手 |
|:-------:|:-------|
| singer_id | varchar(50) |
| singer_name| varchar(200) |

| hot_song---热歌 |
|:-------:|:-------|
| singer_id | varchar(50) |
| song_id | varchar(50) |
| song_name | varchar(200) |
| album_id | varchar(50) |
| album_name | varchar(200) |

| hot_comment---热评 |
|:-------:|:-------|
| song_id | varchar(50) |
| comment_id | varchar(255) |
| comment_content | varchar(2048) |
| comment_count | varchar(50) |
| comment_time | datetime |