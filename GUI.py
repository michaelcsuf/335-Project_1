import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

import time
import random

from SortAlgo import *

current_animation = None
is_paused = False
original_arrays = None
current_frame = 0

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
        global arrays, current_animation, original_arrays, is_paused
        if not arrays or len(arrays) == 0:
            messagebox.showerror("Input Error", "Please generate arrays first.")
            return

        # Store original arrays for reset functionality
        original_arrays = [arr.copy() for arr in arrays]
        
        # Reset pause state
        is_paused = False
        
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

        # Update function for sorting animation with red highlights
        def update_sorting(frame):
            global current_frame 
            current_frame = frame
            
            # Reset all bars to blue first
            for bar in bars:
                bar.set_color("blue")
            
            # Check which bars have changed since last frame
            if frame > 0:  # Not the first frame
                current_values = all_sorting_steps[0][frame]
                previous_values = all_sorting_steps[0][frame-1]
                
                # Find changed indices
                for i, (curr, prev) in enumerate(zip(current_values, previous_values)):
                    if curr != prev:
                        # This bar has changed - highlight it in red
                        bars[i].set_color("red")
            
            # Update heights of all bars
            for bar, height in zip(bars, all_sorting_steps[0][frame]):
                bar.set_height(height)
            
            # Update progress label
            progress_label.config(text=f"Step {frame+1}/{len(all_sorting_steps[0])}")
            # Enable reset button once animation starts
            reset_button.config(state="normal")

        # Update function for search animation
        def update_search(frame):
            global current_frame
            current_frame = frame
            index, is_match = all_sorting_steps[0][frame]
            for bar in bars:
                bar.set_color("blue")
            if is_match:
                bars[index].set_color("green")
            else:
                bars[index].set_color("red")

            progress_label.config(text=f"Step {frame+1}/{len(all_sorting_steps[0])}")
            # Enable reset button once animation starts
            reset_button.config(state="normal")
            
        # Create animation based on the selected algorithm
        if algorithm_name == "Linear Search":
            current_animation = FuncAnimation(fig, update_search, frames=len(all_sorting_steps[0]), interval=500, repeat=False)
        else:
            current_animation = FuncAnimation(fig, update_sorting, frames=len(all_sorting_steps[0]), interval=100, repeat=False)

        # Enable the control buttons
        pause_button.config(state="normal", text="Pause")
        reset_button.config(state="normal")
        
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

# Function to test performance analysis 
def analyze_performance():
    try:
        # Get test data parameters
        min_val = int(min_value_entry.get())
        max_val = int(max_value_entry.get())
        
        # Test sizes - small, medium, large
        test_sizes = [10, 100, 1000, 5000, 10000]
        
        # Separate results for sorting and searching
        sort_results = {alg: [] for alg in sorting_algorithms.keys() if alg != "Linear Search"}
        search_results = {"Linear Search (Best)": [], "Linear Search (Average)": [], "Linear Search (Worst)": []}
        
        # Run tests for each algorithm and size
        for size in test_sizes:
            # Generate test arrays used for all algorithms
            test_array = [random.randint(min_val, max_val) for _ in range(size)]
            
            # Test sorting algorithms
            for alg_name, sort_func in sorting_algorithms.items():
                if alg_name == "Linear Search":
                    continue
                    
                # Create a copy to avoid modifying the original
                array_copy = test_array.copy()
                
                # Start timing
                start_time = time.time()
                
                # Run the sort (without visualization to measure pure algorithm speed)
                def dummy_capture(arr):
                    pass  # Do nothing capture function to avoid visualization overhead
                    
                sort_func(array_copy, dummy_capture)
                
                # End timing
                end_time = time.time()
                runtime = end_time - start_time
                
                # Store results
                sort_results[alg_name].append(runtime)
            
            # Testing Linear Search - Best Case (first element)
            search_array = test_array.copy()
            target = search_array[0]  # First element (best case)
            
            start_time = time.time()
            def dummy_search_capture(index, is_match):
                pass
            linear_search(search_array, target, dummy_search_capture)
            end_time = time.time()
            search_results["Linear Search (Best)"].append(end_time - start_time)
            
            # Testing Linear Search - Average Case (middle element)
            middle_idx = len(search_array) // 2
            target = search_array[middle_idx] if middle_idx < len(search_array) else search_array[0]
            
            start_time = time.time()
            linear_search(search_array, target, dummy_search_capture)
            end_time = time.time()
            search_results["Linear Search (Average)"].append(end_time - start_time)
            
            # Testing Linear Search - Worst Case (element not in array)
            target = max_val + 1  # Value not in array
            
            start_time = time.time()
            linear_search(search_array, target, dummy_search_capture)
            end_time = time.time()
            search_results["Linear Search (Worst)"].append(end_time - start_time)
                
        # Display results in a new window
        display_performance_results(test_sizes, sort_results, search_results)
        
    except Exception as e:
        messagebox.showerror("Analysis Error", f"An error occurred during performance analysis: {e}")

