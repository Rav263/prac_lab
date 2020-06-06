#!/usr/bin/python3

from tkinter import Tk, StringVar, N, W, E, S, SE
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, END
from tkinter import TclError
import subprocess
from subprocess import PIPE


title = "HEX EDIT"


def open_file(*args):
    global file_name
    file_name = file_name_label.get()
    proc = subprocess.run(["xxd", "-g1", file_name], stdout=PIPE, stderr=PIPE)
    line = proc.stdout.decode("utf-8")
    err = proc.stderr.decode("utf-8")
    if len(err) != 0:
        file_err_label.set(err)
    else:
        file_err_label.set("")
        file_text.insert(END, line)
        root.title(title + " " + file_name)


def save_as_file(*args):
    global file_name
    file_name = filedialog.asksaveasfilename()
    save_file()


def undo_text(*args):
    try:
        global file_text
        file_text.edit_undo()
        file_err_label.set("")
    except TclError as err_ex:
        file_err_label.set(str(err_ex))


def redo_text(*args):
    try:
        global file_text
        file_text.edit_redo()
        file_err_label.set("")
    except TclError as err_ex:
        file_err_label.set(str(err_ex))


def save_file(*args):
    root.title(title + " " + file_name + " saving...")
    
    tmp_file = open(file_name + ".swp", "wb")
    tmp_file.write(file_text.get("@0,0", END).encode("utf-8"))
    tmp_file.close()

    proc = subprocess.run(["xxd", "-r", file_name + ".swp"], stdout=PIPE, stderr=PIPE)
    line = proc.stdout
    err = proc.stderr.decode("utf-8")
    
    if len(err) != 0:
        file_err_label.set(err.strip())
    else:
        try:
            out_file = open(file_name, "wb")
            out_file.write(line)
            out_file.close()
        except PermissionError as err_ex:
            file_err_label.set(str(err_ex).strip())
        except FileNotFoundError:
            file_err_label.set("FILE NOT OPENED")
    
    subprocess.run(["rm", file_name + ".swp"])
    root.title(title + " " + file_name)


def clear(*args):
    global file_name
    file_text.delete("1.0", END)
    file_name = ""
    root.title(title)


def file_dialog(*args):
    file_name = filedialog.askopenfilename()
    file_name_label.set(file_name)


def find(*args):
    file_text.tag_remove('found', '1.0', END)
    to_find = search_label.get()
    if to_find:
        idx = '1.0'
        while True:
            idx = file_text.search(to_find, idx, nocase=1, stopindex=END)
            if not idx:
                break
            lastidx = '%s+%dc' % (idx, len(to_find))
            file_text.tag_add('found', idx, lastidx)
            idx = lastidx
        file_text.tag_config('found', foreground='red', background="gray")


def main():
    """
    main() -> None\n

    create main Frame
    create all widgets
    start main loop
    """
    global file_text

    root.title(title)

    mainframe = ttk.Frame(root, width=1280, height=720, padding="3 3 12 12")
    mainframe.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    name_entry = ttk.Entry(mainframe, width=60, textvariable=file_name_label)
    name_entry.grid(column=1, row=3, sticky=(S))
    name_entry.bind("<1>",  file_dialog)

    name_entry = ttk.Entry(mainframe, width=20, textvariable=search_label)
    name_entry.grid(column=4, row=1, sticky=(S))
    
    ttk.Button(mainframe, text="Find", command=find).grid(column=5, row=1, sticky=(S))

    file_text = ScrolledText(mainframe, undo=True)
    file_text.grid(column=0, row=2, columnspan=6, sticky=(W, E))

    ttk.Button(mainframe, text="Save", command=save_file).grid(column=2, row=3, sticky=(S))
    ttk.Button(mainframe, text="Open", command=open_file).grid(column=3, row=3, sticky=(S))
    ttk.Button(mainframe, text="Clear", command=clear).grid(column=4, row=3, sticky=(S))
    ttk.Button(mainframe, text="Save as", command=save_as_file).grid(column=5, row=3, sticky=(S))

    ttk.Label(mainframe, textvariable=file_err_label).grid(column=0, row=1, columnspan=2, sticky=(W, E))
    ttk.Button(mainframe, text="Undo", command=undo_text).grid(column=2, row=1, sticky=(S, W))
    ttk.Button(mainframe, text="Redo", command=redo_text).grid(column=3, row=1, sticky=(S, W))
    ttk.Label(mainframe, text="File name:").grid(column=0, row=3, sticky=W+S)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    root = Tk()
    file_name_label = StringVar()
    file_err_label = StringVar()
    search_label = StringVar()
    file_text = None
    file_name = ""

    main()
