import requests,subprocess,json,time,random,tqdm,re
from functools import partial
subprocess.Popen = partial(subprocess.Popen,encoding='utf-8')
import execjs,pprint

class manga():
    def __init__(self,name,path_word,cover):
        self.name = name
        self.path_word = path_word
        self.cover = cover

def Get_Manga(path_word,content_list=[]):
    url = f'https://www.mangacopy.com/comicdetail/{path_word}/chapters'

    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
    }

    resp = requests.get(url,headers=headers)
    results = json.loads(resp.text)['results']
    resp.close()
    info = Decrypt_data(results)
    content_list = info['groups']['default']['chapters']
    return content_list

def Decrypt_data(results):
    with open('响应体解密.js','r',encoding='utf-8') as f:
        js_code = f.read()
        js = execjs.compile(js_code)
        result = js.call('decrypt',results)
        return result

def Search_Manga(name,manga_list=[],limit=12,i=0,k=1,count=1,page=100,pbar=None):
    # print(f'----------------第{k}页----------------')
    url = f'https://www.mangacopy.com/api/kb/web/searchbd/comics?offset={i}&platform=2&limit={limit}&q={name}&q_type='
    headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
    }
    resp = requests.get(url,headers=headers)
    resp.close()
    data = resp.json()['results']['list']
    try:
        if(k==1):
            page = resp.json()['results']['total']//limit
            # print(f'总共有{page+1}页')
            if(page==0):
                return manga_list
            if pbar is None:
                pbar = tqdm.tqdm(total=page, desc="获取漫画中...")
        elif(k-1==page):
            if pbar:
                pbar.close()
            return  manga_list
    finally:
        for j in data:
            manga_list.append(manga(j['name'],j['path_word'],j['cover']))
            # print(count,j['name'],j['path_word'],j['cover'])
            count+=1
        if pbar:
            pbar.update(1)
    time.sleep(random.randint(2,4))
    i+=12
    k+=1
    return Search_Manga(name,manga_list,limit,i,k,count,page,pbar)

def Download_manga(id):
    time.sleep(random.randint(2,4))
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'}
    url = f'https://www.mangacopy.com/comic/xinzhichengxu/chapter/{id}'
    resp = requests.get(url,headers=headers)
    resp.close()
    results = json.loads(re.findall('<div class="imageData" contentKey=(.*?)></div>',resp.text,re.S)[0])
    info = Decrypt_data(results)
    return info