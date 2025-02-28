import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ast  # For safe evaluation of string to list
from sorting_algorithms import *  # Import sorting functions
from animations import *  # Import animation functions
import time  # Import time module

# Initialize Tkinter
root = tk.Tk()
root.title("Sorting Algorithm Analyzer")
root.geometry("900x700")

# UI COMPONENTS

# Unsorted data selection
frame_data = tk.LabelFrame(root, text="Unsorted Data", padx=10, pady=10)
frame_data.pack(pady=10, fill="x", padx=20)

array_display = tk.Entry(frame_data, width=60)
array_display.pack(pady=5, padx=10)

# Randomizer settings
frame_randomizer = tk.LabelFrame(root, text="Randomizer Settings", padx=10, pady=10)
frame_randomizer.pack(pady=10, fill="x", padx=20)

tk.Label(frame_randomizer, text="Min Value").pack(side="left")
min_value_entry = tk.Entry(frame_randomizer, width=5)
min_value_entry.pack(side="left", padx=5)
min_value_entry.insert(0, "0")

tk.Label(frame_randomizer, text="Max Value").pack(side="left")
max_value_entry = tk.Entry(frame_randomizer, width=5)
max_value_entry.pack(side="left", padx=5)
max_value_entry.insert(0, "100")

tk.Label(frame_randomizer, text="Num Elements").pack(side="left")
num_elements_entry = tk.Entry(frame_randomizer, width=5)
num_elements_entry.pack(side="left", padx=5)
num_elements_entry.insert(0, "30")

# Generate a random list
def generate_list():
    try:
        min_val = int(min_value_entry.get())
        max_val = int(max_value_entry.get())
        num_elements = int(num_elements_entry.get())
        if min_val >= max_val or num_elements <= 0:
            raise ValueError("Invalid input range!")
        random_list = [random.randint(min_val, max_val) for _ in range(num_elements)]
        array_display.delete(0, tk.END)
        array_display.insert(0, str(random_list))
        # Display the unsorted array visually
        ax.clear()
        ax.bar(range(len(random_list)), random_list, color="blue")
        canvas.draw()
    except ValueError as e:
        messagebox.showerror("Input Error", f"Please enter valid numbers!\n{e}")

tk.Button(frame_randomizer, text="Auto-Generate List", command=generate_list).pack(pady=5)

# Sorting Algorithm Selection
frame_algorithms = tk.LabelFrame(root, text="Choose Sorting Algorithm", padx=10, pady=10)
frame_algorithms.pack(pady=10, fill="x", padx=20)

sorting_algorithms = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Radix Sort": radix_sort
}

selected_algorithm = tk.StringVar(value="Bubble Sort")
for alg in sorting_algorithms.keys():
    ttk.Radiobutton(frame_algorithms, text=alg, variable=selected_algorithm, value=alg).pack(side="left", padx=5)

# Add a search entry and button
frame_search = tk.LabelFrame(root, text="Linear Search", padx=10, pady=10)
frame_search.pack(pady=10, fill="x", padx=20)

tk.Label(frame_search, text="Search Value").pack(side="left")
search_entry = tk.Entry(frame_search, width=10)
search_entry.pack(side="left", padx=5)

# Linear Search Functionality
def linear_search_visualization():
    try:
        array_str = array_display.get()
        array = ast.literal_eval(array_str)  # Safely convert string to list
        if not isinstance(array, list):
            raise ValueError("Invalid list format!")

        search_value = int(search_entry.get())  # Get the value to search for

        # Store search steps for visualization
        search_steps = []

        def capture_step(index, is_match):
            search_steps.append((index, is_match))  # Save step (index, is_match)

        # Perform Linear Search
        found_index = linear_search_anim(array, search_value, capture_step)

        # Set up the bar chart
        ax.clear()
        bars = ax.bar(range(len(array)), array, color="blue")

        def update(frame):
            index, is_match = search_steps[frame]
            for bar, height in zip(bars, array):
                bar.set_color("blue")  # Reset color
            if is_match:
                bars[index].set_color("green")  # Highlight match
            else:
                bars[index].set_color("red")  # Highlight current element

        anim = FuncAnimation(fig, update, frames=len(search_steps), interval=500, repeat=False)
        canvas.draw()

        if found_index != -1:
            messagebox.showinfo("Search Result", f"Value {search_value} found at index {found_index}.")
        else:
            messagebox.showinfo("Search Result", f"Value {search_value} not found.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
tk.Button(frame_search, text="Run Linear Search", command=linear_search_visualization).pack(side="left", padx=5)

def animate_sorting():
    try:
        array_str = array_display.get()
        array = ast.literal_eval(array_str)  # Safely convert string to list
        if not isinstance(array, list):
            raise ValueError("Invalid list format!")

        algorithm_name = selected_algorithm.get()
        sorting_function = sorting_algorithms[algorithm_name]

        # Store sorting steps for animation
        sorting_steps = []

        def capture_step(arr):
            sorting_steps.append(list(arr))  # Save the current state

        # Capture the initial state of the array
        capture_step(array)

        # Measure the time taken by the sorting algorithm
        start_time = time.time()
        
        # Call the corresponding animation function
        sorting_map = {
            "Bubble Sort": bubble_sort_anim,
            "Insertion Sort": insertion_sort_anim,
            "Selection Sort": selection_sort_anim,
            "Merge Sort": merge_sort_anim,
            "Quick Sort": quick_sort_anim,
            "Radix Sort": radix_sort_anim
        }

        if algorithm_name in sorting_map:
            sorting_map[algorithm_name](array, capture_step)
        else:
            messagebox.showerror("Sorting Error", "Animation not available for this algorithm.")
            return

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Set up the bar chart
        ax.clear()
        bars = ax.bar(range(len(array)), array, color="blue")

        def update(frame):
            for bar, height in zip(bars, sorting_steps[frame]):
                bar.set_height(height)

        anim = FuncAnimation(fig, update, frames=len(sorting_steps), interval=100, repeat=False)
        canvas.draw()

        # Display the time complexity
        messagebox.showinfo("Time Complexity", f"Time taken by {algorithm_name}: {elapsed_time:.4f} seconds")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Run sorting button
tk.Button(root, text="Run Animation", command=animate_sorting, font=("Arial", 12, "bold")).pack(pady=20)

# Sorting Visualization Frame
frame_visual = tk.LabelFrame(root, text="Sorting Visualization", padx=10, pady=10)
frame_visual.pack(pady=10, fill="both", expand=True, padx=20)

fig, ax = plt.subplots(figsize=(8, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_visual)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Animation Function

# Run Tkinter main loop
root.mainloop()