# Function to display performance results
def display_performance_results(sizes, sort_results, search_results):
    # Create a new window for results
    perf_window = tk.Toplevel(root)
    perf_window.title("Algorithm Performance Analysis")
    perf_window.geometry("900x700")
    
    # Create a notebook with tabs
    notebook = ttk.Notebook(perf_window)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Runtime tab - Combined for both sorting and searching
    runtime_tab = ttk.Frame(notebook)
    notebook.add(runtime_tab, text="Runtime Analysis")
    
    # Create runtime chart
    runtime_fig, runtime_ax = plt.subplots(figsize=(8, 5))
    
    # Plot runtime for each sorting algorithm
    for alg_name, runtimes in sort_results.items():
        runtime_ax.plot(sizes, runtimes, marker='o', label=alg_name)
    
    # Include Linear Search data in the same chart
    for case_name, runtimes in search_results.items():
        runtime_ax.plot(sizes, runtimes, marker='s', label=case_name, linestyle='--')
    
    runtime_ax.set_xlabel('Array Size', fontweight='bold')
    runtime_ax.set_ylabel('Runtime (seconds)', fontweight='bold')
    runtime_ax.set_title('Algorithm Runtime Comparison', fontsize=14, fontweight='bold')
    runtime_ax.legend()
    runtime_ax.grid(True)
    
    # Log scale for better visibility of differences
    runtime_ax.set_xscale('log')
    runtime_ax.set_yscale('log')
    
    runtime_canvas = FigureCanvasTkAgg(runtime_fig, master=runtime_tab)
    runtime_canvas.get_tk_widget().pack(fill='both', expand=True)
    
    # Theoretical complexity tab
    complexity_tab = ttk.Frame(notebook)
    notebook.add(complexity_tab, text="Theoretical Complexity")
    
    # Create a table for theoretical complexities
    complexity_frame = ttk.Frame(complexity_tab)
    complexity_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Headers
    ttk.Label(complexity_frame, text="Algorithm", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=10, pady=5)
    ttk.Label(complexity_frame, text="Best Case", font=('Arial', 12, 'bold')).grid(row=0, column=1, padx=10, pady=5)
    ttk.Label(complexity_frame, text="Average Case", font=('Arial', 12, 'bold')).grid(row=0, column=2, padx=10, pady=5)
    ttk.Label(complexity_frame, text="Worst Case", font=('Arial', 12, 'bold')).grid(row=0, column=3, padx=10, pady=5)
    ttk.Label(complexity_frame, text="Space", font=('Arial', 12, 'bold')).grid(row=0, column=4, padx=10, pady=5)
    
    # Algorithm complexities
    complexities = {
        "Bubble Sort": ["O(n)", "O(n²)", "O(n²)", "O(1)"],
        "Insertion Sort": ["O(n)", "O(n²)", "O(n²)", "O(1)"],
        "Selection Sort": ["O(n²)", "O(n²)", "O(n²)", "O(1)"],
        "Merge Sort": ["O(n log n)", "O(n log n)", "O(n log n)", "O(n)"],
        "Quick Sort": ["O(n log n)", "O(n log n)", "O(n²)", "O(log n)"],
        "Radix Sort": ["O(nk)", "O(nk)", "O(nk)", "O(n+k)"],
        "Linear Search": ["O(1)", "O(n/2)", "O(n)", "O(1)"]
    }
    
    # Fill the table
    row = 1
    for alg_name, complexity in complexities.items():
        ttk.Label(complexity_frame, text=alg_name).grid(row=row, column=0, padx=10, pady=5)
        ttk.Label(complexity_frame, text=complexity[0]).grid(row=row, column=1, padx=10, pady=5)
        ttk.Label(complexity_frame, text=complexity[1]).grid(row=row, column=2, padx=10, pady=5)
        ttk.Label(complexity_frame, text=complexity[2]).grid(row=row, column=3, padx=10, pady=5)
        ttk.Label(complexity_frame, text=complexity[3]).grid(row=row, column=4, padx=10, pady=5)
        row += 1
   
