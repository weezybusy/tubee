#!/usr/bin/env python
# coding: utf-8


from __future__ import unicode_literals
import youtube_dl
import argparse


def error(msg):
    print('ERROR: {}'.format(msg))
    exit(2)


def get_parser():
    parser = argparse.ArgumentParser(
            description='Audio/video youtube downloader.',
            formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=80)
    )
    parser.add_argument(
            '-d', '--directory',
            dest='directory',
            metavar='DIRECTORY',
            help='save directory'
    )
    parser.add_argument(
            '-l', '--link',
            dest='link',
            metavar='LINK',
            help='link to content'
    )
    parser.add_argument(
            '-t', '--type',
            dest='type',
            metavar='TYPE',
            help='type of content to download'
    )
    parser.add_argument(
            '-p', '--playlist',
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
    ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True
    }
    # TODO:
    #       1. Get path
    #       2. Write tests
    path = ''

    if not args.link:
        error('Expected link')

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
                    error('ERROR: invalid resolution.')
        else:
            error('ERROR: invalid type.')

    if args.playlist:
        ydl_opts['noplaylist'] = False
        ydl_opts['outtmpl'] = '%(playlist_index)s-%(title)s.%(ext)s'

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([args.link])


if __name__ == "__main__":
    main()
