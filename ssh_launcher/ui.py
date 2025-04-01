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
            self.search_bar.bind("<KeyRelease>", self.global_search)
            self.search_bar.configure(state="disabled")

            # Disable the search bar so it cannot be clicked or focused
            self.search_bar.configure(state="disabled")

            # Bind key events to the root window for global search functionality
            self.bind("<Key>", self.global_search)
            # Bind arrow keys and Enter for navigation and selection
            self.bind("<Up>", self.move_cursor_up)
            self.bind("<Down>", self.move_cursor_down)
            self.bind("<Return>", self.open_selected_host)
            # Bind the Escape key to close the application
            self.bind("<Escape>", self.close_application)


            # Create a scrollable frame to hold the buttons
            self.host_buttons_frame = ctk.CTkScrollableFrame(self)
            self.host_buttons_frame.pack(fill="both", expand=True, padx=0, pady=0)

            # Store the hosts and buttons
            self.hosts = hosts
            self.host_buttons = []
            self.selected_index = -1  # Track the currently selected host

            # Create a button for each host
            self.create_host_buttons()

        def create_host_buttons(self):
            # Clear existing buttons
            for button in self.host_buttons:
                button.destroy()
            self.host_buttons.clear()

            # Add buttons for the current hosts
            for index, host in enumerate(self.hosts):
                button = ctk.CTkButton(
                    self.host_buttons_frame, 
                    text=host, 
                    command=lambda h=host: connect_ssh(h),
                    anchor="w"  # Align text to the left
                )
                button.pack(padx=0, pady=2, fill="x")
                self.host_buttons.append(button)

                # Bind mouse hover event to update selected_index
                button.bind("<Enter>", lambda event, idx=index: self.update_selected_index(idx))

            # Reset selection index if hosts are updated
            self.update_selected_index(0)

        def update_selected_index(self, index):
            self.selected_index = index
            self.highlight_selected_button()

        def highlight_selected_button(self):
            # Highlight the currently selected button
            for i, button in enumerate(self.host_buttons):
                if i == self.selected_index:
                    button.configure(fg_color="#14375e")  # Highlight color
                else:
                    button.configure(fg_color="#1f538d")  # Default color

        def move_cursor_up(self, event):
            if self.host_buttons:
                self.selected_index = max(self.selected_index - 1, 0)  # Ensure it doesn't go below 0
                self.highlight_selected_button()

        def move_cursor_down(self, event):
            if self.host_buttons:
                self.selected_index = min(self.selected_index + 1, len(self.host_buttons) - 1)  # Ensure it doesn't exceed the last index
                self.highlight_selected_button()

        def open_selected_host(self, event):
            if 0 <= self.selected_index < len(self.host_buttons):
                selected_host = self.hosts[self.selected_index]
                connect_ssh(selected_host)

        def filter_hosts(self, event):
            search_term = self.search_var.get().lower()
            filtered_hosts = [host for host in hosts if search_term in host.lower()]
            self.hosts = filtered_hosts
            self.create_host_buttons()

        def global_search(self, event):
            # Ignore non-character keys like arrow keys, Shift, etc.
            ignored_keys = {"Shift_L", "Shift_R", "Control_L", "Control_R", 
                            "Alt_L", "Alt_R", "Caps_Lock", "Tab", 
                            "Left", "Right", "Up", "Down"}
            if event.keysym not in ignored_keys and (event.char.isprintable() or event.keysym in ("BackSpace", "Delete")):
            # Update the search bar's text variable with the keypress
                current_text = self.search_var.get()
                if event.keysym == "BackSpace":
                    self.search_var.set(current_text[:-1])  # Remove last character
                elif event.keysym == "Delete":
                    self.search_var.set("")  # Clear the search bar
                else:
                    self.search_var.set(current_text + event.char)
                self.filter_hosts(event)
                self.update_selected_index(0)

        def close_application(self, event):
            self.destroy()

    app = App()
    app.mainloop()