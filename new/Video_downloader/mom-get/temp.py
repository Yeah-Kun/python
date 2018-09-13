"""
	create by Ian in 2018-5-31 09:57:37
	缓存所有需要用到的核心代码
"""

def main(**kwargs):
    """Main entry point.
    you-get (legacy)
    """
    from .common import main
    main(**kwargs)


def download_main(download, download_playlist, urls, playlist, **kwargs):
    for url in urls:
        if re.match(r'https?://', url) is None:
            url = 'http://' + url

        if playlist:
            download_playlist(url, **kwargs)
        else:
            download(url, **kwargs)


def any_download(url, **kwargs):
    m, url = url_to_module(url)
    m.download(url, **kwargs)


def url_to_module(url):
    try:
        video_host = r1(r'https?://([^/]+)/', url)
        video_url = r1(r'https?://[^/]+(.*)', url)
        assert video_host and video_url
    except AssertionError:
        url = google_search(url)
        video_host = r1(r'https?://([^/]+)/', url)
        video_url = r1(r'https?://[^/]+(.*)', url)

    if video_host.endswith('.com.cn') or video_host.endswith('.ac.cn'):
        video_host = video_host[:-3]
    domain = r1(r'(\.[^.]+\.[^.]+)$', video_host) or video_host
    assert domASCII code points must be quoted (percent-encoded UTF-8)
    url = ''.join([ch if ord(ch) in range(128) else parse.quote(ch) for ch in url])
    video_host = r1(r'https?://([^/]+)/', url)
    video_url =ain, 'unsupported url: ' + url

    # all non- r1(r'https?://[^/]+(.*)', url)

    k = r1(r'([^.]+)', domain)
    if k in SITES:
        return (
            import_module('.'.join(['you_get', 'extractors', SITES[k]])),
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
            return import_module('you_get.extractors.universal'), url

def universal_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    try:
        content_type = get_head(url, headers=fake_headers)['Content-Type']
    except:
        content_type = get_head(url, headers=fake_headers, get_method='GET')['Content-Type']
    if content_type.startswith('text/html'):
        try:
            embed_download(url, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
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

        meta_videos = re.findall(r'<meta property="og:video:url" content="([^"]*)"', page)
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

        hls_urls = re.findall(r'(https?://[^;"\'\\]+' + '\.m3u8?' +
                              r'[^;"\'\\]*)', page)
        if hls_urls:
            for hls_url in hls_urls:
                type_, ext, size = url_info(hls_url)
                print_info(site_info, page_title, type_, size)
                if not info_only:
                    download_url_ffmpeg(url=hls_url, title=page_title,
                                        ext='mp4', output_dir=output_dir)
            return

        # most common media file extensions on the Internet
        media_exts = ['\.flv', '\.mp3', '\.mp4', '\.webm',
                      '[-_]1\d\d\d\.jpe?g', '[-_][6-9]\d\d\.jpe?g', # tumblr
                      '[-_]1\d\d\dx[6-9]\d\d\.jpe?g',
                      '[-_][6-9]\d\dx1\d\d\d\.jpe?g',
                      '[-_][6-9]\d\dx[6-9]\d\d\.jpe?g',
                      's1600/[\w%]+\.jpe?g', # blogger
                      'img[6-9]\d\d/[\w%]+\.jpe?g' # oricon?
        ]

        urls = []
        for i in media_exts:
            urls += re.findall(r'(https?://[^;"\'\\]+' + i + r'[^;"\'\\]*)', page)

            p_urls = re.findall(r'(https?%3A%2F%2F[^;&]+' + i + r'[^;&]*)', page)
            urls += [parse.unquote(url) for url in p_urls]

            q_urls = re.findall(r'(https?:\\\\/\\\\/[^;"\']+' + i + r'[^;"\']*)', page)
            urls += [url.replace('\\\\/', '/') for url in q_urls]

        # a link href to an image is often an interesting one
        urls += re.findall(r'href="(https?://[^"]+\.jpe?g)"', page, re.I)
        urls += re.findall(r'href="(https?://[^"]+\.png)"', page, re.I)
        urls += re.findall(r'href="(https?://[^"]+\.gif)"', page, re.I)

        # relative path
        rel_urls = []
        rel_urls += re.findall(r'href="(\.[^"]+\.jpe?g)"', page, re.I)
        rel_urls += re.findall(r'href="(\.[^"]+\.png)"', page, re.I)
        rel_urls += re.findall(r'href="(\.[^"]+\.gif)"', page, re.I)
        for rel_url in rel_urls:
            urls += [ r1(r'(.*/)', url) + rel_url ]

        # MPEG-DASH MPD
        mpd_urls = re.findall(r'src="(https?://[^"]+\.mpd)"', page)
        for mpd_url in mpd_urls:
            cont = get_content(mpd_url)
            base_url = r1(r'<BaseURL>(.*)</BaseURL>', cont)
            urls += [ r1(r'(.*/)[^/]*', mpd_url) + base_url ]

        # have some candy!
        candies = []
        i = 1
        for url in set(urls):
            filename = parse.unquote(url.split('/')[-1])
            if 5 <= len(filename) <= 80:
                title = '.'.join(filename.split('.')[:-1])
            else:
                title = '%s' % i
                i += 1

            candies.append({'url': url,
                            'title': title})

        for candy in candies:
            try:
                try:
                    mime, ext, size = url_info(candy['url'], faker=False)
                    assert size
                except:
                    mime, ext, size = url_info(candy['url'], faker=True)
                    if not size: size = float('Inf')
            except:
                continue
            else:
                print_info(site_info, candy['title'], ext, size)
                if not info_only:
                    try:
                        download_urls([candy['url']], candy['title'], ext, size,
                                      output_dir=output_dir, merge=merge,
                                      faker=False)
                    except:
                        download_urls([candy['url']], candy['title'], ext, size,
                                      output_dir=output_dir, merge=merge,
                                      faker=True)
        return

    else:
        # direct download
        filename = parse.unquote(url.split('/')[-1]) or parse.unquote(url.split('/')[-2])
        title = '.'.join(filename.split('.')[:-1]) or filename
        _, ext, size = url_info(url, faker=True)
        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls([url], title, ext, size,
                          output_dir=output_dir, merge=merge,
                          faker=True)
        return



def get_head(url, headers={}, get_method='HEAD'):
    logging.debug('get_head: %s' % url)

    if headers:
        req = request.Request(url, headers=headers)
    else:
        req = request.Request(url)
    req.get_method = lambda: get_method
    res = urlopen_with_retry(req)
    return dict(res.headers)

# DEPRECATED in favor of match1()
def r1(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m.group(1)


def match1(text, *patterns):
    """Scans through a string for substrings matched some patterns (first-subgroups only).

    Args:
        text: A string to be scanned.
        patterns: Arbitrary number of regex patterns.

    Returns:
        When only one pattern is given, returns a string (None if no match found).
        When more than one pattern are given, returns a list of strings ([] if no match found).
    """

    if len(patterns) == 1:
        pattern = patterns[0]
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None
    else:
        ret = []
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                ret.append(match.group(1))
        return ret


def matchall(text, patterns):
    """Scans through a string for substrings matched some patterns.

    Args:
        text: A string to be scanned.
        patterns: a list of regex pattern.

    Returns:
        a list if matched. empty if not.
    """

    ret = []
    for pattern in patterns:
        match = re.findall(pattern, text)
        ret += match

    return ret


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

def ungzip(data):
    """Decompresses data for Content-Encoding: gzip.
    """
    from io import BytesIO
    import gzip
    buffer = BytesIO(data)
    f = gzip.GzipFile(fileobj=buffer)
    return f.read()


bokecc_patterns = [r'bokecc\.com/flash/pocle/player\.swf\?siteid=(.+?)&vid=(.{32})']

def embed_download(url, output_dir = '.', merge = True, info_only = False ,**kwargs):
    content = get_content(url, headers=fake_headers)
    found = False
    title = match1(content, '<title>([^<>]+)</title>')

    vids = matchall(content, youku_embed_patterns)
    for vid in set(vids):
        found = True
        youku_download_by_vid(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

    vids = matchall(content, tudou_embed_patterns)
    for vid in set(vids):
        found = True
        tudou_download_by_id(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

    vids = matchall(content, yinyuetai_embed_patterns)
    for vid in vids:
        found = True
        yinyuetai_download_by_id(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

    vids = matchall(content, iqiyi_embed_patterns)
    for vid in vids:
        found = True
        iqiyi_download_by_vid((vid[1], vid[0]), title=title, output_dir=output_dir, merge=merge, info_only=info_only)

    urls = matchall(content, netease_embed_patterns)
    for url in urls:
        found = True
        netease_download(url, output_dir=output_dir, merge=merge, info_only=info_only)

    urls = matchall(content, vimeo_embed_patters)
    for url in urls:
        found = True
        vimeo_download_by_id(url, title=title, output_dir=output_dir, merge=merge, info_only=info_only, referer=url)

    urls = matchall(content, dailymotion_embed_patterns)
    for url in urls:
        found = True
        dailymotion_download(url, output_dir=output_dir, merge=merge, info_only=info_only)

    aids = matchall(content, bilibili_embed_patterns)
    for aid in aids:
        found = True
        url = 'http://www.bilibili.com/video/av%s/' % aid
        bilibili_download(url, output_dir=output_dir, merge=merge, info_only=info_only)

    iqiyi_urls = matchall(content, iqiyi_patterns)
    for url in iqiyi_urls:
        found = True
        iqiyi.download(url, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)

    bokecc_metas = matchall(content, bokecc_patterns)
    for meta in bokecc_metas:
        found = True
        bokecc.bokecc_download_by_id(meta[1], output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)

    if found:
        return True

    # Try harder, check all iframes
    if 'recur_lv' not in kwargs or kwargs['recur_lv'] < recur_limit:
        r = kwargs.get('recur_lv')
        if r is None:
            r = 1
        else:
            r += 1
        iframes = matchall(content, [r'<iframe.+?src=(?:\"|\')(.+?)(?:\"|\')'])
        for iframe in iframes:
            if not iframe.startswith('http'):
                src = urllib.parse.urljoin(url, iframe)
            else:
                src = iframe
            found = embed_download(src, output_dir=output_dir, merge=merge, info_only=info_only, recur_lv=r, **kwargs)
            if found:
                return True

    if not found and 'recur_lv' not in kwargs:
        raise NotImplementedError(url)
    else:
        return found


