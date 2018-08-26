#!/usr/bin/env python
# coding: utf-8


from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d["status"] == "finished":
        print("Done downloading, now converting...");


ydl_opts = {
'''
To choose format:

    # Download best format available but not better that 480p.
    $ youtube-dl -f 'bestvideo[height<=480]+bestaudio/best[height<=480]'

    # Download best format available but not better that 720p.
    $ youtube-dl -f 'bestvideo[height<=720]+bestaudio/best[height<=720]'

    # Download best format available but not better that 1080.
    $ youtube-dl -f 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
'''
    'format': ''
}


def main():
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=Yl_K2Ata6XY'])


if __name__ == "__main__":
    main()
