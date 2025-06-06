import pprint
from math import floor
from random import randint
from urllib.parse import unquote, quote, urlencode
import requests, time, hashlib, json, re
from numpy.random.mtrand import random


def get_w_webid(mid, session):
    headers1 = {
        'referer': f'https://space.bilibili.com/{mid}',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
    }
    # 给拿w_webid用的，现在也用不上了
    url = f'https://space.bilibili.com/{mid}/upload/video'
    resp = session.get(url, headers=headers1)
    data = resp.text
    resp.close()
    try:
        w_webid = re.findall('<script id="__RENDER_DATA__" type="application/json">(.*?)</script>', data, re.S)[0]
        w_webid = json.loads(unquote(w_webid))['access_id']
    except IndexError:
        print(resp.url)
    return w_webid


# b站改了，w_webid现在用不上了

def get_dm_img_inter():
    width = 1920  # 默认宽度
    height = 971  # 默认高度
    r1 = floor(random() * 114)
    r2 = floor(random() * 514)
    dic = {"ds": [], "wh": [2 * (width + height) + 3 * r1, 4 * width - height + r1, r1],
           "of": [r2, 2 * r2, r2]}  # 鼠标不动ds就是空，of和页面滚动条有关，不滚动就是0，所以就不写进去了
    return dic


def get_w_rid(dm_img_inter, mid, timestamp, w_webid):
    f = [
        "dm_cover_img_str=QU5HTEUgKEludGVsLCBJbnRlbChSKSBVSEQgR3JhcGhpY3MgKDB4MDAwMDQ2QTMpIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEpR29vZ2xlIEluYy4gKEludGVsKQ",
        f'dm_img_inter={quote(dm_img_inter)}',  # 变化
        "dm_img_list=%5B%5D",  # 页面鼠标没有移动可以为[]，此处是url编码的结果
        "dm_img_str=V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ",
        "index=0",
        "keyword=",
        f"mid={mid}",  # 用户id
        "order=pubdate",
        "order_avoided=true",
        "platform=web",
        "pn=1",
        "ps=40",
        "special_type=",
        "tid=0",
        f"w_webid={w_webid}",
        "web_location=333.1387",
        f"wts={timestamp}"
    ]
    args = '&'.join(f)
    key = 'ea1db124af3c7062474693fa704f4ff8'
    strings = args + key
    md5 = hashlib.md5()
    md5.update(strings.encode(('utf-8')))
    w_rid = md5.hexdigest()
    return w_rid


def get_content():
    session = requests.Session()
    session.get('https://www.bilibili.com/', headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0'})
    mid = 2672616
    a = get_dm_img_inter()
    dm_img_inter = ('{"ds"' + ':' + json.dumps(a['ds']) + ',' + '"wh"' + ':' + json.dumps(
        a['wh']) + ',' + '"of"' + ':' + json.dumps(a['of']) + '}').replace(" ", "")
    w_webid = get_w_webid(mid, session)
    timestamp = int(time.time())
    w_rid = get_w_rid(dm_img_inter, mid, timestamp, w_webid)
    dm_img_inter = (quote('{"ds"') + ':' + json.dumps(a['ds']) + ',' + quote('"wh"') + ':' + json.dumps(
        a['wh']) + ',' + quote('"of"') + ':' + json.dumps(a['of']) + quote('}')).replace(" ", "")

    headers2 = {
        'referer': f'https://space.bilibili.com/{mid}/upload/video',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
    }

    params = [
        'pn=1',  # 页码
        'ps=40',  # 每一页的视频数量
        'tid=0',
        'special_type=',
        'order=pubdate',
        'mid=305956876',  # 用户id
        'index=0',
        'keyword=',
        'order_avoided=true',
        'platform=web',
        'web_location=333.1387',
        # ——————————————以上均为固定值———————————————————
        'dm_img_list=[]',  # 可以为空
        'dm_img_str=V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ',  # 固定值
        'dm_cover_img_str=QU5HTEUgKEludGVsLCBJbnRlbChSKSBVSEQgR3JhcGhpY3MgKDB4MDAwMDQ2QTMpIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEpR29vZ2xlIEluYy4gKEludGVsKQ',
        # 固定值
        f'dm_img_inter={dm_img_inter}',
        f'w_webid={w_webid}',
        # url='https://space.bilibili.com/用户id/upload/video',访问用户主页，直接在源代码的render_data中进行获取         现在改了不需要了
        f'w_rid={w_rid}',  # md5加密32位小，密钥：ea1db124af3c7062474693fa704f4ff8，加密体为除了该参数以外的所有参数,参数之间要用&连接起来
        f'wts={timestamp}'  # f'{int(time.time())}',    #时间戳
    ]

    # 274763540
    url = 'https://api.bilibili.com/x/space/wbi/arc/search?' + '&'.join(params)
    resp = session.get(url, headers=headers2)
    print(resp.text)
    resp.close()


get_content()

# 总结：在我成功之后，再次对这次的案例进行反思，发现之前的思考方式完全是采用取巧的方式进行的，页面变化的情况有点击页码，点击上下页，和刷新三种情况，而我为了图方便，选择了最简单的刷新的情况，这种情况下的参数都可以默认为[]，其实说不定也是哪里错了，因为参数之间有互相引用，这也使得最后校验不对而无法获取内容。总之，暂时先这么想，解决问题时一定要考虑到诸多方面，毕竟写这个总结的时候也离上次成功拿到数据之后有段时间了，具体的收获有点忘记了，下次一定要及时总结。
