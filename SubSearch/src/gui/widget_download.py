import tkinter as tk
from tkinter import ttk

import sv_ttk
from src.gui import tkinter_data as tkd
from src.gui import widget_root
from src.scraper import subscene_soup
from src.utilities import file_manager, local_paths


# file with subtitles and corresponding dl links
def read_tmp_file(file: str):
    with open(file, "r") as f:
        return [line.strip() for line in f]


# download said subtitle to the folder with the video file in it
class DownloadList(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # listbox for the subtitles
        self.extent = 0
        self.sublist_lenght = len(SUBLIST)
        self.hs = ttk.Scrollbar(root, orient="vertical", style="Vertical.TScrollbar")
        sub_listbox = tk.Listbox(
            root,
            bg=tkd.Color.dark_grey,
            fg=tkd.Color.light_grey,
            font=tkd.Font.cas8b,
            bd=0,
            border=0,
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=self.hs.set,
        )
        sub_listbox.place(
            height=tkd.Window.height - 60,
            width=tkd.Window.width - 20,
            relx=0.5,
            rely=0.525,
            bordermode="inside",
            anchor="center",
        )
        self.count = 0
        self.sub_listbox = sub_listbox
        self.sublist = SUBLIST
        self.fill_listbox()
        # custom scrollbar
        scrollbar_lengt = 50
        self.scrollbar_lengt = scrollbar_lengt
        self.scrollbar_lenght_half = round(scrollbar_lengt / 2)
        style = ttk.Style()
        style.theme_use("sun-valley-dark")
        style.element_options("Vertical.TScrollbar.thumb")
        # configure the style
        style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            state="disable",
            relief="flat",
            borderwidth=0,
            bd=0,
            arrowsize=24,
        )

        self.hs.place(x=tkd.Window.width - 28, y=51, bordermode="inside", height=633)
        self.hs.config(command=self.sub_listbox.yview)
        self.hs.lift()

    def fill_listbox(self):
        dicts_names = {}
        dicts_urls = {}
        # fil list box with all available subtitles that were found and not downloaded
        for x, i in zip(range(0, self.sublist_lenght), self.sublist):
            x = i.split(" ")
            match = f"{x[0]} {x[1]}"
            name = x[2]
            url = x[-1]
            txt = f"{match} {name}"
            self.sub_listbox.insert(tk.END, f"{match} {name}\n")
            self.sub_listbox.bind("<ButtonPress-1>", self.mouse_b1_press)
            dicts_names[self.count] = txt
            dicts_urls[self.count] = url
            self.dicts_urls = dicts_urls
            self.dicts_names = dicts_names
            self.count += 1

    def mouse_b1_press(self, event):
        self.sub_listbox.bind("<<ListboxSelect>>", self.download_button)

    def mouse_b1_release(self, event):
        self.sub_listbox.bind("<ButtonPress-1>", self.mouse_b1_press)

    def download_button(self, event):
        self.sub_listbox.unbind("<<ListboxSelect>>")
        self.sub_listbox.bind("<ButtonRelease-1>", self.mouse_b1_release)
        _i = str(self.sub_listbox.curselection())
        _i = _i.replace("(", "")
        _i = _i.replace(")", "")
        items = _i.replace(",", "")
        _error = False
        for (number, url), (name) in zip(self.dicts_urls.items(), self.dicts_names.values()):
            if number == int(items):
                self.sub_listbox.delete(int(number))
                self.sub_listbox.insert(int(number), f"?????? DOWNLOADING ??????")
                self.sub_listbox.itemconfig(int(number), {"fg": tkd.Color.blue})
                try:
                    dl_url = subscene_soup.get_download_url(url)
                    _name = name.replace("/", "").replace("\\", "").split(": ")
                    path = f"{local_paths.cwd()}\\{_name[-1]}.zip"
                    item = path, dl_url, 1, 1
                    file_manager.download_zip_auto(item)
                    if _error is False:
                        file_manager.extract_zips(local_paths.cwd(), ".zip")
                        file_manager.clean_up(local_paths.cwd(), ".zip")
                        file_manager.clean_up(local_paths.cwd(), ").nfo")
                        self.sub_listbox.delete(int(number))
                        self.sub_listbox.insert(int(number), f"??? {name}")
                        self.sub_listbox.itemconfig(int(number), {"fg": tkd.Color.green})
                        _error = False
                except OSError:
                    _error = True
                    self.sub_listbox.delete(int(number))
                    self.sub_listbox.insert(int(number), f"????????? Download failed ?????????")
                    self.sub_listbox.itemconfig(int(number), {"fg": tkd.Color.red})


SUBLIST = read_tmp_file("tmp.txt")


def show_widget():
    global root
    root = widget_root.main()
    sv_ttk.set_theme("dark")
    DownloadList(root).pack(anchor="center")
    tk.Frame(root, bg=tkd.Color.dark_grey).pack(anchor="center", expand=True)
    root.mainloop()
