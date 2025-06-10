from os import error

import requests, re, json, pprint, os, tqdm
from urllib.parse import unquote
from rich.progress import track
from moviepy.editor import *
from natsort import natsorted
from PIL import Image

headers = {
    'referer': 'https://www.douyin.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
}

# cookie = ''

def get_video():
    url = input('请输入视频链接：')
    try:
        resp = requests.get(url, headers=headers)
        html = re.findall(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>', resp.text, re.S)[0]
    except:
        print(resp.status_code)
        print(re.findall(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>', resp.text, re.S))
        resp.close()
        return 0
    data = json.loads(unquote(html))
    # pprint.pprint(data)
    try:
        video_text = data['app']['videoDetail']['desc'].replace('\n', '')
        path = f'C:/爬虫战果/视频/{video_text}.mp4'
        video_url = data['app']['videoDetail']['video']['bitRateList'][0]['playAddr'][0]['src']
        # video_url = 'http:' + data['app']['videoDetail']['video']['bitRateList'][0]['playAddr'][0]['src']
        video = requests.get(video_url, headers=headers).content
        # print(video_url)
        # print(video_text)
        if not os.path.isfile(path):
            with open(path, 'wb') as f:  # with open(f"{path}{video_text}.mp4",'wb') as f:
                for chunk in track(video,
                                   description=video_text):  # with tqdm.tqdm(total=len(video),unit='B', unit_scale=True, desc=video_text) as pbar:
                    f.write(bytes([chunk]))  # f.write(video);pbar.update(len(video))
                print('视频下载完成！')
    except IndexError:
        new_path = path.strip('.mp4')
        path = f'C:/爬虫战果/视频/{video_text}/{video_text}.mp4'
        img_list = data['app']['videoDetail']['images']
        # audio_url = 'http:' + data['app']['videoDetail']['video']['playAddr'][0]['src']
        audio_url = data['app']['videoDetail']['video']['playAddr'][0]['src']
        if not os.path.exists(new_path):
            os.makedirs(new_path)
            if not os.path.isfile(path):
                audio = requests.get(audio_url, headers=headers)
                with open(path.replace('.mp4', '.mp3'), 'wb') as f:
                    for chunk in track(audio.content, description=video_text + '.mp3'):
                        f.write(bytes([chunk]))
                    print(f'音频下载完成！')
                audio.close()
        count = 1
        for i in img_list:
            if i['video'] is None:
                print('这是个图片')
                img_url = i['urlList'][0]
                if not os.path.isfile(path):
                    img = requests.get(img_url, headers=headers)
                    with open(path.replace('.mp4', f'[{count}].webp'), 'wb') as f:
                        for chunk in track(img.content, description=video_text + f'[{count}]'):
                            f.write(bytes([chunk]))
                        print(f'图片[{count}]下载完成！')
                    img.close()
                count += 1
            elif i['video'] is not None:
                print('这是个视频')
                video_url = i['video']['bitRateList'][0]['playAddr'][0]['src']
                if not os.path.isfile(path):
                    video_temp = requests.get(video_url, headers=headers)
                    with open(path.replace('.mp4', f'[{count}].mp4'), 'wb') as f:
                        for chunk in track(video_temp.content, description=video_text + f'[{count}]'):
                            f.write(bytes([chunk]))
                        print(f'视频[{count}]下载完成！')
                    video_temp.close()
                count += 1
    resp.close()


get_video()


# 合并分段视频不行，音频对不上视频进度，还是交给专业剪辑的好了
def hebing():
    path = 'C:/爬虫战果/视频/'
    video_text = ''
    count = 11
    # videos = sorted([f'{path}/{video_text}{[i]}.mp4' for i in range(1, count)])
    videos = natsorted(os.listdir(f'{path}/{video_text}'))
    audio = videos.pop(0)
    video_clips = [VideoFileClip(os.path.join(path, video_text, video)) for video in videos]
    final_video = concatenate_videoclips(video_clips)
    audio_clip = AudioFileClip(os.path.join(path, video_text, audio))
    final_video = final_video.set_audio(audio_clip)
    final_video_output = f"{path}/{video_text}.mp4"
    final_video.write_videofile(final_video_output, codec='libx264', audio_codec='aac')
    for clip in video_clips:
        clip.close()
    audio_clip.close()
    final_video.close()
    print("视频合并完成！")


def get_video_by_share():  # 通过视频分享链接下载视频，不过太难了，目前无法实现
    link_str = ''
    url = re.findall(r'https://v.douyin.com/.*?/', link_str, re.S)[0]
    resp = requests.get(url, headers=headers)
    resp2 = requests.get(resp.url.split('?')[0], headers=headers)
    file_path = 'C:/爬虫战果/' + resp2.url.split('/')[-1]
    html = re.findall(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>', resp2.text, re.S)[0]
    data = json.loads(unquote(html))
    pprint.pprint(data)
    # print(data['app']['videoDetail'])
    # video_url = 'http:'+data['app']['videoDetail']['video']['bitRateList'][0]['playAddr'][0]['src']
    # video_text = data['app']['videoDetail']['desc']
    # video = requests.get(video_url,headers=headers).content
    # print(video_url)
    # print(video_text)
    resp.close()
    resp2.close()
