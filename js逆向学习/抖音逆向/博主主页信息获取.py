import time
from pprint import pprint
from urllib.parse import quote
import requests, subprocess
from functools import partial
from itertools import chain
subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
import execjs

def get_a_bogus(args, ua):
    with open(r'C:\Python学习\js逆向学习\抖音逆向\a_bogus.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
        js = execjs.compile(js_code)
        result = js.call('a_bogus', args, ua)
        return result

def get_response(params):     #   下一次的工作，加上异步协程，但是我发现我这里的aiohttp模块不知道为什么无法使用，目前无法实现了，请求数据多就会很慢

    url = 'https://www.douyin.com/aweme/v1/web/aweme/post/'

    headers = {
        'referer': f'https://www.douyin.com/user/{id}',
        # 'referer': f'https://www.douyin.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
        'cookie': 'UIFID_TEMP=c8c20d54553eadab8c678961c2b0df95555df87bbc6b890988ad105aec15abc07b6d3387bdd9bd2cc39d5d97cf3bde63792c211bbafd1cfb9efabb722fe1be8a5c292ce19a2a98b3d95135800ebcc908; s_v_web_id=verify_mbavw8vc_BawGFFeI_pAWQ_4xBm_BfLr_bF4H9kuFNj2T; hevc_supported=true; dy_swidth=1920; dy_sheight=1080; fpk1=U2FsdGVkX1/At+T2RLCydH3NkJm5R2+kTUw5zQe1GctfQ00HsQf3VbBrpvNARFmZJ6/Cr1jDsJQyAVURvt7BpA==; fpk2=8369da3c75ccd12bc017791df73a85c8; __security_mc_1_s_sdk_crypt_sdk=14b7db81-4da0-947a; __security_mc_1_s_sdk_cert_key=bc796dd6-4838-9751; bd_ticket_guard_client_web_domain=2; passport_csrf_token=5f3277508fe6bed5cf377e749e8a053f; passport_csrf_token_default=5f3277508fe6bed5cf377e749e8a053f; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; passport_mfa_token=CjXXW4baD9l94HJ0dMvOEUbR8l1o2LMuRkVAZHaZvFHmnaSk%2FgTWQR69TmhpGWdLMRDua3K%2BgBpKCjyFKKC0rmXzUlhhmcoJIGPaUqYs7t%2B%2B3miVfcVeuFfbClxA2F0kO57A8%2Bq0ggcNq2UZeZeTDpwCGfG5P5YQmOLyDRj2sdFsIAIiAQOG%2FfMd; d_ticket=4ec948de86d9fcef3e8d9e94eb530a53a0d3c; passport_assist_user=Cj0kJKUOte63wHZ6G5jwNwNb9jGbWGClFUYFKKip-36DHktuSeyANi1FBC9DzeP88fMWQ3qMQFEVduLtjTafGkoKPAkUMsQ5oCkm6S8pT2w9xYokaBRUAgCzPSR4wVs4BS-MclTu2Mkzkp7wnSQWwgIcCr88MeLiY6WKzr_LEBCY4vINGImv1lQgASIBA9Ugg-M%3D; n_mh=sEslLyjLZFa535SsJGPweZvUb0qowLPIx_yyCUsmB04; passport_auth_status=eb7d6298534a5087d15cad1dd47c00d0%2C; passport_auth_status_ss=eb7d6298534a5087d15cad1dd47c00d0%2C; sid_guard=d7fc65e4178ee03cc6b4fab9f114a7a8%7C1748614475%7C5184000%7CTue%2C+29-Jul-2025+14%3A14%3A35+GMT; uid_tt=70ddf9ebe40127a9338b4ed7d73573a7; uid_tt_ss=70ddf9ebe40127a9338b4ed7d73573a7; sid_tt=d7fc65e4178ee03cc6b4fab9f114a7a8; sessionid=d7fc65e4178ee03cc6b4fab9f114a7a8; sessionid_ss=d7fc65e4178ee03cc6b4fab9f114a7a8; is_staff_user=false; sid_ucp_v1=1.0.0-KDI3MGJjNWQ4ZDhkZDQ0OWIwZjdkMTg5NWRlNWViNjI3MDYyZDM3YjEKHwiG9MGm-AIQy_rmwQYY7zEgDDDgjdjZBTgCQPEHSAQaAmhsIiBkN2ZjNjVlNDE3OGVlMDNjYzZiNGZhYjlmMTE0YTdhOA; ssid_ucp_v1=1.0.0-KDI3MGJjNWQ4ZDhkZDQ0OWIwZjdkMTg5NWRlNWViNjI3MDYyZDM3YjEKHwiG9MGm-AIQy_rmwQYY7zEgDDDgjdjZBTgCQPEHSAQaAmhsIiBkN2ZjNjVlNDE3OGVlMDNjYzZiNGZhYjlmMTE0YTdhOA; login_time=1748614474324; UIFID=c8c20d54553eadab8c678961c2b0df95555df87bbc6b890988ad105aec15abc07b6d3387bdd9bd2cc39d5d97cf3bde63f96cf7ec236cb750b61222669582af7415957c05da998d74778fd35787f44742482185e860f14350614e6cb48378a98759ea00ac944b3bad3d6a0753b86fd6ebd5c685f36b93b3f6ee5705f1f2b7c51b3b7f590c52f0d47884e729277648905b5a47cdba1f1a5029d2e5c17bcaf11191; _bd_ticket_crypt_cookie=8c14a0f2d0d89524dc60dfb69d87133a; __security_mc_1_s_sdk_sign_data_key_web_protect=a111c665-4376-aa94; __security_server_data_status=1; is_dash_user=1; publish_badge_show_info=%220%2C0%2C0%2C1748614477496%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; ttwid=1%7CiYE5nukviNYKVGNQFnrrpsyd_rU6GdtIZUSbPTcSoas%7C1748785282%7C9dcf6507a073eaca4d2ee80ddd4b3501e0371def63b5d1e27c16e686edf63c82; FOLLOW_RED_POINT_INFO=%221%22; strategyABtestKey=%221749141416.488%22; download_guide=%221%2F20250606%2F0%22; douyin.com; device_web_cpu_core=12; device_web_memory_size=8; architecture=amd64; SelfTabRedDotControl=%5B%7B%22id%22%3A%227342761377129302066%22%2C%22u%22%3A492%2C%22c%22%3A0%7D%2C%7B%22id%22%3A%227426002893125191707%22%2C%22u%22%3A122%2C%22c%22%3A0%7D%2C%7B%22id%22%3A%227393267461628135460%22%2C%22u%22%3A15%2C%22c%22%3A0%7D%5D; WallpaperGuide=%7B%22showTime%22%3A0%2C%22closeTime%22%3A0%2C%22showCount%22%3A0%2C%22cursor1%22%3A40%2C%22cursor2%22%3A12%2C%22hoverTime%22%3A1748850462795%7D; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAApwXz2YNKsdtedbexpyKkR4uVlKzCuTFClwiJGdX3og0%2F1749225600000%2F0%2F0%2F1749205344447%22; __ac_nonce=06842bcd8007853ea42f; __ac_signature=_02B4Z6wo00f01VADLPgAAIDAj1jftYDP151QIyhAADxG6f; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAApwXz2YNKsdtedbexpyKkR4uVlKzCuTFClwiJGdX3og0%2F1749225600000%2F1749199741862%2F0%2F1749205716766%22; passport_fe_beating_status=true; xgplayer_device_id=78459635851; xgplayer_user_id=10675032642; xg_device_score=7.650552891894796; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCR3dBMmFvekc1NXliTG9XUW9LQjZqYlozMkh5N1puMysrZkVBcTQwbWtKVnVVOFJJL29FZyt2M2tsWXJrenFzVVloalZYMEFNRGE1YjlqNDVrb09CZ1U9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22; odin_tt=b0b33db8e3493563cb1c901b84937dea1dfa6020bc7c1194923e468ebe46414b8855d75bf0eb7d0815d18cecfbf65a41663c7ec70364ae3d09530842b46ff6d0'
    }

    args = [
        "device_platform=webapp",
        "aid=6383",
        "channel=channel_pc_web",
        # "cursor=0",
        # "count=20",
        "update_version_code=170400",
        "pc_client_type=1",
        "pc_libra_divert=Windows",
        "support_h265=1",
        "support_dash=1",
        "cpu_core_num=12",
        "version_code=170400",
        "version_name=17.4.0",
        "cookie_enabled=true",
        "screen_width=1920",
        "screen_height=1080",
        "browser_language=zh-CN",
        "browser_platform=Win32",
        "browser_name=Edge",
        "browser_version=137.0.0.0",
        "browser_online=true",
        "engine_name=Blink",
        "engine_version=137.0.0.0",
        "os_name=Windows",
        "os_version=10",
        "device_memory=8",
        "platform=PC",
        "downlink=10",
        "effective_type=4g",
        "round_trip_time=50",
        "webid=7510241786578077199","uifid=c8c20d54553eadab8c678961c2b0df95555df87bbc6b890988ad105aec15abc07b6d3387bdd9bd2cc39d5d97cf3bde63f96cf7ec236cb750b61222669582af7415957c05da998d74778fd35787f44742482185e860f14350614e6cb48378a98759ea00ac944b3bad3d6a0753b86fd6ebd5c685f36b93b3f6ee5705f1f2b7c51b3b7f590c52f0d47884e729277648905b5a47cdba1f1a5029d2e5c17bcaf11191",
        "verifyFp=verify_mbavw8vc_BawGFFeI_pAWQ_4xBm_BfLr_bF4H9kuFNj2T",
        "fp=verify_mbavw8vc_BawGFFeI_pAWQ_4xBm_BfLr_bF4H9kuFNj2T",
        f"msToken={quote(params['msToken'])}"
    ]

    params['a_bogus'] = get_a_bogus('&'.join(args), headers['user-agent'])

    response = requests.get(url, headers=headers, params=params)

    response.close()

    return response

def get_info(id,max_cursor = 0,min_cursor = 0,count = -1,time_list=[],aweme_list = []):

    try:
        if count == -1:

            # 第一次获取作品时间区间
            params = {
                'aid': '6383',
                'sec_user_id': id,
                'count': '1',
                'need_time_list': '1',
                'publish_video_strategy_type': '2',
                'msToken': 'F9I4VmB0isy5RzXW8r897DLJe30Qdy35zgChSxYEhs86JDSYZsuj63JzMBai71czv6SNaouP_bVNs5qnLjX0fLVqypbnfQtGcXz7lIJ5vo2p-c3vI6OAI1m8XdxIYb5HaJfnki8VYgPt2BVrmv8qOcOhRy3Pi97ER0v-4j4DzcpuN_39ta-JmA=='
                # 可以变化也可以不变
            }

            response = get_response(params)

            data = response.json()['time_list']

            time_list = [int(time.mktime(time.strptime(f"{i} 00:00:00", "%Y·%m %H:%M:%S"))) for i in data]

            time_list.insert(0,0)

            count += 1

            aweme_list = get_info(id,time_list[count],time_list[count+1],count,time_list,aweme_list)

        else:
            #   分析了一下有些参数是不需要的  ↓   可能是因为args里面固定的内容有了
            params = {
                'device_platform': 'webapp',
                'aid': '6383',
                'channel': 'channel_pc_web',
                'sec_user_id': id,  # 变化
                'max_cursor': f'{max_cursor}' + '000',  #时间戳 对应需要改变下面的need_time_list为0   经过我的进一步分析，这个need_time_list应该不关联,这个值对应的是用户发布作品的年份加日期，从这个时间以前的开始数count数量的作品  注意这个往后数指的是往前推的时间，不填的话应该是从最新的开始   例如2025-06-01往前的作品
                'min_cursor': f'{min_cursor}' + '000',   #这个则是和上面相反的，就是从这个时间往后开始取count数量的作品  例如2023-07-01往后的作品
                'locate_item_id': '7512022632229932346',    #视频id
                'locate_query': 'false',
                'show_live_replay_strategy': '1',
                'need_time_list': '1',
                'time_list_query': '0',
                'whale_cut_token': '',
                'cut_version': '1',
                'count': '60',  # 这个是每页最大数量，其实实际返回不止这些，会加上用户主页的置顶视频的数量,直接设置成200得了，但是一次最多好像只能拿40多个,下一次的工作是利用递归法按每个月来获取内容
                'publish_video_strategy_type': '2',
                'from_user_page': '1',
                'update_version_code': '170400',
                'pc_client_type': '1',
                'pc_libra_divert': 'Windows',
                'support_h265': '1',
                'support_dash': '1',
                'cpu_core_num': '12',
                'version_code': '290100',
                'version_name': '29.1.0',
                'cookie_enabled': 'true',
                'screen_width': '1920',
                'screen_height': '1080',
                'browser_language': 'zh-CN',
                'browser_platform': 'Win32',
                'browser_name': 'Edge',
                'browser_version': '137.0.0.0',
                'browser_online': 'true',
                'engine_name': 'Blink',
                'engine_version': '137.0.0.0',
                'os_name': 'Windows',
                'os_version': '10',
                'device_memory': '8',
                'platform': 'PC',
                'downlink': '10',
                'effective_type': '4g',
                'round_trip_time': '50',
                'webid': '7510241786578077199',
                'uifid': 'c8c20d54553eadab8c678961c2b0df95555df87bbc6b890988ad105aec15abc07b6d3387bdd9bd2cc39d5d97cf3bde63f96cf7ec236cb750b61222669582af7415957c05da998d74778fd35787f44742482185e860f14350614e6cb48378a98759ea00ac944b3bad3d6a0753b86fd6ebd5c685f36b93b3f6ee5705f1f2b7c51b3b7f590c52f0d47884e729277648905b5a47cdba1f1a5029d2e5c17bcaf11191',
                "verifyFp": "verify_mbavw8vc_BawGFFeI_pAWQ_4xBm_BfLr_bF4H9kuFNj2T",
                "fp": "verify_mbavw8vc_BawGFFeI_pAWQ_4xBm_BfLr_bF4H9kuFNj2T",
                'msToken': 'F9I4VmB0isy5RzXW8r897DLJe30Qdy35zgChSxYEhs86JDSYZsuj63JzMBai71czv6SNaouP_bVNs5qnLjX0fLVqypbnfQtGcXz7lIJ5vo2p-c3vI6OAI1m8XdxIYb5HaJfnki8VYgPt2BVrmv8qOcOhRy3Pi97ER0v-4j4DzcpuN_39ta-JmA=='
                # 可以变化也可以不变
            }

            response = get_response(params)

            data = response.json()['aweme_list']

            aweme_list.append(data)

            count += 1

            aweme_list = get_info(id, time_list[count], time_list[count + 1], count, time_list,aweme_list)

    except IndexError:

        aweme_list = list(chain(*aweme_list))

    finally:

        return aweme_list

if __name__ == '__main__':
    id = input('请粘贴用户search_id：')
    data = get_info(id)
    count = 1
    for i in data:
        temp = {
            "count":count,
            "aweme_id":i['aweme_id'],
            "desc":i['desc'],
            "images":[link['url_list'][0] for link in i['images']] if i['images'] != None else i['images'],
            "url_list":i['video']['play_addr']['url_list']
        }
        pprint(temp)
        count+=1
