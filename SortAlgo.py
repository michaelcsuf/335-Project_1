# Bubble Sort Algorithm
def bubble_sort(arr, capture_step=None):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                if capture_step:
                    capture_step(arr)

# Linear Search Algorithm
def linear_search(arr, target, capture_step):
    found_indices = []
    for index, value in enumerate(arr):
        is_match = (value == target)
        capture_step(index, is_match)
        if is_match:
            found_indices.append(index)
    if not found_indices:
        found_indices.append(-1)
    return found_indices

# Insertion Sort Algorithm
def insertion_sort(cards, capture_step=None):
    for i in range(1, len(cards)):
        key = cards[i]  # The card to be placed in the correct position
        j = i - 1  # Index of the last card in the sorted position
        
        # Move elements of the sorted portion
        while j >= 0 and key < cards[j]:
            cards[j + 1] = cards[j]  # Shift the element to the right
            j -= 1  # Move one step to the left
            if capture_step:
                capture_step(cards)
        cards[j + 1] = key  # Place key in its correct position
        if capture_step:
            capture_step(cards)

# Selection Sort Algorithm
def selection_sort(arr, capture_step=None):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
        if capture_step:
            capture_step(arr)

# Merge Sort Algorithm
def merge_sort(arr, capture_step=None):
    if len(arr) > 1:
        mid = len(arr) // 2  # Find the middle index
        left_half = arr[:mid]  # Divide list into two halves
        right_half = arr[mid:]
        
        merge_sort(left_half, capture_step)
        merge_sort(right_half, capture_step)
        
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
            if capture_step:
                capture_step(arr)
        
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
            if capture_step:
                capture_step(arr)
        
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
            if capture_step:
                capture_step(arr)

# Radix Sort
def counting_sort(arr, exp, capture_step=None):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    # Count the occurrences of each digit in the current place value
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    # Update the count [i] so that it contains actual position in the output[]
    for i in range(1, 10):
        count[i] += count[i - 1]  # Cumulative sum for stable sorting
    # Build the output array by placing them in correct order
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1  # Decrement count to handle duplicates
    # Copy sorted output back to the original array
    for i in range(n):
        arr[i] = output[i]
        if capture_step:
            capture_step(arr)
def radix_sort(arr, capture_step=None):
    # Least significant Digit approach (LSD)
    # Find the maximum number to determine the number of digits
    max_num = max(arr)
    exp = 1
    # Continue sorting for each digit place value
    while max_num // exp > 0:
        counting_sort(arr, exp, capture_step)
        exp *= 10

# Quick Sort
def quick_sort(arr, capture_step=None):
    if len(arr) <= 1:  # Base case
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    sorted_arr = quick_sort(left, capture_step) + middle + quick_sort(right, capture_step)
    if capture_step:
        capture_step(sorted_arr)
    return sorted_arr
