#!/usr/bin/python3

from tkinter import Tk, StringVar, N, W, E, S, SE, Text
from tkinter import ttk
from tkinter import filedialog, END
import subprocess


def open_file(*args):
    pipe_fd = subprocess.PIPE
    proc = subprocess.run(["xxd", "-g1", file_name_label.get()], stdout=pipe_fd)
    line = proc.stdout.decode("utf-8")
    file_text.insert(END,line)


def save_file(*args):
    pass


def file_dialog(*args):
    file_name = filedialog.askopenfilename()
    print(file_name)
    file_name_label.set(file_name)


def main():
    """
    main() -> None\n

    create main Frame
    create all widgets
    start main loop
    """
    global file_text

    root.title("HEX EDIT")

    mainframe = ttk.Frame(root, width=1280, height=720, padding="3 3 12 12")
    mainframe.grid(column=0, row=0) # , sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    feet_entry = ttk.Entry(mainframe, width=60, textvariable=file_name_label)
    feet_entry.grid(column=1, row=3, sticky=(S))
    feet_entry.bind("<1>",  file_dialog)

    file_text = Text(mainframe)
    file_text.grid(column=1, row=2, sticky=(S, E))
    ttk.Button(mainframe, text="Save", command=save_file).grid(column=2, row=3, sticky=(S))
    ttk.Button(mainframe, text="Open", command=open_file).grid(column=3, row=3, sticky=(S))

    ttk.Label(mainframe, text="File name:").grid(column=0, row=3, sticky=W+S)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=10, pady=10)

    feet_entry.focus()
    root.bind('<Return>', open_file)

    root.mainloop()


if __name__ == "__main__":
    root = Tk()
    file_name_label = StringVar()
    file_text = Text()

    main()
