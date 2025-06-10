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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
    }

    # cookie = ''

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
