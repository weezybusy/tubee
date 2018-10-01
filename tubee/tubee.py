#!/usr/bin/env python
# coding: utf-8
# author: Vitaliy Pisnya


from __future__ import unicode_literals
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import tkinter as tk
import youtube_dl


class MyLogger(object):

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


class AutoScrollbar(ttk.Scrollbar):

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError("cannot use pack with this widget")

    def place(self, **kw):
        raise tk.TclError("cannot use place with this widget")


class App:

    def __init__(self, master=None):
        self.master = master
        self.master.title("tubee")
        self.create_variables()
        self.create_colors()
        self.create_styles()
        self.create_widgets()

    def create_variables(self):
        self.link = tk.StringVar()
        self.status = tk.StringVar()
        self.type = tk.StringVar()
        self.resolution = tk.StringVar()
        self.playlist = tk.IntVar()
        self.destination = tk.StringVar()

    def create_colors(self):
        self.color1 = "#ffffff"
        self.color2 = "#6b7d81"
        self.color3 = "#43474f"

    def create_styles(self):
        self.style = ttk.Style()
        self.style.configure("TEntry", foreground=self.color3,
                selectforeground=self.color3, selectbackground=self.color1)
        self.style.configure("TCombobox", foreground=self.color3)
        self.style.map("TCombobox", fieldbackground=[("readonly", self.color1)])
        self.master.option_add("*TCombobox*Listbox.selectBackground", self.color2)
        self.master.option_add("*TCombobox*Listbox.selectForeground", self.color1)
        self.master.option_add("*TCombobox*Listbox.foreground", self.color3)
        self.style.configure("TCheckbutton", foreground=self.color3)
        self.style.configure("TButton", foreground=self.color3)
        self.style.configure("Download.TButton", background=self.color3,
                foreground=self.color1, relief="flat",
                font=("TkDefaultFont", 10, "bold"))
        self.style.map("Download.TButton",
                background=[
                    ("disabled", self.color2),
                    ("pressed", self.color2),
                    ("active", self.color2)
                    ],
                relief=[("pressed", "!disabled", "sunken")]
                )
        self.style.configure("Status.TLabel", foreground=self.color3)

    def create_widgets(self):
        self.create_entry_frame()
        self.create_type_combobox()
        self.create_resolution_combobox()
        self.create_playlist_checkbutton()
        self.create_destination_button()
        self.create_download_button()
        self.create_status_label()

    def create_entry_frame(self):
        self.entry_frame = ttk.Frame(self.master)
        self.entry_frame.grid(row=0, column=0, padx=5, pady=5, columnspan=5,
                sticky=tk.W+tk.E)
        self.create_link_entry()

    def create_link_entry(self):
        self.link_entry = ttk.Entry(
                self.entry_frame,
                width=50,
                foreground=self.color2,
                textvariable=self.link,
                )
        self.link_entry.bind("<FocusIn>", self.on_link_entry_focus)
        self.link.set("Put your link here ...")
        self.link_entry.grid(row=0, column=0, columnspan=5, sticky=tk.W+tk.E)
        self.create_entry_scrollbar()
        self.link_entry.configure(xscrollcommand=self.entry_scrollbar.set)

    def create_entry_scrollbar(self):
        self.entry_scrollbar = AutoScrollbar(
                self.entry_frame,
                orient=tk.HORIZONTAL,
                command=self.link_entry.xview
                )
        self.entry_scrollbar.grid(row=1, column=0, columnspan=5,
                sticky=tk.W+tk.E)

    def create_type_combobox(self):
        self.type_combobox = ttk.Combobox(
                self.master,
                values="audio video",
                state="readonly",
                width=5,
                textvariable=self.type
                )
        self.type_combobox.bind("<<ComboboxSelected>>",
                self.on_type_selection)
        self.type.set("video")
        self.type_combobox.grid(row=3, column=0)

    def create_resolution_combobox(self):
        self.resolution_combobox = ttk.Combobox(
                self.master,
                values="360 480 720 1080",
                width=5,
                state="readonly",
                textvariable=self.resolution,
                )
        self.resolution_combobox.bind("<<ComboboxSelected>>",
                self.on_resolution_selection)
        self.resolution.set("720")
        self.resolution_combobox.grid(row=3, column=1)

    def create_playlist_checkbutton(self):
        self.playlist_checkbutton = ttk.Checkbutton(
                self.master,
                text="Playlist",
                variable=self.playlist,
                takefocus=False
                )
        self.playlist.set(0)
        self.playlist_checkbutton.grid(row=3, column=2)

    def create_destination_button(self):
        self.destination_button = ttk.Button(
                self.master,
                text="Destination",
                width=10,
                style="Destination.TButton",
                takefocus=False,
                command=self.on_destination_button_click
                )
        self.destination.set("~/Downloads")
        self.destination_button.grid(row=3, column=3)

    def create_download_button(self):
        self.download_button = ttk.Button(
                self.master,
                text="Download",
                width=10,
                style="Download.TButton",
                takefocus=False,
                command=self.on_download_button_click,
                )
        self.download_button.grid(row=3, column=4)
        self.download_button_is_clicked = False

    def create_status_label(self):
        self.status_label = ttk.Label(
                self.master,
                textvariable=self.status,
                style="Status.TLabel"
                )
        self.status.set("Status is shown here")
        self.status_label.grid(row=5, column=0, padx=5, pady=5, columnspan=5,
                sticky=tk.W)

    def on_link_entry_focus(self, event):
        if str(self.link_entry.cget("foreground")) == self.color2:
            self.link.set("")
            self.link_entry.config(foreground=self.color3)
        self.status.set("")

    def on_destination_button_click(self):
        self.destination.set(
                tk.filedialog.askdirectory(
                    initialdir="~/Downloads",
                    title="Select destination directory"
                    )
                )

    def on_type_selection(self, event):
        self.type_combobox.selection_clear()
        if self.type.get() == "audio":
            self.resolution_combobox.configure(state="disabled")
        else:
            self.resolution_combobox.configure(state="readonly")

    def on_resolution_selection(self, event):
        self.resolution_combobox.selection_clear()

    def my_hook(self, data):
        if data["status"] == "finished":
            self.status.set("Downloading complete")

    def on_download_button_click(self):
        if self.link.get() == "" or self.link.get() == "Put your link here ...":
            self.status.set("Please, insert the link")
            return

        if self.download_button_is_clicked == True:
            return
        self.download_button_is_clicked = True

        name = "%(title)s.%(ext)s"
        ydl_opts = {
                "noplaylist": True,
                "quiet": True,
                "logger": MyLogger(),
                "progress_hooks": [self.my_hook]
                }
        if self.type.get() == "audio":
            ydl_opts["format"] = "bestaudio/best"
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
                }]
        else:
            ydl_opts["format"] = f"(mp4)[height<={self.resolution.get()}]"

        if self.playlist.get() == 1:
            ydl_opts["noplaylist"] = False
            name = "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"
        path = Path(self.destination.get()).expanduser()
        ydl_opts["outtmpl"] = str((path / name).resolve())

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([self.link.get()])
            except Exception:
                self.status.set("Download error")

        self.download_button_is_clicked = False


def main():
    root = tk.Tk()
    youtube_downloader = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
