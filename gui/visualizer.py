import tkinter as tk
from tkinter import Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from algorithms.bubble_sort import bubble_sort_visual
from algorithms.quick_sort import quick_sort_visual

class SortingVisualizer:
    def __init__(self, root, arr, algorithm):
        self.window = Toplevel(root)
        self.window.title(f"{algorithm} Visualization")
        self.window.geometry("600x400")

        self.arr = arr.copy()
        self.algorithm = algorithm

        # Matplotlib figure and axis
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.draw_array(self.arr, [])

        if algorithm == "Bubble Sort":
            bubble_sort_visual(self.arr, self.update_canvas)
        elif algorithm == "Quick Sort":
            quick_sort_visual(self.arr, 0, len(self.arr) - 1, self.update_canvas)
        
        self.draw_array(self.arr, [])

    def draw_array(self, arr, highlighted_indices):
        self.ax.clear()
        colors = ['blue' if i not in highlighted_indices else 'red' for i in range(len(arr))]
        self.ax.bar(range(len(arr)), arr, color=colors)
        self.canvas.draw()

    def update_canvas(self, arr, highlighted_indices):
        self.draw_array(arr, highlighted_indices)
        self.window.update_idletasks()
