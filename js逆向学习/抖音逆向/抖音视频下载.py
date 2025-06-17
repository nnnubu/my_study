import requests, re, json, pprint, os, aiohttp, aiofiles, time
from urllib.parse import unquote
from rich.progress import track
from natsort import natsorted

headers = {
    'cookie': 'douyin.com; xg_device_score=7.762651797213144; device_web_cpu_core=12; device_web_memory_size=8; architecture=amd64; ttwid=1%7CeI6tSsjKfqVfL3kFuvOxqtvGwFpA2SoNvE2A_gyKAZ0%7C1722269732%7C3b17c168fe5307bda86ae56b779fbae12a58843e1c570543942f447e27102854; UIFID_TEMP=a6000b6bd0597977c28c1dbb751d8a8c80ef4c078dbea6da280536e6f6924b82b408f3349afd409be881f729f5864f93b4e9ce39b92bc8f1debb0e075478459df5f0cfd995a02e043644f3ac9f0a433f; fpk1=U2FsdGVkX1+WJNS7M0t/Cw45EF7OALQs9peZL7oMC4gfG6st4SFXUAH/XwwIrlCh5PRSRpCtbYm1gGXju4U0aQ==; fpk2=c28c178f7fc01e92a5161b6c80153add; UIFID=a6000b6bd0597977c28c1dbb751d8a8c80ef4c078dbea6da280536e6f6924b8275ddf33a0514170a8231c04ea18b4a0fe346fd0644e684fd07a649ffeb430f0a3d5b4cba396b289aa6b83be600adcdaa1d5424aff18edf2f4723ea509c8d21022241e67ce2c38c86fec50a281e786e2c689a5a998406a598126b8de2ec6381002fd26648463f6b6ecd0e3f578f8e1acc44877666c7ae58aeee1a5a098e742f0e; xgplayer_device_id=95963354057; xgplayer_user_id=274207810110; hevc_supported=true; dy_swidth=1920; dy_sheight=1080; passport_csrf_token=7a1ce316de953d8b471cd4e5bcb60865; passport_csrf_token_default=7a1ce316de953d8b471cd4e5bcb60865; bd_ticket_guard_client_web_domain=2; download_guide=%223%2F20241016%2F0%22; pwa2=%220%7C0%7C3%7C0%22; SEARCH_RESULT_LIST_TYPE=%22single%22; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; vdg_s=1; s_v_web_id=verify_m2cadiux_3dce987f_bee4_1a5b_b93f_f07789d9812e; d_ticket=620a7d407417dd763606a4e23e05c2f994e0d; n_mh=sEslLyjLZFa535SsJGPweZvUb0qowLPIx_yyCUsmB04; sso_auth_status=1929a0480907377d359884874863298d; sso_auth_status_ss=1929a0480907377d359884874863298d; is_staff_user=false; SelfTabRedDotControl=%5B%7B%22id%22%3A%227393267461628135460%22%2C%22u%22%3A14%2C%22c%22%3A0%7D%5D; _bd_ticket_crypt_doamin=2; __security_server_data_status=1; store-region=cn-gd; store-region-src=uid; publish_badge_show_info=%220%2C0%2C0%2C1729108227023%22; passport_assist_user=Cj1L_Xs9usZP-vYhxbDglT3a5AZKQAtlTeEUyBr91jle22LH4OM6Qd3As2dyjdNtMxqsNtcqvFzlEO1fZRl2GkoKPHRAkkf57ZAjZi9RJ1gZOKnA5NdRvt5nyjBCTJ69ehnSpeeH7Dtxe-J8T769Nl0GbT2hl24BnEUPC3K_-hDH9t4NGImv1lQgASIBA-wVe8k%3D; sso_uid_tt=e7b80c1945f9ea4a1ed4bb50199f241f; sso_uid_tt_ss=e7b80c1945f9ea4a1ed4bb50199f241f; toutiao_sso_user=0b9f7cb47be11a7bfe514512d4e3cfff; toutiao_sso_user_ss=0b9f7cb47be11a7bfe514512d4e3cfff; sid_ucp_sso_v1=1.0.0-KDI4NDQyOWVkMDMzNjA5OWIyZWU3NjE5YTQ2MDUxMTc4ZTQ1Y2Q5ZTEKHwiG9MGm-AIQ4rrAuAYY7zEgDDDgjdjZBTgGQPQHSAYaAmxxIiAwYjlmN2NiNDdiZTExYTdiZmU1MTQ1MTJkNGUzY2ZmZg; ssid_ucp_sso_v1=1.0.0-KDI4NDQyOWVkMDMzNjA5OWIyZWU3NjE5YTQ2MDUxMTc4ZTQ1Y2Q5ZTEKHwiG9MGm-AIQ4rrAuAYY7zEgDDDgjdjZBTgGQPQHSAYaAmxxIiAwYjlmN2NiNDdiZTExYTdiZmU1MTQ1MTJkNGUzY2ZmZg; passport_auth_status=e1fc28d2bc5d0173f382a02a1f7089ce%2C21e9ac07c6c6f42b0c0226092abbf19d; passport_auth_status_ss=e1fc28d2bc5d0173f382a02a1f7089ce%2C21e9ac07c6c6f42b0c0226092abbf19d; uid_tt=73c50fa10ee7d925f21d9ab2ce0449a3; uid_tt_ss=73c50fa10ee7d925f21d9ab2ce0449a3; sid_tt=99585d55167d01265f5607715598e1ee; sessionid=99585d55167d01265f5607715598e1ee; sessionid_ss=99585d55167d01265f5607715598e1ee; _bd_ticket_crypt_cookie=37a327805eaa1f9bcf2fddb45f8ec00a; sid_guard=99585d55167d01265f5607715598e1ee%7C1729109353%7C5183996%7CSun%2C+15-Dec-2024+20%3A09%3A09+GMT; sid_ucp_v1=1.0.0-KDAwZjZlZTdiOTRjOTA4YTdlMTY4OTA1NmMzNWYyYWY2YTU3ZWYyMzYKGQiG9MGm-AIQ6brAuAYY7zEgDDgGQPQHSAQaAmxmIiA5OTU4NWQ1NTE2N2QwMTI2NWY1NjA3NzE1NTk4ZTFlZQ; ssid_ucp_v1=1.0.0-KDAwZjZlZTdiOTRjOTA4YTdlMTY4OTA1NmMzNWYyYWY2YTU3ZWYyMzYKGQiG9MGm-AIQ6brAuAYY7zEgDDgGQPQHSAQaAmxmIiA5OTU4NWQ1NTE2N2QwMTI2NWY1NjA3NzE1NTk4ZTFlZQ; my_rd=2; __ac_nonce=06711448a00947e826e9d; __ac_signature=_02B4Z6wo00f01KUEtgwAAIDBel9FQdYHpcilJLKAAE5Va7; strategyABtestKey=%221729184906.892%22; WallpaperGuide=%7B%22showTime%22%3A1729100240908%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A65%2C%22cursor2%22%3A20%7D; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAApwXz2YNKsdtedbexpyKkR4uVlKzCuTFClwiJGdX3og0%2F1729267200000%2F0%2F0%2F1729185622464%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAApwXz2YNKsdtedbexpyKkR4uVlKzCuTFClwiJGdX3og0%2F1729267200000%2F0%2F1729185022465%2F0%22; odin_tt=aacbaf91e7cf94761906cbce6548c59a4ea602513f180dfca56be168c18d760655afbc237604a922f476ecdccb0f295a; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A1.55%2C%5C%22effective_type%5C%22%3A%5C%223g%5C%22%2C%5C%22round_trip_time%5C%22%3A350%7D%22; csrf_session_id=7cc154a991d456512137ebd5554b9ce9; home_can_add_dy_2_desktop=%221%22; volume_info=%7B%22isUserMute%22%3Atrue%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCR3dBMmFvekc1NXliTG9XUW9LQjZqYlozMkh5N1puMysrZkVBcTQwbWtKVnVVOFJJL29FZyt2M2tsWXJrenFzVVloalZYMEFNRGE1YjlqNDVrb09CZ1U9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; IsDouyinActive=false; passport_fe_beating_status=false',
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
