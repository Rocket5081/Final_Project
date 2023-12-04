from view import FilePlotterApp
from model import SoundAnalyzerModel

class SoundAnalyzerController:
    def __init__(self, app, model):
        self.app = app
        self.model = model

        # Bind functions to GUI events
        self.app.generate_button.config(command=self.plot_data)

    def plot_data(self):
        # Get data from the GUI
        file_path = self.app.file_path
        plot_type = self.app.plot_type.get()

        # Pass data to the model for processing
        self.model.process_data(file_path, plot_type)

if __name__ == "__main__":
    # Create instances of the model and view
    model = SoundAnalyzerModel()
    root = tk.Tk()
    app = FilePlotterApp(root)

    # Create an instance of the controller and pass the view and model
    controller = SoundAnalyzerController(app, model)

    # Run the Tkinter event loop
    root.mainloop()
