#!/usr/bin/env python
# coding: utf-8
# author: Vitaliy Pisnya


from __future__ import unicode_literals
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import tkinter as tk
import youtube_dl


class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Youtube Downloader")

        self.link = tk.StringVar()
        self.type = tk.StringVar()
        self.resolution = tk.StringVar()
        self.playlist = tk.IntVar()
        self.destination = tk.StringVar()

        self.default_fg = "#282828"

        self.create_link_entry()
        self.create_type_combobox()
        self.create_resolution_combobox()
        self.create_playlist_checkbutton()
        self.create_destination_button()
        self.create_download_button()

    # TODO: add scrollbar to entry.
    def create_link_entry(self):
        style = ttk.Style()
        style.configure("LinkEntry.TEntry", selectbackground=self.default_fg,
                selectforeground="white")
        self.link.set("Put your link here ...")
        self.link_entry = ttk.Entry(
                self.master,
                takefocus=False,
                width=47,
                foreground="grey",
                textvariable=self.link,
                style="LinkEntry.TEntry"
                )
        self.link_entry.bind("<FocusIn>", self.on_link_entry_fucus)
        self.link_entry.grid(row=0, column=0, padx=5, pady=5, columnspan=4,
                sticky=tk.W+tk.E)

    def create_type_combobox(self):
        style = ttk.Style()
        style.configure("Type.TCombobox", foreground=self.default_fg)
        self.type.set("video")
        self.type_combobox = ttk.Combobox(
                self.master,
                values="audio video",
                state="readonly",
                textvariable=self.type,
                )
        self.type_combobox.configure(width=10, style="Type.TCombobox")
        self.type_combobox.bind("<<ComboboxSelected>>",
                self.on_new_type_selection)
        self.type_combobox.grid(row=2, column=0)

    def create_resolution_combobox(self):
        style = ttk.Style()
        style.configure("Resolution.TCombobox", foreground=self.default_fg)
        self.resolution.set("720")
        self.resolution_combobox = ttk.Combobox(
                self.master,
                values="360 480 720 1080",
                width=10,
                state="readonly",
                textvariable=self.resolution,
                style="Resolution.TCombobox"
                )
        self.resolution_combobox.bind("<<ComboboxSelected>>",
                self.on_new_resolution_selection)
        self.resolution_combobox.grid(row=2, column=1)

    # TODO: find out how to change color of dot.
    def create_playlist_checkbutton(self):
        style = ttk.Style()
        style.configure("Playlist.TCheckbutton", foreground=self.default_fg)
        self.playlist.set(0)
        self.playlist_checkbutton = ttk.Checkbutton(
                self.master,
                text='Playlist',
                variable=self.playlist,
                style="Playlist.TCheckbutton"
                )
        self.playlist_checkbutton.configure
        self.playlist_checkbutton.grid(row=2, column=2)

    def create_destination_button(self):
        style = ttk.Style()
        style.configure("Destination.TButton", foreground=self.default_fg)
        self.destination.set("~/Downloads")
        self.destination_button = ttk.Button(
                self.master,
                text='Destination',
                style="Destination.TButton",
                command=self.on_destination_button_click
                )
        self.destination_button.configure(width=10)
        self.destination_button.grid(row=2, column=3)

    def create_download_button(self):
        style = ttk.Style()
        style.configure("Download.TButton", background="green",
                foreground="white",  font=("TkDefaultFont", 10, "bold"))
        style.map("Download.TButton",
                background=[
                    ("disabled", "yellow"),
                    ("pressed", "#ff471a"),
                    ("active", "red")
                    ],
                relief=[ ('pressed', '!disabled', 'sunken') ]
                )
        self.download_button = ttk.Button(
                self.master,
                text="Download",
                command=self.on_download_button_click,
                style="Download.TButton"
                )
        self.download_button.configure(width=10)
        self.download_button.grid(padx=5, pady=10, columnspan=4)
        self.download_button_is_clicked = False

    def on_destination_button_click(self):
        self.destination.set(tk.filedialog.askdirectory(
                initialdir='~/Downloads',
                title='Select directory'
                )
            )

    def on_link_entry_fucus(self, event):
        colors = [ "grey", "red" ]
        if str(self.link_entry.cget("foreground")) in colors:
            self.link_entry.delete(0, "end")
            self.link_entry.insert(0, "")
            self.link_entry.config(foreground=self.default_fg)

    def on_new_type_selection(self, event):
        self.type_combobox.selection_clear()
        if self.type.get() == 'audio':
            self.resolution_combobox.configure(state='disabled')
        else:
            self.resolution_combobox.configure(state='readonly')

    def on_new_resolution_selection(self, event):
        self.resolution_combobox.selection_clear()

    def on_download_button_click(self):

        if self.download_button_is_clicked == True:
            return
        self.download_button_is_clicked = True

        name = "%(title)s.%(ext)s"
        ydl_opts = {
                "noplaylist": True,
                "quiet": True
                }

        if self.type.get() == "audio":
            ydl_opts["format"] = "bestaudio/best"
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
                }]
        else:
            ydl_opts['format'] = f"(mp4)[height<={self.resolution.get()}]"

        if self.playlist.get() == 1:
            ydl_opts["noplaylist"] = False
            name = "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"

        path = Path(self.destination.get()).expanduser()
        ydl_opts["outtmpl"] = str((path / name).resolve())

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([self.link.get()])
            except Exception:
                self.link_entry.configure(foreground="red")
                self.link.set("Download error")

        self.on_download_complete()


    def on_download_complete(self):
        self.download_button_is_clicked = False
        self.link_entry.set("Download complete")



def main():
    root = tk.Tk()
    youtube_downloader = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
