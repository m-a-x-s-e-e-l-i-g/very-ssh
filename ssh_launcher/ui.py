import customtkinter as ctk
from tkinter import messagebox
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def launch_gui(hosts, light_mode):
    def connect_ssh(host):
        if host:
            os.system(f'start wt ssh {host}')
        else:
            messagebox.showinfo("No selection", "Please select a valid host.")

    class App(ctk.CTk):
        IGNORED_KEYS = {"Shift_L", "Shift_R", "Control_L", "Control_R", 
                        "Alt_L", "Alt_R", "Caps_Lock", "Tab", 
                        "Left", "Right", "Up", "Down"}

        def __init__(self):
            super().__init__()
            self.configure_window(light_mode)
            self.initialize_variables(hosts)
            self.create_widgets()
            self.bind_events()

        def configure_window(self, light_mode):
            self.title("VerySSH")
            self.iconbitmap(resource_path("ssh_launcher/assets/icon.ico"))
            self.geometry("250x300")
            self.minsize(250, 150)
            self.resizable(False, True)
            ctk.set_appearance_mode("Dark" if not light_mode else "Light")
            ctk.set_default_color_theme("dark-blue")

        def initialize_variables(self, hosts):
            self.search_var = ctk.StringVar()
            self.hosts = hosts
            self.host_buttons = []
            self.selected_index = -1

        def create_widgets(self):
            self.create_search_bar()
            self.create_host_buttons_frame()
            self.create_host_buttons()

        def create_search_bar(self):
            self.search_bar = ctk.CTkEntry(self, textvariable=self.search_var)
            self.search_bar.pack(fill="x", padx=(6, 15), pady=(4, 0))
            self.search_bar.configure(state="disabled")

        def create_host_buttons_frame(self):
            self.host_buttons_frame = ctk.CTkScrollableFrame(self)
            self.host_buttons_frame.pack(fill="both", expand=True, padx=0, pady=0)

        def create_host_buttons(self):
            for button in self.host_buttons:
                button.destroy()
            self.host_buttons.clear()

            for index, host in enumerate(self.hosts):
                button = ctk.CTkButton(
                    self.host_buttons_frame, 
                    text=host, 
                    command=lambda h=host: connect_ssh(h),
                    anchor="w"
                )
                button.pack(padx=0, pady=2, fill="x")
                self.host_buttons.append(button)
                button.bind("<Enter>", lambda event, idx=index: self.update_selected_index(idx))

            self.update_selected_index(0)

        def bind_events(self):
            self.bind("<Key>", self.global_search)
            self.bind("<Up>", self.move_cursor_up)
            self.bind("<Down>", self.move_cursor_down)
            self.bind("<Return>", self.open_selected_host)
            self.bind("<Escape>", self.close_application)

        def update_selected_index(self, index):
            self.selected_index = index
            self.highlight_selected_button()

        def highlight_selected_button(self):
            for i, button in enumerate(self.host_buttons):
                button.configure(fg_color="#14375e" if i == self.selected_index else "#1f538d")

        def move_cursor_up(self, event):
            if self.host_buttons:
                self.selected_index = max(self.selected_index - 1, 0)
                self.highlight_selected_button()

        def move_cursor_down(self, event):
            if self.host_buttons:
                self.selected_index = min(self.selected_index + 1, len(self.host_buttons) - 1)
                self.highlight_selected_button()

        def open_selected_host(self, event):
            if 0 <= self.selected_index < len(self.host_buttons):
                connect_ssh(self.hosts[self.selected_index])

        def filter_hosts(self):
            search_term = self.search_var.get().lower()
            self.hosts = [host for host in hosts if search_term in host.lower()]
            self.create_host_buttons()

        def global_search(self, event):
            if event.keysym not in self.IGNORED_KEYS and (event.char.isprintable() or event.keysym in ("BackSpace", "Delete")):
                current_text = self.search_var.get()
                if event.keysym == "BackSpace":
                    self.search_var.set(current_text[:-1])
                elif event.keysym == "Delete":
                    self.search_var.set("")
                else:
                    self.search_var.set(current_text + event.char)
                self.filter_hosts()
                self.update_selected_index(0)

        def close_application(self, event):
            self.destroy()

    app = App()
    app.mainloop()