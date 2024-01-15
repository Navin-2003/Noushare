from tkinter import Tk, ttk

# Create a Tkinter window
window = Tk()
window.geometry("700x400")
window.configure(bg="#FFFFFF")

# Create a custom progress bar widget
class CustomProgressBar(ttk.Frame):
    def __init__(self, master, length, style="gray.Horizontal.TProgressbar"):
        super().__init__(master)
        
        self.style = ttk.Style()
        self.style.layout(style, [('custom.Horizontal.TProgressbar.trough', {'children': [('custom.Horizontal.TProgressbar.pbar', {'side': 'left', 'sticky': 'ns'})], 'sticky': 'ns'})])
        self.style.configure(style, troughcolor='gray', thickness=20)

        self.progress_bar = ttk.Progressbar(self, style=style, length=length, mode="determinate")
        self.progress_bar.pack(pady=5)

# Create a custom progress bar with gray color
progress_frame = CustomProgressBar(window, length=300)
progress_frame.pack(side="bottom", pady=10)

window.mainloop()
