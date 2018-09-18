#!/usr/bin/env python
# coding: utf-8
# author: Vitaliy Pisnya


from __future__ import unicode_literals
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import tkinter as tk
import youtube_dl


debug = False


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

        self.create_link_entry()
        self.create_type_combobox()
        self.create_resolution_combobox()
        self.create_playlist_checkbutton()
        self.create_destination_button()
        self.create_download_button()
        self.create_progressbar()

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
        self.link_entry.pack(anchor=tk.W)

    def create_type_combobox(self):
        self.type.set("video")
        self.type_combobox = ttk.Combobox(
                self.master,
                values="audio video",
                state="readonly",
                textvariable=self.type,
                )
        self.type_combobox.configure(width=10)
        self.type_combobox.pack(anchor=tk.W)
        self.type_combobox.bind("<<ComboboxSelected>>", self.on_new_type_selection)

    def create_resolution_combobox(self):
        self.resolution.set("720")
        self.resolution_combobox = ttk.Combobox(
                self.master,
                values="360 480 720 1080",
                state="readonly",
                textvariable=self.resolution
                )
        self.resolution_combobox.configure(width=10)
        self.resolution_combobox.pack(anchor=tk.W)

    def create_playlist_checkbutton(self):
        self.playlist.set(0)
        self.playlist_checkbutton = ttk.Checkbutton(
                self.master,
                text='Playlist',
                variable=self.playlist
                )
        self.playlist_checkbutton.pack(anchor=tk.W)

    def create_destination_button(self):
        self.destination.set("~/Downloads")
        self.destination_button = ttk.Button(
                self.master,
                text='Destination',
                command=self.on_destination_button_click
                )
        self.destination_button.configure(width=10)
        self.destination_button.pack(anchor=tk.W)

    def create_download_button(self):
        self.download_button = ttk.Button(
                self.master,
                text="Download",
                command=self.on_download_button_click
                )
        self.download_button.configure(width=10)
        self.download_button.pack(anchor=tk.W)

    # TODO: create progress bar?
    def create_progressbar(self):
        self.progressbar = ttk.Progressbar(
                self,
                orient="horizontal",
                length=100,
                mode='determinate'
                )
        self.progressbar.pack()

    def on_destination_button_click(self):
        self.destination.set(tk.filedialog.askdirectory(
                initialdir='~/Downloads',
                title='Select directory'
                )
            )

    def on_link_entry_fucus(self, event):
        if str(self.link_entry.cget("foreground")) == "grey":
            self.link_entry.delete(0, "end")
            self.link_entry.insert(0, "")
            self.link_entry.config(foreground="black")

    def on_new_type_selection(self, event):
        if self.type.get() == 'audio':
            self.resolution_combobox.configure(state='disabled')
        else:
            self.resolution_combobox.configure(state='readonly')

    def on_download_button_click(self):
        self.name = "%(title)s.%(ext)s"
        self.ydl_opts = {
                "noplaylist": True,
                "quiet": True
                }
        
        if self.type.get() == "audio":
            self.ydl_opts["format"] = "bestaudio/best"
            self.ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
                }]
        else:
            self.ydl_opts['format'] = f"bestvideo[height<={self.resolution.get()}]+bestaudio/best"
        
        if self.playlist.get() == 1:
            self.ydl_opts["noplaylist"] = False
            self.name = "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"
        
        self.path = Path(self.destination.get()).expanduser()
        self.ydl_opts["outtmpl"] = str((self.path / self.name).resolve())

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            try:
                ydl.download([self.link.get()])
            except youtube_dl.DownloadError as e:
                messagebox.showerror(message="Error: invalid URL.")
                exit(1)


def main():
    root = tk.Tk()
    youtube_downloader = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
