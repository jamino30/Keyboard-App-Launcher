from AppLauncher import AppLauncher, tk

"""

Productivity workflows that are supported:
- control playback

Productivity workflows being developed:
- dictionaries
- file system navigation

"""

if __name__ == "__main__":
    """
    Initializes launcher
    """
    root = tk.Tk()

    root.overrideredirect(True)
    disp_width = 550
    disp_height = 50
    cen_width = int(root.winfo_screenwidth() / 2 - (disp_width / 2))
    cen_height = int(root.winfo_screenheight() / 4 - (disp_height / 2))
    root.geometry(f"+{cen_width}+{cen_height}")
    root.resizable(False, False)
    root.configure(background="black")
    root.attributes("-alpha", 0.9)

    AppLauncher(root)
    root.mainloop()
