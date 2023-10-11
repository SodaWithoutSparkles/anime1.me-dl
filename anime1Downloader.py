#!/usr/bin/python3

import argparse
import requests
import json
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser("anime1Downloader.py", formatter_class=argparse.RawTextHelpFormatter,
                                 description='Download anime1.me videos using requsets and beautifulsoup static parser')
parser.add_argument(
    "url", help="a anime1.me direct url, e.g. https://anime1.me/18305\nYou may need to quote the url")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="print debug info")
parser.add_argument('-x', '--extract', action='store_true',
                    help="extract URL only, no download")
parser.add_argument('-cf', '--cloudflare',
                    help="set cf_clearance cookie to bypass cloudflare detection\nThe cookie is valid for an hour\nYou may need to quote the cookie", metavar='COOKIE')
parser.add_argument('-ua', '--user-agent',
                    help="set user-agent to bypass detection")
args = parser.parse_args()
url = args.url
if args.verbose:
    print("[debug]", args.verbose)
print(" [info] extracting from", url)

headers = {'User-Agent': args.user_agent}
cookies = {'cf_clearance': args.cloudflare}


def mergeLists(list1, list2):
    return list(map(lambda x, y: (x, y), list1, list2))


def extractAPIpath(url):
    videoClass = 'video-js'
    titleClass = 'entry-title'
    session = requests.Session()
    if (args.user_agent != None and args.cloudflare != None):
        resp = session.get(url, headers=headers, cookies=cookies)
    elif (args.user_agent != None or args.cloudflare != None):
        print("[ERROR] cloudflare detects both user-agent and cf_clearance")
        print("[ERROR] using just a single one might not bypass the detection")
        exit(1)
    else:
        print(
            " [WARN] user-agent and cf_clearance missing, cloudflare might block the request")
        resp = session.get(url)

    if (resp.status_code) == 403:
        print("[ERROR] fatal: blocked by cloudflare")
        exit(1)
    soup = BeautifulSoup(resp.text, 'lxml')
    listOfTitles = soup.find_all(attrs={"class": titleClass})
    listOfVideos = soup.find_all(attrs={"class": videoClass})
    titles = []
    videos = []
    for title in listOfTitles:
        titles.append(title.get_text())
    for video in listOfVideos:
        videos.append(video['data-apireq'])

    if (len(videos) == 0 or videos[0] == None):
        print("[ERROR] fatal: unable to find data-apireq, abort")
        exit(1)
    if (len(titles) == 0 or titles[0] == None):
        print("[ERROR] fatal: unable to find title, abort")
        exit(1)
    if (len(titles) != len(videos)):
        print("[ERROR] fatal: mismatch between number of videos and title")
        exit(1)
    merged = mergeLists(titles, videos)
    for item in merged:
        print(f" [info] title: {item[0]}")
        if args.verbose:
            print(f"[debug]   - data-apireq: {item[1]}")
    return merged


def getSource(video):
    dataRaw = 'd=' + video
    session = requests.Session()
    response = session.post(
        'https://v.anime1.me/api',
        data=dataRaw,
        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    result = json.loads(response.content.decode("utf-8"))
    if args.verbose:
        print(f"[debug] source: https:{str(result['s'][0]['src'])}")
        print(f"[debug] cookie: {session.cookies.get_dict()}")
        print(f"[debug] raw api response: {response.content.decode('utf-8')}")
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
    videos = extractAPIpath(url)

    sources = []
    cookies = []

    for video in videos:
        src, cookie = getSource(video[1])
        sources.append(src)
        cookies.append(cookie)

    print('_'*50)
    for i in range(len(sources)):
        if not (args.extract):
            downloadVideo(sources[i], cookies[i], videos[i][0])
        else:
            print(f' [info] title: {videos[i][0]}')
            print(f' [info]   - https:{sources[i]}')
            print(f' [info]   - cookie: {cookies[i]}')


try:
    main(url)

except Exception as e:
    print("----    Error    ----")
    print(e)
finally:
    print(" [info] done")
