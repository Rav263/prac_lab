#!/usr/bin/python3

from tkinter import Tk, StringVar, N, W, E, S, SE
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, END
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
        out_file = open(file_name, "wb")
        out_file.write(line)
        out_file.close()
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

    feet_entry = ttk.Entry(mainframe, width=60, textvariable=file_name_label)
    feet_entry.grid(column=1, row=3, sticky=(S))
    feet_entry.bind("<1>",  file_dialog)

    file_text = ScrolledText(mainframe)
    file_text.grid(column=0, row=2, columnspan=6, sticky=(W, E))

    ttk.Button(mainframe, text="Save", command=save_file).grid(column=2, row=3, sticky=(S))
    ttk.Button(mainframe, text="Open", command=open_file).grid(column=3, row=3, sticky=(S))
    ttk.Button(mainframe, text="Clear", command=clear).grid(column=4, row=3, sticky=(S))
    ttk.Button(mainframe, text="Save as", command=save_as_file).grid(column=5, row=3, sticky=(S))

    ttk.Label(mainframe, textvariable=file_err_label).grid(column=0, row=1, columnspan=6, sticky=(W, E))
    ttk.Label(mainframe, text="File name:").grid(column=0, row=3, sticky=W+S)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=10, pady=10)

    feet_entry.focus()

    root.mainloop()


if __name__ == "__main__":
    root = Tk()
    file_name_label = StringVar()
    file_err_label = StringVar()
    file_text = None
    file_name = ""

    main()
