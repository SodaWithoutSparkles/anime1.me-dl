# anime1.me-dl
Extract URL and/or Download anime from anime1.me

## Install
Go to the [release page](https://github.com/SodaWithoutSparkles/anime1.me-dl/release/latest) and download the source code. Unpack it and start using!

If you are using android with termux installed, you may want to use [this guide](https://github.com/SodaWithoutSparkles/anime1.me-dl/blob/main/termux.md) instead.

## Supported sites
This downloader (or more appropriately an extractor) supports the following sites.

- Tested and verified:
    - `https://anime1.me/<numbers>`, e.g.: `https://anime1.me/18305`
    - `https://anime1.me/category` (will download all videos)

- Does not support:
    - Any other site. This will cause unpredictable and undocumented behaviours.

## Requirements 
- `beautifulsoup4` `4.11.1` or higher
- `requests` `2.25.1` or higher
- `lxml` `4.6.3` or higher
- `yt_dlp` `2022.8.19` or higher (Optional, default, only needed when downloading)


## Usage

```
usage: anime1Downloader.py [-h] [-v] [-x] [-c COOKIE] [-ua USER_AGENT] url

Download anime1.me videos using requsets and beautifulsoup static parser

positional arguments:
  url                   a anime1.me direct url, e.g. https://anime1.me/18305
                        You may need to quote the url

options:
  -h, --help            show this help message and exit
  -v, --verbose         print debug info
  -x, --extract         extract URL only, no download
  -c COOKIE, --cloudflare COOKIE
                        set cf_clearance cookie to bypass cloudflare detection
                        The cookie is valid for an hour
                        You may need to quote the cookie
  -ua USER_AGENT, --user-agent USER_AGENT
                        set user-agent to bypass detection
```

## Tips
- You can use `-x` to extract url only, and use other downloaders
- Cookies must be attached when downloading (done by default)
- If used with other downloaders, make sure to attach the cookie as well
- You don't need yt-dlp if you only use `-x` flag only

