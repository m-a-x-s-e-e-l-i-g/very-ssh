import customtkinter as ctk
from tkinter import messagebox
import os
import sys
import subprocess

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def launch_gui(hosts, light_mode):
    def connect_ssh(host):
        if host:
            subprocess.Popen(['wt', 'ssh', host], shell=True)
        else:
            messagebox.showinfo("No selection", "Please select a valid host.")

    class App(ctk.CTk):
        IGNORED_KEYS = {"Shift_L", "Shift_R", "Control_L", "Control_R", 
                        "Alt_L", "Alt_R", "Caps_Lock", "Tab", 
                        "Left", "Right", "Up", "Down"}
        SELECTED_FG = "#14375e"
        DEFAULT_FG = "#1f538d"

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
            self.all_hosts = list(hosts)
            self.all_hosts_lower = [host.lower() for host in self.all_hosts]
            self.hosts = list(self.all_hosts)
            self.host_buttons = []
            self.visible_button_count = 0
            self.no_results_label = None
            self.no_results_visible = False
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
            visible_count = len(self.hosts)

            if self.no_results_label is None:
                self.no_results_label = ctk.CTkLabel(
                    self.host_buttons_frame,
                    text="No results found.",
                    anchor="center",
                    font=("Arial", 12, "italic")
                )

            if visible_count == 0:
                if self.visible_button_count:
                    for button in self.host_buttons[:self.visible_button_count]:
                        button.pack_forget()
                    self.visible_button_count = 0
                if not self.no_results_visible:
                    self.no_results_label.pack(pady=10)
                    self.no_results_visible = True
                self.selected_index = -1
                return

            if self.no_results_visible:
                self.no_results_label.pack_forget()
                self.no_results_visible = False

            while len(self.host_buttons) < visible_count:
                index = len(self.host_buttons)
                button = ctk.CTkButton(
                    self.host_buttons_frame,
                    text="",
                    command=lambda idx=index: self.connect_host_by_index(idx),
                    anchor="w"
                )
                button.bind("<Enter>", lambda event, idx=index: self.update_selected_index(idx))
                self.host_buttons.append(button)

            for index, host in enumerate(self.hosts):
                button = self.host_buttons[index]
                button.configure(text=host, fg_color=self.DEFAULT_FG)

            if self.visible_button_count < visible_count:
                for button in self.host_buttons[self.visible_button_count:visible_count]:
                    button.pack(padx=0, pady=2, fill="x")
            elif self.visible_button_count > visible_count:
                for button in self.host_buttons[visible_count:self.visible_button_count]:
                    button.pack_forget()

            self.visible_button_count = visible_count

            self.selected_index = -1
            self.update_selected_index(0)

        def connect_host_by_index(self, index):
            if 0 <= index < len(self.hosts):
                connect_ssh(self.hosts[index])

        def bind_events(self):
            self.bind("<Key>", self.global_search)
            self.bind("<Up>", self.move_cursor_up)
            self.bind("<Down>", self.move_cursor_down)
            self.bind("<Return>", self.open_selected_host)
            self.bind("<Escape>", self.close_application)

        def update_selected_index(self, index):
            previous_index = self.selected_index
            self.selected_index = index
            self.update_button_highlight(previous_index)
            self.update_button_highlight(self.selected_index)

        def update_button_highlight(self, index):
            if 0 <= index < len(self.hosts):
                self.host_buttons[index].configure(
                    fg_color=self.SELECTED_FG if index == self.selected_index else self.DEFAULT_FG
                )

        def move_cursor_up(self, event):
            if self.hosts:
                previous_index = self.selected_index
                self.selected_index = max(self.selected_index - 1, 0)
                self.update_button_highlight(previous_index)
                self.update_button_highlight(self.selected_index)

        def move_cursor_down(self, event):
            if self.hosts:
                previous_index = self.selected_index
                self.selected_index = min(self.selected_index + 1, len(self.hosts) - 1)
                self.update_button_highlight(previous_index)
                self.update_button_highlight(self.selected_index)

        def open_selected_host(self, event):
            if 0 <= self.selected_index < len(self.hosts):
                connect_ssh(self.hosts[self.selected_index])

        def filter_hosts(self):
            search_term = self.search_var.get().lower()
            if not search_term:
                self.hosts = self.all_hosts
            else:
                self.hosts = [
                    host for host, host_lower in zip(self.all_hosts, self.all_hosts_lower)
                    if search_term in host_lower
                ]
            self.create_host_buttons()

        def global_search(self, event):
            is_text_input = bool(event.char) and event.char.isprintable()
            if event.keysym not in self.IGNORED_KEYS and (is_text_input or event.keysym in ("BackSpace", "Delete")):
                current_text = self.search_var.get()
                if event.keysym == "BackSpace":
                    self.search_var.set(current_text[:-1])
                elif event.keysym == "Delete":
                    self.search_var.set("")
                else:
                    self.search_var.set(current_text + event.char)
                self.filter_hosts()

        def close_application(self, event):
            self.destroy()

    app = App()
    app.mainloop()