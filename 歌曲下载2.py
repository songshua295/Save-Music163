# 该方式并不稳定，建议直接网站搜。
# 请求 https://hayqbhgr.slider.kz/ 网站的api，爬取的歌曲。
# 因为是根据歌名来进行的搜索的，而这里仅仅是根据首选来进行下载，所以难免会出现错误。

import requests
import json
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TPE1, TIT2, error

def downMusic(songname):
    # 目标URL
    url = f"https://hayqbhgr.slider.kz/vk_auth.php?q={songname}" 

    # 设置请求头，模拟PC浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 发送GET请求，携带请求头
    response = requests.get(url, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        # 加载JSON数据
        data = json.loads(response.text)

        # 访问audios键下的第一个列表的第一个元素
        first_audio = data["audios"][""][0]

        # 获取tit_art和url
        tit_art = first_audio["tit_art"]
        audio_url = first_audio["url"]

        # 打印结果
        print("标题:", tit_art)
        print("url：", audio_url)

        # 下载文件
        download_response = requests.get(audio_url, headers=headers)
        if download_response.status_code == 200:
            # 确保music2文件夹存在
            os.makedirs('music2', exist_ok=True)
            file_path = f'music2/{songname}.mp3'
            
            # 写入文件
            with open(file_path, 'wb') as f:
                f.write(download_response.content)
            
            # 解析歌手和歌曲名称
            artist, title = songname.split(' - ')
            
            # 加载ID3标签
            try:
                audio = MP3(file_path, ID3=ID3)
                audio.add_tags()  # 尝试添加标签
            except error as e:
                print(f"添加标签时出错：{e}")  # 打印错误信息
                audio = MP3(file_path)  # 直接加载现有的标签
            
            # 设置标签
            audio['TPE1'] = TPE1(encoding=3, text=artist)
            audio['TIT2'] = TIT2(encoding=3, text=title)
            audio.save()
            
            print("文件已下载并标签已更新")
        else:
            print("文件下载失败，状态码：", download_response.status_code)
    else:
        print("请求失败，状态码：", response.status_code)

# 使用示例
songname=input("请输入歌手-歌曲名称")
downMusic(songname)