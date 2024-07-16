# 此方式只能用于下载网易云非vip歌曲
# 码率：128k

import json
import os
import pandas as pd
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB

# 读取 JSON 文件
with open('1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 获取 'tracks' 列表
tracks = data.get('playlist', {}).get('tracks', [])

# 提取需要的字段
extracted_tracks = []
for track in tracks:
    # 构建一个新的字典，只包含需要的字段
    # 使用 .get() 方法来安全地获取可能不存在的字段
    track_info = {
        'name': track.get('name', ''),  # 如果 'name' 字段不存在，使用空字符串作为默认值
        'id': track.get('id', ''),      # 如果 'id' 字段不存在，使用空字符串作为默认值
        'ar_name': track.get('ar', [{}])[0].get('name', '') if track.get('ar', []) else '',  # 提取第一个艺术家的 'name'
        'alia': track.get('alia', [None])[0] if track.get('alia', []) else '',  # 提取别名数组中的第一个别名
        'al_name': track.get('al', {}).get('name', '')  # 提取专辑的 'name'
    }
    extracted_tracks.append(track_info)

# 将提取的数据转换为 pandas DataFrame
df = pd.DataFrame(extracted_tracks)

# 确保 'music' 文件夹存在
music_dir = 'music'
if not os.path.exists(music_dir):
    os.makedirs(music_dir)

for index, row in df.iterrows():
    download_url = f"http://music.163.com/song/media/outer/url?id={row['id']}.mp3"
    clean_ar_name = row['ar_name'] if row['ar_name'] is not None else 'Unknown Artist'
    clean_name = row['name'] if row['name'] is not None else 'Unknown Title'
    clean_al_name = row['al_name'] if row['al_name'] is not None else 'Unknown Album'
    
    # 清理文件名中的非法字符
    clean_ar_name = clean_ar_name.replace('/', '-').replace('\\', '-').replace('|', '-').replace(':', '-').replace('"', '').replace('?', '').replace('*', '')
    clean_name = clean_name.replace('/', '-').replace('\\', '-').replace('|', '-').replace(':', '-').replace('"', '').replace('?', '').replace('*', '')
    clean_al_name = clean_al_name.replace('/', '-').replace('\\', '-').replace('|', '-').replace(':', '-').replace('"', '').replace('?', '').replace('*', '')
    
    file_name = f"{clean_ar_name} - {clean_name}.mp3"
    save_path = os.path.join(music_dir, file_name)
    
    try:
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # 使用mutagen加载现有的ID3标签
            audio = MP3(save_path, ID3=ID3)
            if audio.tags is None:
                audio.add_tags()  # 如果没有标签，添加新的标签
            audio.tags.add(TIT2(encoding=3, text=clean_name))  # 更新标题
            audio.tags.add(TPE1(encoding=3, text=clean_ar_name))  # 更新艺术家
            audio.tags.add(TALB(encoding=3, text=clean_al_name))  # 更新专辑
            audio.save()
            
            # print(f"Downloaded and tagged:  {row['id']}\t{file_name}")
        else:
            print(f"Failed to download: {row['id']}\t{file_name}")
    except Exception as e:
        print(f"Error processing file {row['id']}\t{file_name}: {e}")