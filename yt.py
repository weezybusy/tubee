#!/usr/bin/env python
# coding: utf-8


from __future__ import unicode_literals
from pathlib import Path
import argparse
import youtube_dl


def error(msg):
    print('ERROR: {}.'.format(msg))
    exit(1)


def get_parser():
    parser = argparse.ArgumentParser(
            description='Audio/video youtube downloader.',
            formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=80)
    )
    parser.add_argument(
            '-l', '--link',
            dest='link',
            metavar='LINK',
            help='link to content',
            required=True
    )
    parser.add_argument(
            '-p', '--path',
            dest='path',
            metavar='PATH',
            help='save path',
    )
    parser.add_argument(
            '-t', '--type',
            dest='type',
            metavar='TYPE',
            help='type of content to download'
    )
    parser.add_argument(
            '--playlist',
            dest='playlist',
            action='store_true',
            help='download playlist'
    )
    parser.add_argument(
            '-r', '--resolution',
            dest='resolution',
            metavar='RESOLUTION',
            help='preferable video resolution'
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    file_name = '%(title)s.%(ext)s'
    dir_name = Path('.')
    link = args.link
    ydl_opts = { 'noplaylist': True }

    if args.type:
        if args.type == 'audio':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192'
                        }]
        elif args.type == 'video':
            if args.resolution:
                if args.resolution in [ '720', '1080' ]:
                    ydl_opts['format'] = 'bestvideo[height<={0}]+bestaudio/best[height<={0}]'.format(args.resolution)
                else:
                    error('ERROR: invalid resolution')
        else:
            error('ERROR: invalid type')

    if args.playlist:
        ydl_opts['noplaylist'] = False
        file_name = '%(playlist_index)s-%(title)s.%(ext)s'

    if args.path:
        dir_name = Path(args.path)
        if not (dir_name.exists() and dir_name.is_dir()):
            error('\'{}\' is invalid path'.format(dir_name))
    path = (dir_name / file_name).resolve()
    ydl_opts['outtmpl'] = str(path)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([args.link])


if __name__ == "__main__":
    main()
