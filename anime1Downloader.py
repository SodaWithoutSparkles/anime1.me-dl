#!/usr/bin/python3

import argparse
import requests
import json
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser("anime1Downloader.py", formatter_class=argparse.RawTextHelpFormatter, description='Download anime1.me videos using requsets and beautifulsoup static parser')
parser.add_argument(
    "url", help="a anime1.me direct url, e.g. https://anime1.me/18305\nLinks starting with https://anime1.me/category may not work\nYou may need to quote the url")
parser.add_argument('-v', '--verbose', action='store_true', help="print debug info")
parser.add_argument('-x', '--extract', action='store_true', help="extract URL only, no download")
args = parser.parse_args()
url = args.url
if args.verbose:
    print("[debug]", args.verbose)
print(" [info] downloading from", url)

def extractAPIpath(url):
    videoClass = 'video-js'
    titleClass = 'entry-title'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    title = soup.find(attrs={"class": titleClass}).get_text()
    video = soup.find(attrs={"class": videoClass})['data-apireq']
    if (video == None):
        print("[ERROR] fatal: unable to find data-apireq, abort")
        exit(1)
    print(" [info] title: ", title)
    if args.verbose:
        print("[debug] data-apireq: ", video)
    return video, title


def getSource(video):
    dataRaw = 'd=' + video
    session = requests.Session()
    response = session.post(
        'https://v.anime1.me/api',
        data=dataRaw,
        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    result = json.loads(response.content.decode("utf-8"))
    if args.verbose:
        print("[debug] raw api response: ", response.content.decode("utf-8"))
        print("[debug] cookie: ", session.cookies.get_dict())
        print("[debug] source: https:" + str(result['s'][0]['src']))
    src = result['s'][0]['src']
    return src, session.cookies.get_dict()


def downloadVideo(src, cookie, title):
    import yt_dlp
    src = 'https:' + src
    dict_cookie = cookie
    e = dict_cookie['e']
    h = dict_cookie['h']
    p = dict_cookie['p']
    all = 'e=' + e + ';' + 'h=' + h + ';' + 'p=' + p
    dict_cookie = {'cookie': all}
    ydl_opts = {
        'concurrent_fragment_downloads': 32,
        'http_headers': dict_cookie,
        'verbose': args.verbose,
        'outtmpl': title + ".%(ext)s"
    }
    if args.verbose:
        print("[debug] yt-dlp opts: ", ydl_opts)
    print(" [info] passing info to yt-dlp for downloading... \n")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([src])


def main(url):
    video, title = extractAPIpath(url)
    src, cookie = getSource(video)
    if not(args.extract):
        downloadVideo(src, cookie, title)
    else:
        print(f'[INFO] URL: {src}\n[INFO] cookie: {cookie}')

try:
    main(url)

except Exception as e:
    print("----    Error    ----")
    print(e)
finally:
    print(" [info] cleaning up...")
