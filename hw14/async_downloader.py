import asyncio
import os
import aiohttp
import aiofiles
from tqdm import tqdm
from aiohttp import ClientSession, client_exceptions


async def asio_request(url: str, path: str, session: ClientSession, **kwargs):
    print("[URL] {}".format(url))
    try:
        async with session.get(url, **kwargs) as response:
            fname = response.content_disposition.filename if response.content_disposition and response.content_disposition.filename else response.url.name
            length = response.content_length
            print("[INFO] Start to download {}".format(fname))
            with tqdm(total=length) as pbar:
                async with aiofiles.open(os.path.join(path, fname), 'wb') as fp:
                    while True:
                        chunk = await response.content.read(16384)
                        pbar.update(len(chunk))
                        await fp.write(chunk)
                        if not chunk:
                            break
            print("[INFO] Finish downloading {}".format(fname))
    except:
        print("[FATAL] Failed to connect")


async def bulk_download(urls: list, path: str, **kwargs):
    async with ClientSession() as sess:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(asio_request(
                url=url, path=path, session=sess, **kwargs))
            tasks.append(task)
        await asyncio.gather(*tasks)
        print("[INFO] All downloads finished")

if __name__ == "__main__":
    import sys
    assert sys.version_info >= (3, 7), "Async requires Python 3.7 or later"

    texs = 'https://raw.githubusercontent.com/LearningOS/os-lectures/master/lecture21/slide-21-{:02d}.tex'
    mp4s = 'https://cloud.tsinghua.edu.cn/d/339de5f93d8c420ebbb7/files/?p=%2Flecture21%2Fslide-21-{:02d}.mp4&dl=1'
    urls = []
    urls = [texs.format(i) for i in range(1, 6)]
    urls.extend([mp4s.format(i) for i in range(1, 6)])
    save_path = './download'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    os.makedirs(save_path, exist_ok=True)
    print("Start downloading files: ")
    asyncio.run(bulk_download(urls, save_path, headers=headers))
