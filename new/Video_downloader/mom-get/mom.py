"""
    create by Ian in 2018-5-31 22:01:39
    mom-get下载器核心代码
"""
import io
import re
import sys
from http import cookiejar
from importlib import import_module


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
SITES = {
    '163': 'netease',
    '56': 'w56',
    'acfun': 'acfun',
    'archive': 'archive',
    'baidu': 'baidu',
    'bandcamp': 'bandcamp',
    'baomihua': 'baomihua',
    'bigthink': 'bigthink',
    'bilibili': 'bilibili',
    'cctv': 'cntv',
    'cntv': 'cntv',
    'cbs': 'cbs',
    'coub': 'coub',
    'dailymotion': 'dailymotion',
    'dilidili': 'dilidili',
    'douban': 'douban',
    'douyin': 'douyin',
    'douyu': 'douyutv',
    'ehow': 'ehow',
    'facebook': 'facebook',
    'fantasy': 'fantasy',
    'fc2': 'fc2video',
    'flickr': 'flickr',
    'freesound': 'freesound',
    'fun': 'funshion',
    'google': 'google',
    'giphy': 'giphy',
    'heavy-music': 'heavymusic',
    'huaban': 'huaban',
    'huomao': 'huomaotv',
    'iask': 'sina',
    'icourses': 'icourses',
    'ifeng': 'ifeng',
    'imgur': 'imgur',
    'in': 'alive',
    'infoq': 'infoq',
    'instagram': 'instagram',
    'interest': 'interest',
    'iqilu': 'iqilu',
    'iqiyi': 'iqiyi',
    'ixigua': 'ixigua',
    'isuntv': 'suntv',
    'joy': 'joy',
    'kankanews': 'bilibili',
    'khanacademy': 'khan',
    'ku6': 'ku6',
    'kuaishou': 'kuaishou',
    'kugou': 'kugou',
    'kuwo': 'kuwo',
    'le': 'le',
    'letv': 'le',
    'lizhi': 'lizhi',
    'longzhu': 'longzhu',
    'magisto': 'magisto',
    'metacafe': 'metacafe',
    'mgtv': 'mgtv',
    'miomio': 'miomio',
    'mixcloud': 'mixcloud',
    'mtv81': 'mtv81',
    'musicplayon': 'musicplayon',
    'naver': 'naver',
    '7gogo': 'nanagogo',
    'nicovideo': 'nicovideo',
    'panda': 'panda',
    'pinterest': 'pinterest',
    'pixnet': 'pixnet',
    'pptv': 'pptv',
    'qingting': 'qingting',
    'qq': 'qq',
    'quanmin': 'quanmin',
    'showroom-live': 'showroom',
    'sina': 'sina',
    'smgbb': 'bilibili',
    'sohu': 'sohu',
    'soundcloud': 'soundcloud',
    'ted': 'ted',
    'theplatform': 'theplatform',
    'tucao': 'tucao',
    'tudou': 'tudou',
    'tumblr': 'tumblr',
    'twimg': 'twitter',
    'twitter': 'twitter',
    'ucas': 'ucas',
    'videomega': 'videomega',
    'vidto': 'vidto',
    'vimeo': 'vimeo',
    'wanmen': 'wanmen',
    'weibo': 'miaopai',
    'veoh': 'veoh',
    'vine': 'vine',
    'vk': 'vk',
    'xiami': 'xiami',
    'xiaokaxiu': 'yixia',
    'xiaojiadianvideo': 'fc2video',
    'ximalaya': 'ximalaya',
    'yinyuetai': 'yinyuetai',
    'miaopai': 'yixia',
    'yizhibo': 'yizhibo',
    'youku': 'youku',
    'iwara': 'iwara',
    'youtu': 'youtube',
    'youtube': 'youtube',
    'zhanqi': 'zhanqi',
    '365yg': 'toutiao',
}

fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # noqa
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',  # noqa
}


