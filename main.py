#!/usr/bin/python3

from tkinter import Tk, StringVar, N, W, E, S, SE
from tkinter import ttk
from tkinter import filedialog


def open_file(*args):
    pass


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
    root.title("HEX EDIT")
    root.geometry("1280x720")

    mainframe = ttk.Frame(root, width=1280, height=720, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    feet_entry = ttk.Entry(mainframe, width=100, textvariable=file_name_label)
    feet_entry.grid(column=4, row=10, sticky=(S))
    feet_entry.bind("<1>",  file_dialog)

    ttk.Label(mainframe, textvariable=file_text).grid(column=2, row=2, sticky=(W, E))
    ttk.Button(mainframe, text="Save", command=save_file).grid(column=5, row=3, sticky=SE)
    ttk.Button(mainframe, text="Open", command=open_file).grid(column=3, row=1, sticky=SE)

    ttk.Label(mainframe, text="File name:").grid(column=1, row=1, sticky=W)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=10, pady=10)

    feet_entry.focus()
    root.bind('<Return>', open_file)

    root.mainloop()


if __name__ == "__main__":
    root = Tk()
    file_name_label = StringVar()
    file_text = StringVar()

    main()
