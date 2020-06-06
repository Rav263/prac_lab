#!/usr/bin/python3

from tkinter import Tk, StringVar, N, W, E, S, SE, Text
from tkinter import ttk
from tkinter import filedialog, END
import subprocess


def open_file(*args):
    global file_name
    pipe_fd = subprocess.PIPE
    file_name = file_name_label.get()
    proc = subprocess.run(["xxd", "-g1", file_name], stdout=pipe_fd)
    line = proc.stdout.decode("utf-8")
    file_text.insert(END, line)


def save_file(*args):
    pipe_fd = subprocess.PIPE
    open(file_name + ".swp", "wb").write(file_text.get("@0,0", END).encode("utf-8"))
    proc = subprocess.run(["xxd", "-r", file_name + ".swp"], stdout=pipe_fd)
    line = proc.stdout.decode("utf-8")
    open(file_name, "w").write(line)
    subprocess.run(["rm", file_name + ".swp"])


def file_dialog(*args):
    file_name = filedialog.askopenfilename()
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
    file_text = None
    file_name = ""

    main()
