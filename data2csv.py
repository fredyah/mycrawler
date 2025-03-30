import pandas as pd
import re

def remove_emojis(text):
    # 這個 pattern 可以匹配大部分常見的 emoji
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # 表情符號
        "\U0001F300-\U0001F5FF"  # 符號 & 圖形
        "\U0001F680-\U0001F6FF"  # 交通 & 地圖符號
        "\U0001F1E0-\U0001F1FF"  # 國旗
        "\U0001F900-\U0001F9FF"  # 補充符號與圖形
        "\U0001FA70-\U0001FAFF"  # 擴展 emoji 區段 (根據需要加入)
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

data = []

with open('links.txt', 'r', encoding = 'utf-8-sig') as f:
    for aa in f.readlines():
        for bb in aa.split('title="'):
            if "href" in '"'.join(bb.split('"')[:6]):
                if "/shorts/" in bb or "/watch?" in '"'.join(bb.split('"')[:6]):
                    titlE = '"'.join(bb.split('"')[:6]).split('"')[0]
                    hreF = '"'.join(bb.split('"')[:6]).split('href="')[1].split('"')[0]

                    data.append([remove_emojis(titlE), f"https://www.youtube.com{hreF}"])

df = pd.DataFrame(data)

df.drop_duplicates(subset=[df.columns[0]], inplace=True)

df.to_csv('youtube_list.csv', index=False)


