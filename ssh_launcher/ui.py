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
        if host:  # Ensure the host is valid
            os.system(f'start wt ssh {host}')
        else:
            messagebox.showinfo("No selection", "Please select a valid host.")

    class App(ctk.CTk):  # Use customtkinter's CTk as the base class
        def __init__(self):
            super().__init__()
            self.title("VerySSH")
            icon_path = resource_path("ssh_launcher/assets/icon.ico")
            self.iconbitmap(icon_path)
            self.geometry("250x300")  # Set a default window size
            self.minsize(250, 150)  # Set a minimum window size
            self.resizable(False, True)  # Disable horizontal resizing

            # Set the appearance mode (dark or light)
            ctk.set_appearance_mode("Dark" if not light_mode else "Light")
            ctk.set_default_color_theme("dark-blue")  # Optional: Set a color theme

            # Create a search bar
            self.search_var = ctk.StringVar()
            self.search_bar = ctk.CTkEntry(
                self, 
                textvariable=self.search_var
            )
            self.search_bar.pack(fill="x", padx=(6, 15), pady=(4, 0))
            self.search_bar.bind("<KeyRelease>", self.search)

            # Focus the search bar when the app starts
            self.search_bar.focus_set()

            # Create a scrollable frame to hold the buttons
            self.host_buttons_frame = ctk.CTkScrollableFrame(self)
            self.host_buttons_frame.pack(fill="both", expand=True, padx=0, pady=0)

            # Store the hosts and buttons
            self.hosts = hosts
            self.host_buttons = []

            # Create a button for each host
            self.create_host_buttons()

        def create_host_buttons(self):
            # Clear existing buttons
            for button in self.host_buttons:
                button.destroy()
            self.host_buttons.clear()

            # Add buttons for the current hosts
            for host in self.hosts:
                button = ctk.CTkButton(
                    self.host_buttons_frame, 
                    text=host, 
                    command=lambda h=host: connect_ssh(h),
                    anchor="w"  # Align text to the left
                )
                button.pack(padx=0, pady=2, fill="x")
                self.host_buttons.append(button)

        def filter_hosts(self, event):
            search_term = self.search_var.get().lower()
            filtered_hosts = [host for host in hosts if search_term in host.lower()]
            self.hosts = filtered_hosts
            self.create_host_buttons()

        def search(self, event):
            # Ignore non-character keys like arrow keys, Shift, etc.
            ignored_keys = {"Shift_L", "Shift_R", "Control_L", "Control_R", 
                            "Alt_L", "Alt_R", "Caps_Lock", "Tab", 
                            "Left", "Right", "Up", "Down"}
            if event.keysym not in ignored_keys and (event.char.isprintable() or event.keysym in ("BackSpace", "Delete")):
                self.filter_hosts(event)

    app = App()
    app.mainloop()