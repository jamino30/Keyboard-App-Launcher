import tkinter as tk
import os
from MacNativeApps import system_applications, utility_applications

"""

Provides functionality for application launch
Currently supports:
- Third-party applications
- macOS Native System Applications
- macOS Native Utility Applications

"""


class AppLauncher(tk.Frame):
    def __init__(self, master):
        """
        Initialize keyboard application launcher interface
        """
        tk.Frame.__init__(self, master)

        self.master = master

        master.bind("<Escape>", self.close)
        master.bind("<Button-1>", self.close)
        master.bind("<Return>", self.enter_pressed)
        master.bind("<Meta_L><Key>", self.open_app)

        self.var = tk.StringVar()
        self.display = tk.Entry(
            textvariable=self.var, width=27, font=("Circular Std", 32, "normal")
        )

        self.display.configure(
            highlightthickness=0,
            borderwidth=0,
            takefocus=1,
            foreground="white",
            background="black",
        )
        self.display.grid(row=0, columnspan=2, padx=8, pady=8)
        self.display.focus_force()

        self.apps = set(
            os.popen("find /Applications -maxdepth 1 -name *.app").read().split("\n")
        )
        self.apps.update(system_applications)
        self.apps.update(utility_applications)

        self.var.trace_id = self.var.trace("w", self.search_similar_display)
        self.used_labels = []
        self.matching_apps = []
        self.app_open_state = True

    def get_display_value(self):
        """
        Returns current display value
        """
        return self.var.get()

    def search_similar_display(self, *args):
        """
        Utilizes a serach algorithm to display similar results to display (user input) value
        """
        for label in self.used_labels:
            label.destroy()
        self.used_labels = []
        self.matching_apps = []

        if self.get_display_value() != "":
            for app in self.apps:
                name = os.path.split(app)[-1].split(".")[0]
                if name.lower().startswith(self.get_display_value().lower()):
                    self.matching_apps.append(name)

            if len(self.matching_apps) < 10:
                range_val = len(self.matching_apps)
            else:
                range_val = 10

            for i in range(range_val):
                label1 = tk.Label(text=str(self.matching_apps[i]))
                label1.configure(
                    font=("Circular Std", 18), foreground="white", background="black"
                )
                label1.grid(row=i + 1, column=0, sticky="w", padx=(8, 0), pady=(0, 10))
                self.used_labels.append(label1)

                label_val1 = tk.Label()
                if i == 0:
                    label_val1["text"] = "↩"
                else:
                    label_val1["text"] = f"⌘{i}"
                label_val1.configure(
                    font=("Circular Std", 16), foreground="#9b9b9b", background="black"
                )
                label_val1.grid(
                    row=i + 1, column=1, sticky="e", padx=(0, 8), pady=(0, 10)
                )
                self.used_labels.append(label_val1)

    def enter_pressed(self, event):
        """
        Determines <Enter> key action
        Action is either:
        - Open Application
        - Workflow Result
        """
        event.char = 0
        if self.app_open_state:
            self.open_app(event)
        else:
            self.app_action(event)

    def open_app(self, event):
        """
        Opens the selected application from file system
        """
        for app in self.apps:
            if (
                os.path.split(app)[-1].split(".")[0]
                == self.matching_apps[int(event.char)]
            ):
                path = os.path.join(
                    os.path.split(app)[0], "\ ".join(os.path.split(app)[-1].split(" "))
                )

                os.system("open " + path)

        # self.master.destroy()

    def close(self, event):
        """
        Closes application launcher/program when out of bounds click or <Escape> key
        """
        if (
            event.keysym == "Escape"
            or event.x < 0
            or event.x > 550
            or event.y < 0
            or event.y > 50
        ):
            self.master.destroy()
