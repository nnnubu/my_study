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


url = 'https://www.bilibili.com/video/BV1QVSJYzEYf/?spm_id_from=333.788.videopod.sections&vd_source=9cb26b93127feca8518ea39506132c11&p=7'
# url = 'https://www.bilibili.com/video/BV1QVSJYzEYf/?spm_id_from=333.788.videopod.sections&vd_source=9cb26b93127feca8518ea39506132c11'
header = {
    "cookie": "buvid3=A07A2F16-A326-C9EA-D3C7-9819F05A3CA425846infoc; b_nut=1748624025; _uuid=A8108F6EB-B8EB-E84A-9EA6-DA2FB431088FC25387infoc; buvid_fp=858a4450213f5c2b086f64826eb0abc4; header_theme_version=CLOSE; enable_web_push=DISABLE; enable_feed_channel=ENABLE; home_feed_column=5; browser_resolution=2133-1083; buvid4=13B7A145-B277-5666-9361-2FAB63C42AD789708-024042510-A29gAFm6qKCDuygPoa4PQA%3D%3D; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDg4ODMyMjcsImlhdCI6MTc0ODYyMzk2NywicGx0IjotMX0.HiSo4-AhW3Gm1ops2CXBLCV7X1355GhN-gcv5HPLdoY; bili_ticket_expires=1748883167; SESSDATA=1c165b9d%2C1764177084%2C0f187%2A52CjCBwt4i4kYSYGYDBoN5ZNzAnqdJ1ceVn458ItYwWYT7YaReZCT3E_56DCRD6cZuIx4SVk83WlJkVjc0dnFDajRQMnBFMjZ3eE9HUWVybWNZR21abHhYQUg2dVc0N3R0SVRFRmRmRjZ5V0xwaTh1RWxCV3ZGSXluTGpZdnRqQlFDbVZ5YjA1WkxnIIEC; bili_jct=d1bb4aed04aa0753130eb083f80eac31; DedeUserID=430970446; DedeUserID__ckMd5=6b1ce26d8638a884; b_lsid=CEBC1BCD_197226A1D3D; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; sid=6ojsagri; CURRENT_FNVAL=4048; rpdid=|(J|)lYJ|)|)0J'u~R)Ykm|mm; CURRENT_QUALITY=80",
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
