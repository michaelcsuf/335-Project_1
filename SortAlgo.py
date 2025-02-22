


# Bubble Sort Algorithm
def bubble_sort(students):
    n = len(students)

    for i in range(n):
        for j in range(0, n - i - 1):
            if students[j][1] > students[j+1][1]:
                students[j], students[j+1] = students[j+1], students[j]

# Insertion Sort Algorithm
def insertion_sort(cards):
    for i in range(1, len(cards)):
        key = cards[i] # The card to be placed in the correct position
        j = i - 1 # Index of the last card in the sorted position
        
        # Move elements of the sorted portion
        while j >= 0 and key < cards[j]:
            cards[j + 1] = cards[j] # Shift the element to the right
            j -= 1 # Move one step to the left
        cards[j + 1] = key # Place key in its correct position

# Selection Sort Algorithm
def selection_sort(books):
    n = len(books)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if books[j][1] < books[min_index][1]:
                min_index = j
        books[i], books[min_index] = books[min_index], books[i]

def merge_sort(flights):
    if len(flights) > 1:
        mid = len(flights) // 2 # Find the middle index
        left_half = flights[:mid] # Divide list into two halves
        right_half = flights[mid:] 
        
        merge_sort(left_half)
        merge_sort(right_half)
        
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][1] < right_half[j][1]:
                flights[k] = left_half[i]
                i += 1
            else:
                flights[k] = right_half[j]
                j += 1
            k += 1
        
        while i < len(left_half):
            flights[k] = left_half[i]
            i += 1
            k += 1
        
        while j < len(right_half):
            flights[k] = right_half[j]
            j += 1
            k += 1

# Radix Sort
def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
# Count the occurrences of each digit in the current place value
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
# Update the count [i] so that it contains actual position in the output[]
    for i in range(1, 10):
        count[i] += count[i - 1] # Cumulative sum for stable sorting
# Build the output array by placing them in correct order
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1 # Decrement count to handle duplicates
# Copy sorted output back to the original array
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
# Least significant DIgit approach (LSD)
# Find the maximum number to determine the number of digits
    max_num = max(arr)
    exp = 1
# Continue sorting for each digit place value
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return arr