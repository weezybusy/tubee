#!/usr/bin/env python
# coding: utf-8


from __future__ import unicode_literals
from pathlib import Path
import argparse
import youtube_dl
import tkinter as tk

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.master.title('YT')

    def create_widgets(self):

        # Entry for a link.
        self.link_var = tk.StringVar()
        self.link_entry = tk.Entry(
                self,
                bd=1,
                textvariable=self.link_var
        )
        self.link_entry.insert(0, "Put your link here ...")
        self.link_entry.bind('<FocusIn>', self.on_entry_click)
        self.link_entry.bind('<FocusOut>', self.on_entry_focusout)
        self.link_entry.config(fg='grey')
        self.link_entry.pack()

        # Radio buttons for type.
        #self.type_var = tk.IntVar()
        #self.audio_radiobutton = tk.Radiobutton(
        #        self,
        #        text="Video",
        #        variable=self.type_var,
        #        value=1,
        #        command=self.get_type
        #)
        #self.audio_radiobutton.pack()
        #self.video_radiobutton = tk.Radiobutton(
        #        self,
        #        text="Audio",
        #        variable=self.type_var,
        #        value=2,
        #        command=self.get_type
        #)
        #self.video_radiobutton.pack()

        # Menu button for resolution.

        # Check button for playlist.

        # Get destination path.

        # Message box

        # Button to start downloading.

    #def get_link(self):
    #    print(self.link_var.get())

    #def get_type(self):
    #    if self.type.get() == 1:
    #        print("Type: audio")
    #    elif self.type_var.get() == 2:
    #        print("Type: video")

    def on_entry_click(self, event):
        """function that gets called whenever entry is clicked"""
        if self.link_entry.get() == 'Put your link here ...':
           self.link_entry.delete(0, "end") # delete all the text in the entry
           self.link_entry.insert(0, '')    #Insert blank for user input
           self.link_entry.config(fg='black')

    def on_entry_focusout(self, event):
        if self.link_entry.get() == '':
           self.link_entry.insert(0, 'Put your link here ...')
           self.link_entry.config(fg='grey')


#def error(msg):
#    print('ERROR: {}.'.format(msg))
#    exit(1)


#def get_parser():
#    parser = argparse.ArgumentParser(
#            description='Audio/video youtube downloader.',
#            formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=80)
#    )
#    parser.add_argument(
#            '-l', '--link',
#            dest='link',
#            metavar='LINK',
#            help='link to content',
#            required=True
#    )
#    parser.add_argument(
#            '-p', '--path',
#            dest='path',
#            metavar='PATH',
#            help='save path',
#    )
#    parser.add_argument(
#            '-t', '--type',
#            dest='type',
#            metavar='TYPE',
#            help='type of content to download'
#    )
#    parser.add_argument(
#            '--playlist',
#            dest='playlist',
#            action='store_true',
#            help='download playlist'
#    )
#    parser.add_argument(
#            '-r', '--resolution',
#            dest='resolution',
#            metavar='RESOLUTION',
#            help='preferable video resolution'
#    )
#    return parser
#
#
#def main():
#    parser = get_parser()
#    args = parser.parse_args()
#    file_name = '%(title)s.%(ext)s'
#    dir_name = Path('.')
#    link = args.link
#    ydl_opts = { 'noplaylist': True }
#
#    if args.type:
#        if args.type == 'audio':
#            ydl_opts['format'] = 'bestaudio/best'
#            ydl_opts['postprocessors'] = [{
#                        'key': 'FFmpegExtractAudio',
#                        'preferredcodec': 'mp3',
#                        'preferredquality': '192'
#                        }]
#        elif args.type == 'video':
#            if args.resolution:
#                if args.resolution in [ '720', '1080' ]:
#                    ydl_opts['format'] = 'bestvideo[height<={0}]+bestaudio/best[height<={0}]'.format(args.resolution)
#                else:
#                    error('ERROR: invalid resolution')
#        else:
#            error('ERROR: invalid type')
#
#    if args.playlist:
#        ydl_opts['noplaylist'] = False
#        file_name = '%(playlist_index)s-%(title)s.%(ext)s'
#
#    if args.path:
#        dir_name = Path(args.path)
#        if not (dir_name.exists() and dir_name.is_dir()):
#            error('\'{}\' is invalid path'.format(dir_name))
#    path = (dir_name / file_name).resolve()
#    ydl_opts['outtmpl'] = str(path)
#
#    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#            ydl.download([args.link])


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
