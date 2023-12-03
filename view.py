import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

class FigureCanvasTk:
    def __init__(self, figure, master=None, **kwargs):
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        self.canvas = FigureCanvasTkAgg(figure, master=master, **kwargs)
        self.widget = self.canvas.get_tk_widget()

    def draw(self):
        self.canvas.draw()

class FilePlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sound Analyzer")

        self.file_path = None
        self.plot_type = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # File Upload
        file_label = tk.Label(self.root, text="Select File:")
        file_label.grid(row=0, column=0, pady=10)

        file_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        file_button.grid(row=0, column=1, pady=10)

        # Radio Buttons
        radio_label = tk.Label(self.root, text="Select Plot Type:")
        radio_label.grid(row=1, column=0, pady=10)

        high_radio = tk.Radiobutton(self.root, text="High", variable=self.plot_type, value="high")
        high_radio.grid(row=1, column=1, pady=10)

        mid_radio = tk.Radiobutton(self.root, text="Mid", variable=self.plot_type, value="mid")
        mid_radio.grid(row=1, column=2, pady=10)

        low_radio = tk.Radiobutton(self.root, text="Low", variable=self.plot_type, value="low")
        low_radio.grid(row=1, column=3, pady=10)

        # Plot Button
        plot_button = tk.Button(self.root, text="Plot", command=self.plot)
        plot_button.grid(row=2, column=1, pady=10)

        # Plot Display Area
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTk(self.fig, master=self.root)
        self.canvas_widget = self.canvas.widget
        self.canvas_widget.grid(row=3, column=0, columnspan=4)

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

    def plot(self):
        if not self.file_path:
            tk.messagebox.showwarning("Warning", "Please select a file.")
            return

        plot_type = self.plot_type.get()
        if plot_type not in ["high", "mid", "low"]:
            tk.messagebox.showwarning("Warning", "Please select a plot type.")
            return

        self.plot_data()

    def plot_data(self):
        # Example: Read data from the selected file and plot it
        # For demonstration, let's assume the file contains x and y data.
        x, y = [1, 2, 3, 4, 5], [2, 4, 1, 6, 3]

        self.ax.clear()
        self.ax.plot(x, y, marker='o')

        self.ax.set_title("Plot")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = FilePlotterApp(root)
    root.mainloop()
