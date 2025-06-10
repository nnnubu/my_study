from pprint import pprint
import requests, re, json, os
from moviepy.editor import *
from pymediainfo import MediaInfo


def generate_unique_filename(path, title, extension):
    base = title
    counter = 1
    while os.path.exists(os.path.join(path, f"{title}{extension}")):
        title = f"{base}({counter})"
        counter += 1
    return title


url = ''

cookie = ''

header = {
    "referer": "https://www.bilibili.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
}

resp = requests.get(url, headers=header)
html = re.findall(r'window.__playinfo__=(.*?)</script>', resp.text, re.S)
datas = json.loads(html[0])
quality = datas['data']['quality']

if quality >= 80:
    temp = re.findall(r'<h1 data-title="(.*?)"', resp.text, re.S)[0]
    title = re.sub(r'[<>:"/\|?*]', "", temp)
    video_url = datas['data']['dash']['video'][0]['baseUrl']
    audio_url = datas['data']['dash']['audio'][0]['baseUrl']

    path = '../../../爬虫战果/视频/'
    if not os.path.exists(path):
        os.makedirs(path)

    title = generate_unique_filename(path, title, '.mp4')

    video = requests.get(video_url, headers=header)
    audio = requests.get(audio_url, headers=header)

    with open(f"{path}{title}0.mp4", 'wb') as f:
        f.write(video.content)
        print('视频下载完成！')
    with open(f"{path}{title}1.mp3", 'wb') as f:
        f.write(audio.content)
        print('音频下载完成！')

    resp.close()
    video.close()
    audio.close()

    vdname = path + title + '0.mp4'
    adname = path + title + '1.mp3'

    try:
        vd = VideoFileClip(vdname)
        ad = AudioFileClip(adname)
        vd = vd.set_audio(ad)
        vd.write_videofile(f'{path}{title}.mp4')
    finally:
        os.remove(vdname)
        os.remove(adname)
else:
    print('视频画质太低！请检查cookie是否过期！')
