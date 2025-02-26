import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from SortAlgo import *  # Import sorting functions

# INSTALLATION REQUIREMENTS:
# 1: I needed a env for it to run idk about you so fyi
# 2; we need numpy and matplotlib so here is the install
#    pip install matplotlib numpy
# 3: Tkinter
#    sudo apt install python3-tk  (Linux)
#    brew install python-tk       (Mac)


root = tk.Tk()
root.title( "Sorting Algorithm Analyzer")
root.geometry("900x700")

# UI COMPONENTS 

# Unsorted data selec
frame_data = tk.LabelFrame(root, text="Unsorted Data", padx=10, pady=10)
frame_data.pack(pady=10, fill="x", padx=20)

array_display = tk.Entry(frame_data, width=60)
array_display.pack(pady=5, padx=10)

# randomizer settingss

frame_randomizer = tk.LabelFrame(root,  text="Randomizer Settings", padx=10, pady=10)
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

# gen a random List
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

# Sorting Visualization Frame
frame_visual = tk.LabelFrame(root, text="Sorting Visualization", padx=10, pady=10)
frame_visual.pack(pady=10, fill="both", expand=True, padx=20)

fig, ax = plt.subplots(figsize=(8, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_visual)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Animation Function
def animate_sorting():
    try:
        array_str = array_display.get() 
        array = eval(array_str)  # Convert string to list (Make sure input is safe)
        if not isinstance(array, list):
            raise ValueError("Invalid list format!")

        algorithm_name = selected_algorithm.get()
        sorting_function = sorting_algorithms[algorithm_name]

        # Store sorting steps for animation
        sorting_steps = []
        
        def capture_step(arr):
            sorting_steps.append(list(arr))  # Save the current state

        # Modified sorting functions to capture each step
        def bubble_sort_anim(arr ):
            n = len(arr)
            for i in range(n):
                for j in range(n - i-1):
                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j +1] = arr[ j + 1], arr[j]
                        capture_step(arr)

        def insertion_sort_anim(arr):
            for i in range(1, len(arr)):
                key = arr[i]
                j = i - 1
                while j >= 0 and key < arr[j]:
                    arr[j + 1] = arr[j]
                    j -= 1
                    capture_step(arr)
                arr[j + 1] = key
                capture_step(arr)

        def selection_sort_anim(arr):
            n = len(arr)
            for i in range( n):
                min_index = i
                for j in range(i + 1, n ):
                    if arr[j] < arr[min_index]:
                        min_index = j
                arr[i], arr[min_index] = arr[min_index], arr[i]
                capture_step(arr)

        # Call the corresponding animation function
        sorting_map = {
            "Bubble Sort": bubble_sort_anim,
            "Insertion Sort": insertion_sort_anim,
            "Selection Sort": selection_sort_anim
        }

        if algorithm_name in sorting_map:
            sorting_map[algorithm_name](array )
        else:
            messagebox.showerror( "Sorting Error", "Animation not available for this algorithm.")
            return

        # Set up the bar chart
        ax.clear()
        bars = ax.bar(range(len(array) ), array, color="blue")

        def update(frame):
            for bar, height in zip(bars, sorting_steps[frame]):
                bar.set_height(height)

        anim = FuncAnimation(fig, update, frames=len(sorting_steps), interval=100, repeat=False)
        canvas.draw()
    
    except Exception as e: 
        messagebox.showerror("Error", f"An error occurred: {e}")

# run a sorting button
tk.Button(root, text="Run Animation", command=animate_sorting, font=("Arial", 12, "bold")).pack(pady=20)

# Run tkinter on the main loop
root.mainloop()
