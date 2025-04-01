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

            # Create a scrollable frame to hold the buttons
            self.host_buttons_frame = ctk.CTkScrollableFrame(self)
            self.host_buttons_frame.pack(fill="both", expand=True)

            # Create a button for each host
            for host in hosts:
                button = ctk.CTkButton(
                    self.host_buttons_frame, 
                    text=host, 
                    command=lambda h=host: connect_ssh(h),
                    anchor="w"  # Align text to the left
                )
                button.pack(padx=0, pady=2, fill="x")

    app = App()
    app.mainloop()