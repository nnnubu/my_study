import requests, subprocess, json, time, re, pprint, hashlib
from functools import partial
from urllib.parse import unquote, quote

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
import execjs

session = requests.Session()
timestamp = int(time.time())


def get_w_webid(mid, session, retry_count=3, delay=2):
    headers = {
        'referer': f'https://space.bilibili.com/{mid}',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
    }
    url = f'https://space.bilibili.com/{mid}/upload/video'
    try:
        resp = session.get(url, headers=headers)
        data = resp.text
        resp.close()
        w_webid = re.findall('<script id="__RENDER_DATA__" type="application/json">(.*?)</script>', data, re.S)[0]
        w_webid = json.loads(unquote(w_webid))['access_id']
        return w_webid
    except IndexError as e:
        print(f"发生了一个错误 : {e}")
        if retry_count > 0:
            print(f"正在重新获取... ({retry_count} 剩余请求次数)")
            time.sleep(delay)
            return get_w_webid(mid, session, retry_count=retry_count - 1)
        else:
            print("已超过最大请求次数！")
            return None


def get_dom_info():
    with open('dom_info.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
        js = execjs.compile(js_code)
        result = js.call('dom_info', )
        return result


#   get_dom_info这个函数可能失效，但是目前还能用    2025/5/22


def get_w_rid(dm_cover_img_str, dm_img_inter, dm_img_list, dm_img_str, mid, pn, w_webid, timestamp):
    f = [
        f"dm_cover_img_str={dm_cover_img_str}",
        f'dm_img_inter={quote(dm_img_inter)}',
        f"dm_img_list={quote(dm_img_list)}",
        f"dm_img_str={dm_img_str}",
        "index=0",
        "keyword=",
        f"mid={mid}",
        "order=pubdate",
        "order_avoided=true",
        "platform=web",
        f"pn={pn}",
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


def main():
    pn = input('请输入页码:')
    mid = input('请输入用户的mid:')
    dom_info = get_dom_info()
    dm_img_list = dom_info[0]
    dm_img_str = dom_info[1]
    dm_cover_img_str = dom_info[2]
    dm_img_inter = dom_info[3]
    w_webid = get_w_webid(mid, session)
    w_rid = get_w_rid(dm_cover_img_str, dm_img_inter, dm_img_list, dm_img_str, mid, pn, w_webid, timestamp)

    headers = {
        'referer': f'https://space.bilibili.com/{mid}/upload/video',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
    }

    params = [
        f'pn={pn}',
        'ps=40',
        'tid=0',
        'special_type=',
        'order=pubdate',
        f'mid={mid}',
        'index=0',
        'keyword=',
        'order_avoided=true',
        'platform=web',
        'web_location=333.1387',
        f'dm_img_list={dm_img_list}',
        f'dm_img_str={dm_img_str}',
        f'dm_cover_img_str={dm_cover_img_str}',
        f'dm_img_inter={dm_img_inter}',
        f'w_webid={w_webid}',
        f'w_rid={w_rid}',
        f'wts={timestamp}'
    ]

    url = 'https://api.bilibili.com/x/space/wbi/arc/search?' + '&'.join(params)
    resp = session.get(url, headers=headers)
    pprint.pprint(resp.json())
    resp.close()


if __name__ == '__main__':
    main()
