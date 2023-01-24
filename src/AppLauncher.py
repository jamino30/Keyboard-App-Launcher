import tkinter as tk
import os
from MacNativeApps import system_applications, utility_applications
import PlaybackControlActions as PCA
import Constants as CONST


class AppLauncher(tk.Frame):
    """Represents the design frame and functionality for
    a keyboard application launcher.

    Currently supports third-party applications, macOS native
    system and utility applications.
    """

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
            foreground=CONST.TEXT_COLOR,
            background=CONST.BG_COLOR,
        )
        self.display.grid(row=0, columnspan=2, padx=8, pady=8)
        self.display.focus_force()

        self.apps = set(self.get_applications("/Applications", 2, "app"))
        self.apps.update(
            system_applications,
            utility_applications,
        )

        self.var.trace_id = self.var.trace("w", self.search_similar_display)
        self.used_labels = []
        self.matching_apps = []
        self.app_open_state = True

    def get_applications(self, dir_name, max_depth, extension_type):
        """
        Get third-party applications located in /Applications directory
        """

        return (
            os.popen(f"find {dir_name} -maxdepth {max_depth} -name *.{extension_type}")
            .read()
            .split("\n")
        )

    @property
    def get_display_value(self):
        """
        Returns current display value
        """
        return self.var.get()

    def search_similar_display(self, *args):
        """
        Shows similar search results to display (user input) value
        """
        self.reset_search_similar_display()

        if self.get_display_value != "":
            for app in self.apps:
                name = os.path.split(app)[-1].split(".")[0]
                self.find_similar_apps_algo(name)

            for i in range(self.get_range_val()):
                self.create_app_search_result_label(i)

    def reset_search_similar_display(self):
        """
        Resets display search results
        """
        for label in self.used_labels:
            label.destroy()
        self.used_labels = []
        self.matching_apps = []

    def find_similar_apps_algo(self, name):
        """
        Finds all applications that are similar to user display input.
        Currently utilizes Algorithm v2.

        :param str name: application name (excluding directory path and extension)

        - Algorithm v1 => Determines if entire application/command name starts with display value
            if name.lower().startswith(self.get_display_value.lower()):
                self.matching_apps.append(name)

        - Algorithm v2 => Determines if any word in application/command name starts with display value
            if any(
                item.lower().startswith(self.get_display_value.lower())
                for item in name.split(" ")
            ):
                self.matching_apps.append(name)

        - Algorithm v3 => Incorporates Algorithm v2 and user application/command search data
            ... TBA ...
        """
        if any(
            item.lower().startswith(self.get_display_value.lower())
            for item in name.split(" ")
        ):
            self.matching_apps.append(name)

    def get_range_val(self):
        """
        Gets the number of applications to show in search results (maximum 10)
        """
        if len(self.matching_apps) < 10:
            range_val = len(self.matching_apps)
        else:
            range_val = 10

        return range_val

    def create_app_search_result_label(self, i):
        self.create_left_hand_label(i)
        self.create_right_hand_label(i)

    def create_left_hand_label(self, i):
        """
        Creates left hand label in search result for application name

        :param int i: row number in the search result display
        """
        label1 = tk.Label(text=str(self.matching_apps[i]))
        label1.configure(
            font=("Circular Std", 18),
            foreground=CONST.TEXT_COLOR,
            background=CONST.BG_COLOR,
        )
        label1.grid(row=i + 1, column=0, sticky="w", padx=(8, 0), pady=(0, 10))
        self.used_labels.append(label1)

    def create_right_hand_label(self, i):
        """
        Creates right hand label in search result for application launcher hotkey(s)

        :param int i: row number in the search result display
        """
        label_val1 = tk.Label()
        if i == 0:
            label_val1["text"] = "↩"
        else:
            label_val1["text"] = f"⌘{i}"
        label_val1.configure(
            font=("Circular Std", 16),
            foreground=CONST.SYMBOL_COLOR,
            background=CONST.BG_COLOR,
        )
        label_val1.grid(row=i + 1, column=1, sticky="e", padx=(0, 8), pady=(0, 10))
        self.used_labels.append(label_val1)

    def enter_pressed(self, event):
        """
        Determines <Enter> key action
        Action is either:
        - Open Application
        - Workflow Result

        :param Event event: the key bind event
        """
        event.char = 0
        if self.app_open_state:
            self.open_app(event)

    def open_app(self, event):
        """
        Opens the selected application from file system

        :param Event event: the key bind event
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

        @param event is the key bind event
        """
        if (
            event.keysym == "Escape"
            or event.x < 0
            or event.x > 550
            or event.y < 0
            or event.y > 50
        ):
            self.master.destroy()