# Bar graph for sorting algorithms 
def show_performance_bar_graph():
    try:
        # Get test data parameters
        min_val = int(min_value_entry.get())
        max_val = int(max_value_entry.get())
        
        # Use a single size for bar graph comparison
        size = 1000  # A moderate size to compare algorithms
        
        # Collect results for each algorithm
        results = {}
        
        # Generate test array used for all algorithms
        test_array = [random.randint(min_val, max_val) for _ in range(size)]
        
        # Test sorting algorithms
        for alg_name, sort_func in sorting_algorithms.items():
            if alg_name == "Linear Search":
                continue
                
            # Create a copy to avoid modifying the original
            array_copy = test_array.copy()
            
            # Run the algorithm multiple times to get a more stable measurement
            total_time = 0
            runs = 3
            
            for _ in range(runs):
                array_test = array_copy.copy()
                
                # Start timing
                start_time = time.time()
                
                # Run the sort without visualization
                def dummy_capture(arr):
                    pass
                
                sort_func(array_test, dummy_capture)
                
                # End timing
                end_time = time.time()
                total_time += (end_time - start_time)
            
            # Average runtime
            results[alg_name] = total_time / runs
        
        # Test Linear Search (average case)
        search_array = test_array.copy()
        middle_idx = len(search_array) // 2
        target = search_array[middle_idx]
        
        # Run search multiple times
        total_time = 0
        runs = 10  # More runs for search since it's faster
        
        for _ in range(runs):
            # Start timing
            start_time = time.time()
            
            def dummy_search_capture(index, is_match):
                pass
                
            linear_search(search_array, target, dummy_search_capture)
            
            # End timing
            end_time = time.time()
            total_time += (end_time - start_time)
        
        results["Linear Search"] = total_time / runs
        
        # Create a new window for the bar graph
        bar_window = tk.Toplevel(root)
        bar_window.title("Algorithm Performance Comparison")
        bar_window.geometry("800x600")
        
        # Create the figure and axis
        bar_fig, bar_ax = plt.subplots(figsize=(10, 6))
        
        # Create the bar chart
        algorithms = list(results.keys())
        runtimes = [results[alg] for alg in algorithms]
        
        # Sort algorithms by runtime for better visualization
        sorted_indices = sorted(range(len(runtimes)), key=lambda i: runtimes[i])
        algorithms = [algorithms[i] for i in sorted_indices]
        runtimes = [runtimes[i] for i in sorted_indices]
        
        # Use different colors for different algorithm types
        colors = []
        for alg in algorithms:
            if alg == "Linear Search":
                colors.append('green')
            elif "Sort" in alg and alg in ["Merge Sort", "Quick Sort", "Radix Sort"]:
                colors.append('orange')  # Efficient sorts
            else:
                colors.append('blue')    # Simple sorts
        
        # Create the bars
        bars = bar_ax.bar(algorithms, runtimes, color=colors)
        
        # Add data labels on top of bars
        for bar in bars:
            height = bar.get_height()
            bar_ax.text(bar.get_x() + bar.get_width()/2., height + 0.0001,
                        f'{height:.6f}s',
                        ha='center', va='bottom', rotation=45, fontsize=8)
        
        # Add labels and title
        bar_ax.set_xlabel('Algorithm', fontweight='bold')
        bar_ax.set_ylabel('Runtime (seconds)', fontweight='bold')
        bar_ax.set_title(f'Algorithm Runtime Comparison (Array Size = {size})', 
                         fontsize=14, fontweight='bold')
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        # Adjust layout
        plt.tight_layout()
        
        # Add the plot to the window
        canvas = FigureCanvasTkAgg(bar_fig, master=bar_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add a label explaining the colors
        explanation = ttk.Label(bar_window, 
                               text="Colors: Blue = Simple Sorts, Orange = Efficient Sorts, Green = Search",
                               font=('Arial', 10))
        explanation.pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Analysis Error", f"An error occurred generating bar graph: {e}")

# Function to toggle pause/resume of animation
def toggle_pause_resume():
    global is_paused, current_animation
    if current_animation:
        is_paused = not is_paused
        if is_paused:
            current_animation.event_source.stop()
            pause_button.config(text="Resume")
        else:
            current_animation.event_source.start()
            pause_button.config(text="Pause")

# Function to reset the visualization
def reset_visualization():
    global current_animation, arrays, original_arrays, current_frame, is_paused
    
    # Stop the current animation
    if current_animation:
        current_animation.event_source.stop()
    
    # Reset to original state
    if original_arrays:
        arrays = [arr.copy() for arr in original_arrays]
        
        # Redraw the initial state
        ax.clear()
        ax.bar(range(len(arrays[0])), arrays[0], color="blue")
        canvas.draw()
    
    # Reset controls
    current_frame = 0
    is_paused = False
    pause_button.config(text="Pause", state="disabled")
    reset_button.config(state="disabled")
    progress_label.config(text="Step 0/0")

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
array_display.pack(pady=5, padx=10)
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

# Control frame with buttons
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

# Execute button
execute_button = tk.Button(control_frame, text="Execute", command=animate_sorting, 
                          font=("Arial", 12, "bold"))
execute_button.grid(row=0, column=0, padx=5)

# Pause/Resume button
pause_button = tk.Button(control_frame, text="Pause", command=toggle_pause_resume, 
                        font=("Arial", 12, "bold"), 
                        state="disabled")
pause_button.grid(row=0, column=1, padx=5)

# Reset button
reset_button = tk.Button(control_frame, text="Reset", command=reset_visualization, 
                        font=("Arial", 12, "bold"), 
                        state="disabled")
reset_button.grid(row=0, column=2, padx=5)

# Progress label
progress_label = tk.Label(control_frame, text="Step 0/0", font=("Arial", 10))
progress_label.grid(row=0, column=3, padx=20)

# Button to analyze performance
performance_button = tk.Button(root, text="Analyze Algorithm", 
                              command=analyze_performance,
                              font=("Arial", 12))
performance_button.pack(pady=10)

# Button for bar graph visualization 
bar_button = tk.Button(root, text="Show Bar Graph", 
                       command=show_performance_bar_graph,
                       font=("Arial", 12))
bar_button.pack(pady=10)

# Sorting Visualization frame
frame_visual = tk.LabelFrame(root, text="Sorting Visualization of Array 1", padx=10, pady=10)
frame_visual.pack(pady=10, fill="both", expand=True, padx=20)

# Matplotlib figure and canvas for visualization
fig, ax = plt.subplots(figsize=(8, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_visual)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Start the Tkinter main loop
root.mainloop()
