import tkinter as tk
from tkinter import messagebox
import os

def launch_gui(hosts, light_mode):
    bg_color = "#ffffff" if light_mode else "#1e1e1e"
    fg_color = "#000000" if light_mode else "#ffffff"
    btn_color = "#f0f0f0" if light_mode else "#333333"

    def connect_ssh(event=None):
        selection = listbox.curselection()
        if selection:
            host = listbox.get(selection[0])
            os.system(f'start wt ssh {host}')
        else:
            messagebox.showinfo("No selection", "Please select a host to connect.")

    root = tk.Tk()
    root.title("SSH Launcher")
    root.configure(bg=bg_color)

    tk.Label(root, text="Select SSH Host:", bg=bg_color, fg=fg_color).pack(pady=5)

    listbox = tk.Listbox(root, width=50, height=20, bg=bg_color, fg=fg_color, selectbackground="#444444")
    listbox.pack(padx=10, pady=5)

    for host in hosts:
        listbox.insert(tk.END, host)

    btn = tk.Button(root, text="Connect", bg=btn_color, fg=fg_color, command=connect_ssh)
    btn.pack(pady=10)

    root.bind('<Return>', connect_ssh)
    root.mainloop()
