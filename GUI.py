import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

import time
import random

from SortAlgo import *

# Function to generate a random list of arrays
def generate_list():
    global arrays
    try:
        # Get input values from the user
        min_val = int(min_value_entry.get())
        max_val = int(max_value_entry.get())
        num_elements = int(num_elements_entry.get())
        num_arrays = int(num_arrays_entry.get())
        
        # Validate input values
        if min_val >= max_val or num_elements <= 0 or num_arrays <= 0:
            raise ValueError("Invalid input range!")
        
        # Generate random arrays
        arrays = []
        for _ in range(num_arrays):
            random_list = [random.randint(min_val, max_val) for _ in range(num_elements)]
            arrays.append(random_list)
        
        # Display the first array
        array_display.delete(0, tk.END)
        array_display.insert(0, str(arrays[0]))

        # Display all arrays
        all_arrays_display.delete("1.0", tk.END)
        for i, arr in enumerate(arrays):
            all_arrays_display.insert(tk.END, f"Array {i+1}: {arr}\n")

        # Plot the first array
        ax.clear()
        ax.bar(range(len(arrays[0])), arrays[0], color="blue")
        canvas.draw()
    except ValueError as e:
        messagebox.showerror("Input Error", f"Please enter valid numbers!\n{e}")

# Function to animate the sorting process
def animate_sorting():
    try:
        global arrays
        if not arrays or len(arrays) == 0:
            messagebox.showerror("Input Error", "Please generate arrays first.")
            return

        # Get the selected algorithm
        algorithm_name = selected_algorithm.get()
        sorting_function = sorting_algorithms[algorithm_name]

        total_time = 0
        all_sorting_steps = []
        search_results = []

        # Perform sorting or searching on each array
        for array in arrays:
            array_copy = array.copy()
            sorting_steps = []

            def capture_step(arr):
                sorting_steps.append(list(arr))

            def capture_search_step(index, is_match):
                print(f"Captured step: index={index}, is_match={is_match}")
                sorting_steps.append((index, is_match))

            capture_step(array_copy)
            start_time = time.time()
            
            if algorithm_name == "Linear Search":
                search_value = search_entry.get()
                if not search_value:
                    messagebox.showerror("Input Error", "Please enter a value to search for.")
                    return
                found_indices = sorting_function(array_copy, int(search_value), capture_search_step)
                search_results.append(found_indices)
            else:
                sorting_function(array_copy, capture_step)

            end_time = time.time()
            elapsed_time = end_time - start_time
            total_time += elapsed_time

            all_sorting_steps.append(sorting_steps)

        # Plot the first array
        ax.clear()
        bars = ax.bar(range(len(arrays[0])), arrays[0], color="blue")

        # Update function for sorting animation
        def update_sorting(frame):
            for bar, height in zip(bars, all_sorting_steps[0][frame]):
                bar.set_height(height)

        # Update function for search animation
        def update_search(frame):
            print(f"Updating search: frame={frame}, data={all_sorting_steps[0][frame]}")
            index, is_match = all_sorting_steps[0][frame]
            for bar in bars:
                bar.set_color("blue")
            if is_match:
                bars[index].set_color("green")
            else:
                bars[index].set_color("red")

        # Create animation based on the selected algorithm
        if algorithm_name == "Linear Search":
            anim = FuncAnimation(fig, update_search, frames=len(all_sorting_steps[0]), interval=500, repeat=False)
        else:
            anim = FuncAnimation(fig, update_sorting, frames=len(all_sorting_steps[0]), interval=100, repeat=False)

        canvas.draw()

        # Display search results if Linear Search was used
        if algorithm_name == "Linear Search":
            result_message = ""
            for i, indices in enumerate(search_results):
                if indices and indices[0] != -1:
                    result_message += f"Array {i+1}: Found at index(s) {indices}.\n"
                else:
                    result_message += f"Array {i+1}: Value not found\n"
            messagebox.showinfo("Search Results", result_message)
        
        # Display total time taken for sorting
        messagebox.showinfo("Time Complexity", f"Total time taken by {algorithm_name} for all arrays: {total_time:.4f} seconds")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to handle window closing
def on_closing():
    root.quit()
    root.destroy()

# Initialize Tkinter
root = tk.Tk()
root.title("Sorting Algorithm Analyzer")
root.geometry("750x900")

root.protocol("WM_DELETE_WINDOW", on_closing)

# UI COMPONENTS

# Randomizer settings frame
frame_randomizer = tk.LabelFrame(root, text="Randomizer Settings", padx=10, pady=10)
frame_randomizer.pack(pady=10, fill="x", padx=20)

# Min value input
tk.Label(frame_randomizer, text="Min Value").pack(side="left")
min_value_entry = tk.Entry(frame_randomizer, width=5)
min_value_entry.pack(side="left", padx=5)
min_value_entry.insert(0, "0")

# Max value input
tk.Label(frame_randomizer, text="Max Value").pack(side="left")
max_value_entry = tk.Entry(frame_randomizer, width=5)
max_value_entry.pack(side="left", padx=5)
max_value_entry.insert(0, "100")

# Number of elements input
tk.Label(frame_randomizer, text="Num Elements").pack(side="left")
num_elements_entry = tk.Entry(frame_randomizer, width=5)
num_elements_entry.pack(side="left", padx=5)
num_elements_entry.insert(0, "30")

# Number of arrays input
tk.Label(frame_randomizer, text="Num Arrays").pack(side="left")
num_arrays_entry = tk.Entry(frame_randomizer, width=5)
num_arrays_entry.pack(side="left", padx=5)
num_arrays_entry.insert(0, "1")

# Button to generate random list
tk.Button(frame_randomizer, text="Auto-Generate List", command=generate_list).pack(pady=5)

# Unsorted data selection frame
frame_data = tk.LabelFrame(root, text="Unsorted Data", padx=10, pady=10)
frame_data.pack(pady=10, fill="x", padx=20)
array_display = tk.Entry(frame_data, width=60)
all_arrays_display = tk.Text(frame_data, height=10, width=60)
all_arrays_display.pack(pady=5, padx=10)

# Sorting Algorithm Selection frame
frame_algorithms = tk.LabelFrame(root, text="Choose Sorting Algorithm", padx=10, pady=10)
frame_algorithms.pack(pady=10, fill="x", padx=20)

# Dictionary of sorting algorithms
sorting_algorithms = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Radix Sort": radix_sort,
    "Linear Search": linear_search
}

# Radio buttons for selecting sorting algorithm
selected_algorithm = tk.StringVar(value="Bubble Sort")
for alg in sorting_algorithms.keys():
    ttk.Radiobutton(frame_algorithms, text=alg, variable=selected_algorithm, value=alg).pack(side="left", padx=5)

# Search entry and button for Linear Search
frame_search = tk.LabelFrame(root, text="For Linear Search into Array 1", padx=10, pady=10)
frame_search.pack(pady=10, fill="x", padx=20)

tk.Label(frame_search, text="Search Value").pack(side="left")
search_entry = tk.Entry(frame_search, width=10)
search_entry.pack(side="left", padx=5)

# Button to execute the selected algorithm
tk.Button(root, text="Execute Algorithm", command=animate_sorting, font=("Arial", 12, "bold")).pack(pady=20)

# Sorting Visualization frame
frame_visual = tk.LabelFrame(root, text="Sorting Visualization of Array 1", padx=10, pady=10)
frame_visual.pack(pady=10, fill="both", expand=True, padx=20)

# Matplotlib figure and canvas for visualization
fig, ax = plt.subplots(figsize=(8, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_visual)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Start the Tkinter main loop
root.mainloop()
