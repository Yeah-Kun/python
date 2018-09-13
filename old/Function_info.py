import tkinter as tk


def callback():

    listbox.insert(tk.END, "Hello")

if __name__ == "__main__":
    master = tk.Tk()

    button = tk.Button(master, text="ok", command=callback)
    button.pack()

    listbox = tk.Listbox(master)
    listbox.pack()

    tk.mainloop()
