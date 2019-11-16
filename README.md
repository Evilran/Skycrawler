# Skycrawler: SkyPixel Videos Crawler
[![Python 3.7](https://img.shields.io/badge/python-3.7-yellow.svg)](https://www.python.org/)[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Evilran/Skycrawler/blob/master/LICENSE)

    
        ____  _                                  _
        / ___|| | ___   _  ___ _ __ __ ___      _| | ___ _ __
        \___ \| |/ / | | |/ __| '__/ _` \ \ /\ / / |/ _ \ '__|
        ___) |   <| |_| | (__| | | (_| |\ V  V /| |  __/ |
        |____/|_|\_\__, |\___|_|  \__,_| \_/\_/ |_|\___|_|
                    |___/
    
                                         --version:1.0 Evi1ran
    

## API

**代码中所有链接为大疆 api，均由抓包获得，不存在非法手段，请勿用于非法用途！**

用户数据：

```
https://www.skypixel.com/api/v2/users/$USER
```

视频数据

```
https://www.skypixel.com/api/v2/users/$USER/works
```

*($USER 为变量）*

## Support

- Broken-point Continuingly-Downloading


Usage
---
```
optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Configure the $user (https://www.skypixel.com/users/$user) (ex. 'robomas-_user')
  -k KEYWORD, --keyword KEYWORD
                        Configure the $keyword (ex. 'vs')
  -r {0,480,720,1080}, --resolution {0,480,720,1080}
                        Configure the $resolution, 0 = download video of all resolutions (default 0)
  -f FILE, --file FILE  Download files list (default ./Download.txt)
```



Take downloading all RoboMaster competition videos as an example:

```
$ python3 Skycrawler.py -u robomas-_user -k vs
```



Have fun :)

