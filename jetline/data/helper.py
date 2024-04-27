import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os


def choose_file():
    """
    This method opens a file dialog window to allow the user to choose a file on their system. It returns the path of the selected file.
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

