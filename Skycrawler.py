#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Name: Skycrawler.py
Author: Evi1ran
Date Created: November 16, 2019
Description: SkyPixel Videos Crawler
'''

# built-in imports
import os
import sys
import json
import random
import argparse
import textwrap
import threading

# third-party imports
from urllib import request
from urllib import error
from http import cookiejar
from multiprocessing import Pool


def videoDownload(lines):
    threads = []
    for url in lines:
        if "sd" in url.split('/')[-1]:
            file_path = './480p/'
        if "720" in url.split('/')[-1]:
            file_path = './720p/'
        if "1080" in url.split('/')[-1]:
            file_path = './1080p/'
        t = threading.Thread(target=download, args=(url, file_path))
        threads.append(t)
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    print("[*] Download completed!")


def schedule(alist, file_path):
    threads = []
    for url in alist:
        t = threading.Thread(target=download, args=(url, file_path))
        threads.append(t)
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    print("[*] Download completed!")


def download(url, file_path):
    lock.acquire()
    # Completion download file name
    if url == "\n":
        return
    file_path = file_path + url.split('/')[-2] + '-' + url.split('/')[-1]
    # Get the total size of the file
    req1 = request.Request(url)
    res1 = request.urlopen(req1)
    total_size = int(res1.headers['Content-Length'])
    # Compare with local file,
    # implement breakpoint download
    if os.path.exists(file_path):
        temp_size = os.path.getsize(file_path)
        if not temp_size < total_size:
            return
    else:
        temp_size = 0
    req = request.Request(url)
    req.add_header('Range', 'bytes=%d-' % temp_size)
    res = request.urlopen(req)
    with open(file_path, "ab") as f:
        while True:
            chunk = res.read(chunk_size)
            temp_size += len(chunk)
            if not chunk:
                break
            f.write(chunk)
            f.flush()
            # Show download progress
            done = int(50 * temp_size / total_size)
            sys.stdout.write("\r>> Downloading %s %s%s %d%%" % (
                file_path, '█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
            sys.stdout.flush()
    print("\n")
    lock.release()


def buildRequest(url):
    ua_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    ]

    # Fake user-agent,
    # Build http request
    user_agent = random.choice(ua_list)
    req = request.Request(url=url)
    req.add_header('User-Agent', user_agent)
    return req


if __name__ == "__main__":
    lock = threading.Lock()
    chunk_size = 1024
    print('''

    ____  _                                  _
    / ___|| | ___   _  ___ _ __ __ ___      _| | ___ _ __
    \___ \| |/ / | | |/ __| '__/ _` \ \ /\ / / |/ _ \ '__|
    ___) |   <| |_| | (__| | | (_| |\ V  V /| |  __/ |
    |____/|_|\_\\__, |\___|_|  \__,_| \_/\_/ |_|\___|_|
                |___/

                                     --version:1.0 Evi1ran
                                    ''')
    parser = argparse.ArgumentParser(description="SkyPixel Videos Crawler", usage='use "python ' + os.path.basename(
        __file__) + ' -h" for more information', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-u", "--user",
                       help='Configure the $user (https://www.skypixel.com/users/$user) (ex. \'robomas-_user\')')
    parser.add_argument("-k", "--keyword",
                       help='Configure the $keyword (ex. \'vs\')')
    parser.add_argument("-r", "--resolution", type=int, choices=[0, 480, 720, 1080], default='0',
                        help='Configure the $resolution, 0 = download video of all resolutions (default 0)')
    parser.add_argument("-f", "--file", default="./Download.txt",
                        help='Download files list (default ./Download.txt)')
    args = parser.parse_args()
    if args.resolution == 480:
        file_path = './480p/'
    if args.resolution == 720:
        file_path = './720p/'
    if args.resolution == 1080:
        file_path = './1080p/'
    if args.resolution == 0:
        path = ['./480p/', './720p/', './1080p/']
    if os.path.exists(args.file) and os.path.getsize(args.file):
        try:
            print("[*] File detected, start automatic download...")
            f = open(args.file, "r")
            lines = f.readlines()
            print("[*] Start downloading %s videos:" % str(len(lines)))
            videoDownload(lines)
            sys.exit()
        except Exception:
            print("[!] Error: Download URL format is incorrect!")
    else:
        if args.user is None or args.keyword is None:
            parser.print_help()
            sys.exit()
        user_api = 'https://www.skypixel.com/api/v2/users/%s?lang=en-US&platform=web&device=desktop' % args.user
        video_api = 'https://www.skypixel.com/api/v2/users/%s/works?lang=en-US&platform=web&device=desktop&limit=20&offset=' % args.user
        # Set opener for api,
        # ensure the same cookie
        cookie = cookiejar.MozillaCookieJar()
        handler = request.HTTPCookieProcessor(cookie)
        opener = request.build_opener(handler)
        user_req = buildRequest(user_api)

        try:
            # Get the total number of videos from user api
            user_res = opener.open(user_req)
            user_data = json.loads(user_res.read().decode('utf-8'))
            count = user_data['data']['item']['work_count']
            print("[*] User videos:", count)
            alist = []
            blist = []
            clist = []
            alists = [alist, blist, clist]
            video_count = 0
            # Pagination
            for i in range(0, count, 20):
                # Build request for video api
                video_req = buildRequest(video_api+str(i))
                video_res = opener.open(video_req)
                video_data = json.loads(video_res.read().decode('utf-8'))
                video_list = video_data['data']['items']
                for i in range(len(video_list)):
                    video = video_list[i]
                    if args.keyword in json.dumps(video['title']):
                        video_count += 1
                        if args.resolution == 480:
                            alist.append(video['cdn_url']['small'])
                        if args.resolution == 720:
                            alist.append(video['cdn_url']['medium'])
                        if args.resolution == 1080:
                            alist.append(video['cdn_url']['large'])
                        if args.resolution == 0:
                            alist.append(video['cdn_url']['small'])
                            blist.append(video['cdn_url']['medium'])
                            clist.append(video['cdn_url']['large'])

            if video_count > 0:
                f = open(args.file, 'w')
                if args.resolution == 0:
                    for i in range(0, 3):
                        for url in alists[i]:
                            f.write(url + "\n")
                        f.write("\n")
                else:
                    for url in alist:
                        f.write(url + "\n")
                f.close()
                print("[*] Start downloading %s videos: " % video_count)
                if args.resolution == 0:
                    pool = Pool(processes=3)
                    for i in range(0, 3):
                        pool.apply_async(
                            func=schedule, args=(alists[i], path[i]))
                    pool.close()
                    pool.join()
                else:
                    schedule(alist, file_path)
            else:
                print("[!] No eligible videos found!")
        except error.URLError:
            print("[!] Error: URL access failed!")
        except error.HTTPError:
            print("[!] Error: HTTP request failed!")
