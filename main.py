import pandas as pd
import json


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

# 查看 DataFrame 的前几行
print(df.head())

# 将 DataFrame 保存为 CSV 文件
df.to_csv('selected_output.csv', index=False, encoding='utf-8')


