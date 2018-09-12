#!/usr/bin/env python
# coding: utf-8
# author: Vitaliy Pisnya


from __future__ import unicode_literals
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import tkinter as tk
import youtube_dl


# TODO: add progression bar


class App(ttk.Frame):

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.master.title("Youtube Downloader")
        self.master.configure(padx=10, pady=10)

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
        self.options = [ "", "audio", "video" ]
        self.type.set(self.options[2])
        self.type_option_menu = ttk.OptionMenu(
                self.master,
                self.type,
                *self.options
                )
        self.type_option_menu.configure(width=5)
        self.type_option_menu.pack()

    def create_resolution_optionmenu(self):
        self.options = [ "", "480p", "720p", "1080p" ]
        self.resolution.set(self.options[2])
        self.resolution_option_menu = ttk.OptionMenu(
                self.master,
                self.resolution,
                *self.options
                )
        self.resolution_option_menu.configure(width=5)
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
        self.destination_button.configure(width=10)
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
        self.download_button.configure(width=10)
        self.download_button.pack()

    def on_link_entry_fucus(self, event):
        if str(self.link_entry.cget("foreground")) == "grey":
            self.link_entry.delete(0, "end")
            self.link_entry.insert(0, "")
            self.link_entry.config(foreground="black")

    def on_download_button_click(self):
        self.name = "%(title)s.%(ext)s"
        self.dir = Path(".")
        self.ydl_opts = { "noplaylist": True }
        
        if self.type.get() == "audio":
            self.ydl_opts["format"] = "bestaudio/best"
            self.ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
                }]
        else:
            self.ydl_opts['format'] = 'bestvideo[height<={0}]+bestaudio/best[height<={0}]'.format(self.resolution.get())
        
        if self.playlist.get() == 1:
            self.ydl_opts["noplaylist"] = False
            self.name = "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"
        
        self.dir = Path(str(self.destination.get())).expanduser()
        if not (self.dir.exists() and self.dir.is_dir()):
            print("\'{}\' is invalid path".format(self.dir))
            exit(1)
        self.path = (self.dir / self.name).resolve()
        self.ydl_opts["outtmpl"] = str(self.path)

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            try:
                print(self.link.get())
                print(self.type.get())
                print(self.resolution.get())
                print(self.path)
                #ydl.download([str(self.link.get())])
            except Exception as e:
                #messagebox.showinfo(message=e)
                exit(1)


def main():
    root = tk.Tk()
    youtube_downloader = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