def r1(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m.group(1)


def ungzip(data):
    """Decompresses data for Content-Encoding: gzip.
    """
    from io import BytesIO
    import gzip
    buffer = BytesIO(data)
    f = gzip.GzipFile(fileobj=buffer)
    return f.read()


def get_head(url, headers={}, get_method='HEAD'):
    logging.debug('get_head: %s' % url)

    if headers:
        req = request.Request(url, headers=headers)
    else:
        req = request.Request(url)
    # 设定请求方法为"HEAD"，类似于get请求，只不过返回的响应中没有具体的内容，用于获取报头
    req.get_method = lambda: get_method
    res = urlopen_with_retry(req)
    return dict(res.headers)


def get_content(url, headers={}, decoded=True):
    """Gets the content of a URL via sending a HTTP GET request.

    Args:
        url: A URL.
        headers: Request headers used by the client.
        decoded: Whether decode the response body using UTF-8 or the charset specified in Content-Type.

    Returns:
        The content as a string.
    """

    logging.debug('get_content: %s' % url)

    req = request.Request(url, headers=headers)
    if cookies:
        cookies.add_cookie_header(req)
        req.headers.update(req.unredirected_hdrs)

    response = urlopen_with_retry(req)
    data = response.read()

    # Handle HTTP compression for gzip and deflate (zlib)
    content_encoding = response.getheader('Content-Encoding')
    if content_encoding == 'gzip':
        data = ungzip(data)
    elif content_encoding == 'deflate':
        data = undeflate(data)

    # Decode the response body
    if decoded:
        charset = match1(
            response.getheader('Content-Type'), r'charset=([\w-]+)'
        )
        if charset is not None:
            data = data.decode(charset)
        else:
            data = data.decode('utf-8', 'ignore')

    return data


def universal_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    try:
        content_type = get_head(url, headers=fake_headers)['Content-Type']
    except:
        content_type = get_head(url, headers=fake_headers, get_method='GET')[
                                'Content-Type']
    if content_type.startswith('text/html'):
        try:
            embed_download(url, output_dir=output_dir,
                           merge=merge, info_only=info_only, **kwargs)
        except Exception:
            pass
        else:
            return

    domains = url.split('/')[2].split('.')
    if len(domains) > 2: domains = domains[1:]
    site_info = '.'.join(domains)

    if content_type.startswith('text/html'):
        # extract an HTML page
        response = get_response(url, faker=True)
        page = str(response.data)

        page_title = r1(r'<title>([^<]*)', page)
        if page_title:
            page_title = unescape_html(page_title)

        meta_videos = re.findall(
            r'<meta property="og:video:url" content="([^"]*)"', page)
        if meta_videos:
            for meta_video in meta_videos:
                meta_video_url = unescape_html(meta_video)
                type_, ext, size = url_info(meta_video_url)
                print_info(site_info, page_title, type_, size)
                if not info_only:
                    download_urls([meta_video_url], page_title,
                                  ext, size,
                                  output_dir=output_dir, merge=merge,
                                  faker=True)
            return

    else:
        # direct download
        filename = parse.unquote(
            url.split('/')[-1]) or parse.unquote(url.split('/')[-2])
        title = '.'.join(filename.split('.')[:-1]) or filename
        _, ext, size = url_info(url, faker=True)
        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls([url], title, ext, size,
                          output_dir=output_dir, merge=merge,
                          faker=True)
        return


def urlopen_with_retry(*args, **kwargs):
    retry_time = 3
    for i in range(retry_time):
        try:
            return request.urlopen(*args, **kwargs)
        except socket.timeout as e:
            logging.debug('request attempt %s timeout' % str(i + 1))
            if i + 1 == retry_time:
                raise e
        # try to tackle youku CDN fails
        except error.HTTPError as http_error:
            logging.debug('HTTP Error with code{}'.format(http_error.code))
            if i + 1 == retry_time:
                raise http_error


def url_to_module(url):
    try:
        # 将url分成host+url（ip + port）
        video_host = r1(r'https?://([^/]+)/', url)
        video_url = r1(r'https?://[^/]+(.*)', url)
        assert video_host and video_url
    except AssertionError:
        print("URL无法转换为host + url")

    if video_host.endswith('.com.cn') or video_host.endswith('.ac.cn'):
        video_host = video_host[:-3]
    domain = r1(r'(\.[^.]+\.[^.]+)$', video_host) or video_host  # 匹配顶级域名+一级域名
    assert domain, 'unsupported url: ' + url

    url = ''.join([ch if ord(ch) in range(128) else parse.quote(ch)
                  for ch in url])  # 将非ascii编码转换成ascii
    video_host = r1(r'https?://([^/]+)/', url)
    video_url = ain, 'unsupported url: ' + url

    k = r1(r'([^.]+)', domain)  # 消除.com后缀，获得一级域名
    if k in SITES:
        return (
            import_module('.'.join(['extractors', SITES[k]])),
            url
        )
    else:
        import http.client
        video_host = r1(r'https?://([^/]+)/', url)  # .cn could be removed
        if url.startswith('https://'):
            conn = http.client.HTTPSConnection(video_host)
        else:
            conn = http.client.HTTPConnection(video_host)
        conn.request('HEAD', video_url, headers=fake_headers)
        res = conn.getresponse()
        location = res.getheader('location')
        if location and location != url and not location.startswith('/'):
            return url_to_module(location)
        else:
            return import_module('extractors.universal'), url


def main(urls):
    for url in urls:
        if re.match(r'https?://', url) is None:
            url = 'http://' + url
        m, url = url_to_module(url)
        m.download(url)






if __name__ == '__main__':
    main(["http://www.tangdou.com/v94/dAOMNENjwT0zwQ2.html"])
