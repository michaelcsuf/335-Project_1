import tkinter as tk
from tkinter import messagebox
import random
import time

from visualizer import SortingVisualizer

def generate_random_array():
    try:
        min_val = int(min_entry.get())
        max_val = int(max_entry.get())
        num_elements = int(num_entry.get())

        if num_elements <= 0 or min_val >= max_val:
            messagebox.showerror("Error", "Invalid range or number of elements")
            return

        global arr
        arr = [random.randint(min_val, max_val) for _ in range(num_elements)]
        array_display.config(text="Array: " + str(arr))
    
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

def generate_random_multiple_arrays():
    try:
        num_arrays = int(num_arrays_entry.get())
        global arr
        arr = []

        for _ in range(num_arrays):
            num_elements = int(num_entry.get())  # Use same size for all arrays
            arr.append([random.randint(int(min_entry.get()), int(max_entry.get())) for _ in range(num_elements)])

        array_display.config(text="Arrays: " + str(arr))
    
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

def analyze_runtime():
    if not arr:
        messagebox.showerror("Error", "No array generated yet!")
        return

    arr_copy = arr.copy()
    start_time = time.time()

    if sort_var.get() == "Bubble Sort":
        from algorithms.bubble_sort import bubble_sort
        bubble_sort(arr_copy)
    elif sort_var.get() == "Quick Sort":
        from algorithms.quick_sort import quick_sort
        quick_sort(arr_copy)
    elif sort_var.get() == "Merge Sort":
        from algorithms.merge_sort import merge_sort
        merge_sort(arr_copy)
    elif sort_var.get() == "Radix Sort":
        from algorithms.radix_sort import radix_sort
        radix_sort(arr_copy)

    end_time = time.time()
    time_taken = end_time - start_time

    messagebox.showinfo("Runtime Analysis", f"Sorting Algorithm: {sort_var.get()}\nTime Taken: {time_taken:.6f} seconds")

def visualize_sorting():
    if not arr:
        messagebox.showerror("Error", "No array generated yet!")
        return
    SortingVisualizer(root, arr, sort_var.get())

# Main GUI Window
root = tk.Tk()
root.title("Sorting Algorithm Analyzer Tool")
root.geometry("600x600")

arr = []

tk.Label(root, text="Unsorted Data", font=("Arial", 12, "bold")).pack()

# Single vs Multiple Array Selection
array_type = tk.StringVar(value="single")
tk.Radiobutton(root, text="Single Array", variable=array_type, value="single").pack()
tk.Radiobutton(root, text="Multiple Arrays", variable=array_type, value="multiple").pack()

# Randomizer Settings
tk.Label(root, text="Min Value").pack()
min_entry = tk.Entry(root)
min_entry.pack()

tk.Label(root, text="Max Value").pack()
max_entry = tk.Entry(root)
max_entry.pack()

tk.Label(root, text="Number of Elements").pack()
num_entry = tk.Entry(root)
num_entry.pack()

tk.Label(root, text="Number of Arrays (for Multiple Array Mode)").pack()
num_arrays_entry = tk.Entry(root)
num_arrays_entry.pack()

# Generate Buttons
tk.Button(root, text="Generate Single Array", command=generate_random_array).pack()
tk.Button(root, text="Generate Multiple Arrays", command=generate_random_multiple_arrays).pack()

array_display = tk.Label(root, text="Array(s) will appear here", wraplength=500)
array_display.pack()

# Sorting Algorithm Selection
tk.Label(root, text="Select Sorting Algorithm").pack()
sort_options = ["Bubble Sort", "Quick Sort", "Merge Sort", "Radix Sort"]
sort_var = tk.StringVar()
sort_var.set(sort_options[0])
sort_menu = tk.OptionMenu(root, sort_var, *sort_options)
sort_menu.pack()

# Buttons to Analyze and Visualize
tk.Button(root, text="Run Runtime Analysis", command=analyze_runtime).pack()
tk.Button(root, text="Visualize Sorting", command=visualize_sorting).pack()

root.mainloop()
