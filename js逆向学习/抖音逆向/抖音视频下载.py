import requests, re, json, pprint, os, aiohttp, aiofiles, time
from urllib.parse import unquote
from rich.progress import track
from natsort import natsorted

headers = {
    'cookie': '',
    'referer': 'https://www.douyin.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'}

async def get_video(sem,modal_id, author=None,progress=None,task_id=None):
    async with sem: 
        url = f'https://www.douyin.com/jingxuan?modal_id={modal_id}'
        headers = {
            'Referer': 'https://www.douyin.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
        }
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                async with session.get(url,headers=headers) as resp:
                    try:
                        html = re.findall(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>',await resp.text(), re.S)[0]
                    except Exception as e:
                        print(f"Error: {e}")
                        print(resp.status)
                        print(re.findall(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>',await resp.text(), re.S))
                        return 0
                data = json.loads(unquote(html))
                try:
                    video_text = re.sub(r'[<>:"/\\|?*\n]', '', data['app']['videoDetail']['desc'])
                    if author:
                        author_dir = f'C:/爬虫战果/视频/{author}'
                        if not os.path.exists(author_dir):
                            os.makedirs(author_dir)
                        path = f'{author_dir}/{video_text}.mp4'
                    else:
                        path = f'C:/爬虫战果/视频/{video_text}.mp4'
                    video_url = data['app']['videoDetail']['video']['bitRateList'][0]['playAddr'][0]['src']
                    if not os.path.isfile(path):
                        async with session.get(video_url, headers=headers) as resp:
                            if resp.status == 200:
                                async with aiofiles.open(path, 'wb') as f:
                                    if progress:
                                        progress.start()
                                    async for chunk in resp.content.iter_chunked(1024):
                                        await f.write(chunk)
                                        if progress:
                                            progress.update(task_id,advance=len(chunk))
                        # print(f'{video_text}.mp4下载完成!')
                except IndexError:
                    new_path = path.strip('.mp4')
                    path = f'{new_path}/{video_text}.mp4'
                    img_list = data['app']['videoDetail']['images']
                    audio_url = data['app']['videoDetail']['video']['playAddr'][0]['src']
                    if not os.path.exists(new_path):
                        os.makedirs(new_path)
                        if not os.path.isfile(path):
                            async with session.get(audio_url, headers=headers) as resp:
                                if resp.status == 200:
                                    async with aiofiles.open(path.replace('.mp4', '.mp3'), 'wb') as f:
                                        if progress:
                                            progress.start()
                                        async for chunk in resp.content.iter_chunked(1024):
                                            await f.write(chunk)
                                            if progress:
                                                progress.update(task_id,advance=len(chunk))
                            # print(f'{video_text}.mp3下载完成!')
                    count = 1
                    for i in img_list:
                        if i['video'] is None:
                            # print('这是个图片')
                            img_url = i['urlList'][0]
                            if not os.path.isfile(path):
                                async with session.get(img_url) as resp:
                                    if resp.status == 200:
                                        async with aiofiles.open(path.replace('.mp4', f'[{count}].webp'), 'wb') as f:
                                            async for chunk in resp.content.iter_chunked(1024):
                                                await f.write(chunk)
                                                if progress:
                                                    progress.update(task_id,advance=len(chunk))
                                # print(f'{video_text}[{count}].webp下载完成!')
                            count += 1
                        elif i['video'] is not None:
                            # print('这是个视频')
                            video_url = i['video']['bitRateList'][0]['playAddr'][0]['src']
                            if not os.path.isfile(path):
                                async with session.get(video_url, headers=headers) as resp:
                                    if resp.status == 200:
                                        async with aiofiles.open(path.replace('.mp4', f'[{count}].mp4'), 'wb') as f:
                                            async for chunk in resp.content.iter_chunked(1024):
                                                await f.write(chunk)
                                                if progress:
                                                    progress.update(task_id,advance=len(chunk))
                                # print(f'{video_text}[{count}].mp4下载完成!')
                            count += 1
            except aiohttp.ClientPayloadError:
                print(f"Error: Not enough data to satisfy content length header. Retrying...")
                progress.stop(task_id)
                time.sleep(5)
                await get_video(modal_id, author, progress, task_id)  # 重试请求 

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
