import asyncio,uuid,re,time,pprint
from rich.progress import Progress
from 博主主页信息获取 import spider_1,spider_2
from 抖音视频下载 import get_video

async def main():   #这个在下载图文视频的时候会出现进度到不了100%的情况，但实际上应该是下载完成了

    progress = Progress()

    sem = asyncio.Semaphore(5)

    # temp_list = spider_1()

    temp_list = await spider_2()

    author = temp_list[0].author

    tasks=[]

    for i in temp_list:
        if len(i.data_size) > 0:
            total = sum(i.data_size)
        else:
            total = int(1.5 * 1024 * 1024)
            # total = 50
        desc = re.sub(r'[,<>:"/\\|?*\n]', '', i.desc)
        # task_id = str(uuid.uuid4())
        task_id = progress.add_task(desc, total=total)
        tasks.append(asyncio.create_task(get_video(sem,i.aweme_id, author,progress,task_id)))

    await asyncio.wait(tasks)  

if __name__ == "__main__":
    asyncio.run(main())