#!/usr/bin/env python
# coding: utf-8
# author: Vitaliy Pisnya


from __future__ import unicode_literals
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import youtube_dl
#import argparse


class App(ttk.Frame):

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.master.title("Youtube Downloader")
        self.master.geometry("400x200")

        self.link = tk.StringVar()
        self.type = tk.StringVar()
        self.resolution = tk.StringVar()
        self.playlist = tk.IntVar()
        self.destination = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.create_link_entry()
        self.create_type_optionmenu()
        self.create_resolution_optionmenu()
        self.create_playlist_checkbutton()
        self.create_destination_button()
        self.create_download_button()

    def create_link_entry(self):
        self.link.set("Put your link here ...")
        self.link_entry = ttk.Entry(
                self.master,
                takefocus=False,
                width=30,
                foreground="grey",
                textvariable=self.link
                )
        self.link_entry.bind("<FocusIn>", self.on_link_entry_fucus)
        self.link_entry.pack()

    def create_type_optionmenu(self):
        self.choices = [ "", "audio", "video" ]
        self.type.set(self.choices[2])
        self.type_option_menu = ttk.OptionMenu(
                self.master,
                self.type,
                *self.choices
                )
        self.type_option_menu.pack()

    def create_resolution_optionmenu(self):
        self.choices = [ "", 480, 720, 1080 ]
        self.resolution.set(self.choices[2])
        self.resolution_option_menu = ttk.OptionMenu(
                self.master,
                self.resolution,
                *self.choices
                )
        self.resolution_option_menu.pack()

    def create_playlist_checkbutton(self):
        self.playlist.set(0)
        self.playlist_checkbutton = ttk.Checkbutton(
                self.master,
                text='Playlist',
                variable=self.playlist
                )
        self.playlist_checkbutton.pack()

    def create_destination_button(self):
        self.destination.set("~/Downloads")
        self.destination_button = ttk.Button(
                self.master,
                text='Destination',
                command=self.on_destination_button_click
                )
        self.destination_button.pack()

    def on_destination_button_click(self):
        self.destination.set(tk.filedialog.askdirectory(
                initialdir='~/Downloads',
                title='Select directory'
                )
        )

    def create_download_button(self):
        self.download_button = ttk.Button(
                self.master,
                text="Download",
                command=self.on_download_button_click
                )
        self.download_button.pack()

    def on_link_entry_fucus(self, event):
        if str(self.link_entry.cget("foreground")) == "grey":
            self.link_entry.delete(0, "end")
            self.link_entry.insert(0, "")
            self.link_entry.config(foreground="black")

    def on_download_button_click(self):
        self.test()

        #file_name = '%(title)s.%(ext)s'
        #dir_name = Path('.')
        #link = args.link
        #ydl_opts = { 'noplaylist': True }
        #
        #if args.type:
        #    if args.type == 'audio':
        #        ydl_opts['format'] = 'bestaudio/best'
        #        ydl_opts['postprocessors'] = [{
        #                    'key': 'FFmpegExtractAudio',
        #                    'preferredcodec': 'mp3',
        #                    'preferredquality': '192'
        #                    }]
        #    elif args.type == 'video':
        #        if args.resolution:
        #            if args.resolution in [ '720', '1080' ]:
        #                ydl_opts['format'] = 'bestvideo[height<={0}]+bestaudio/best[height<={0}]'.format(args.resolution)
        #            else:
        #                error('ERROR: invalid resolution')
        #    else:
        #        error('ERROR: invalid type')
        #
        #if args.playlist:
        #    ydl_opts['noplaylist'] = False
        #    file_name = '%(playlist_index)s-%(title)s.%(ext)s'
        #
        #if args.path:
        #    dir_name = Path(args.path)
        #    if not (dir_name.exists() and dir_name.is_dir()):
        #        error('\'{}\' is invalid path'.format(dir_name))
        #path = (dir_name / file_name).resolve()
        #ydl_opts['outtmpl'] = str(path)
        #
        #with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #        ydl.download([args.link])

    def test(self):
        print(self.link.get())
        print(self.type.get())
        print(self.resolution.get())
        print(self.playlist.get())
        print(self.destination.get())


def main():
    root = tk.Tk()
    youtube_downloader = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
