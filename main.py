#!/usr/bin/python3
"""GUI module for xxd"""

# pylint: disable=unused-argument
# pylint: disable=global-statement
# pylint: disable=invalid-name


from tkinter import Tk, StringVar, W, E, S
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, END
from tkinter import TclError
import subprocess
import sys
from subprocess import PIPE


title = "HEX EDIT"
file_to_save = ""


def open_file(*args):
    """open_file(*args) -> None

    opens file and read it
    """

    global file_name

    file_name = file_name_label.get()
    proc = subprocess.run(["xxd", "-g1", file_name], stdout=PIPE, stderr=PIPE, check=True)
    line = proc.stdout.decode("utf-8")
    err = proc.stderr.decode("utf-8")

    if len(err) != 0:
        file_err_label.set(err)
    else:
        file_err_label.set("")
        file_text.insert(END, line)
        root.title(title + " " + file_name)


def save_as_file(*args):
    """save_as_file(*args) -> None

    saves file as
    """

    global file_name
    file_name = filedialog.asksaveasfilename()
    save_file()


def undo_text(*args):
    """undo_text(*args) -> None

    undo text
    """

    try:
        global file_text
        file_text.edit_undo()
        file_err_label.set("")
    except TclError as err_ex:
        file_err_label.set(str(err_ex))


def redo_text(*args):
    """redo_text(*args) -> None

    redo text
    """

    try:
        global file_text
        file_text.edit_redo()
        file_err_label.set("")
    except TclError as err_ex:
        file_err_label.set(str(err_ex))


def save_file(*args):
    """save_file(*args) -> None

    saves file with file name
    """
    global file_to_save
    global file_name

    if len(file_to_save):
        file_name = file_to_save
        file_to_save = ""

    root.title(title + " " + file_name + " saving...")

    tmp_file = open(file_name + ".swp", "wb")
    tmp_file.write(file_text.get("@0,0", END).encode("utf-8"))
    tmp_file.close()

    proc = subprocess.run(["xxd", "-r", file_name + ".swp"], stdout=PIPE, stderr=PIPE, check=True)
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

    subprocess.run(["rm", file_name + ".swp"], check=True)
    root.title(title + " " + file_name)


def clear(*args):
    """clear(*args) -> None

    clears txt
    """
    global file_name
    file_text.delete("1.0", END)
    file_name = ""
    root.title(title)


def file_dialog(*args):
    """file_dialog(*args) -> None

    get file name from filedialog
    """
    file_name_dial = filedialog.askopenfilename()
    file_name_label.set(file_name_dial)


def find(*args):
    """find(*args) -> None

    searching text in opened file and mark it
    """

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

    # main frame
    mainframe = ttk.Frame(root, width=1280, height=720, padding="3 3 12 12")
    mainframe.grid(column=0, row=0)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # file name entry
    name_entry = ttk.Entry(mainframe, width=60, textvariable=file_name_label)
    name_entry.grid(column=1, row=3, sticky=(S))
    name_entry.bind("<1>", file_dialog)

    # search entry
    search_entry = ttk.Entry(mainframe, width=20, textvariable=search_label)
    search_entry.grid(column=4, row=1, sticky=(S))

    # main scrolled text
    file_text = ScrolledText(mainframe, undo=True)
    file_text.grid(column=0, row=2, columnspan=6, sticky=(W, E))

    # create all buttons
    ttk.Button(mainframe, text="Find", command=find).grid(column=5, row=1, sticky=(S))
    ttk.Button(mainframe, text="Save", command=save_file).grid(column=2, row=3, sticky=(S))
    ttk.Button(mainframe, text="Open", command=open_file).grid(column=3, row=3, sticky=(S))
    ttk.Button(mainframe, text="Clear", command=clear).grid(column=4, row=3, sticky=(S))
    ttk.Button(mainframe, text="Save as", command=save_as_file).grid(column=5, row=3, sticky=(S))
    ttk.Button(mainframe, text="Undo", command=undo_text).grid(column=2, row=1, sticky=(S, W))
    ttk.Button(mainframe, text="Redo", command=redo_text).grid(column=3, row=1, sticky=(S, W))

    # create labels
    err_label = ttk.Label(mainframe, textvariable=file_err_label)
    err_label.grid(column=0, row=1, columnspan=2, sticky=(W, E))
    ttk.Label(mainframe, text="File name:").grid(column=0, row=3, sticky=W+S)

    # set padding for all childs
    for child in mainframe.winfo_children():
        child.grid_configure(padx=10, pady=10)

    args_parse()
    root.mainloop()


def args_parse():
    """args_parse() -> None

    parse comand line args
    """

    if len(sys.argv) == 2:
        file_name_label.set(sys.argv[1])
        open_file()
    elif len(sys.argv) == 3:
        file_name_label.set(sys.argv[1])
        open_file()

        global file_to_save
        file_to_save = sys.argv[2]

if __name__ == "__main__":
    root = Tk()
    file_name_label = StringVar()
    file_err_label = StringVar()
    search_label = StringVar()
    file_text = None
    file_name = ""

    main()
