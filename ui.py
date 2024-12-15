import tkinter as tk


class GameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Basic Form")
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.current_frame = None

    def set_fullscreen(self, fullscreen=True):
        if fullscreen:
            self.root.attributes("-fullscreen", True)
        else:
            self.root.attributes("-fullscreen", False)

    def center_window(self, width=640, height=480):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")

    def start(self):
        self.root.mainloop()
