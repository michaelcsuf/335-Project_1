import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def bubble_sort_anim(arr, capture_step):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                capture_step(arr)

def insertion_sort_anim(arr, capture_step):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            capture_step(arr)
        arr[j + 1] = key
        capture_step(arr)

def selection_sort_anim(arr, capture_step):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
        capture_step(arr)

def merge_sort_anim(arr, capture_step):
    def merge_sort_helper(arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            left = arr[:mid]
            right = arr[mid:]

            merge_sort_helper(left)
            merge_sort_helper(right)

            i = j = k = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                k += 1
                capture_step(arr)

            while i < len(left):
                arr[k] = left[i]
                i += 1
                k += 1
                capture_step(arr)

            while j < len(right):
                arr[k] = right[j]
                j += 1
                k += 1
                capture_step(arr)

    merge_sort_helper(arr)

def quick_sort_anim(arr, capture_step):
    def quick_sort_helper(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_helper(arr, low, pi - 1)
            quick_sort_helper(arr, pi + 1, high)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                capture_step(arr)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        capture_step(arr)
        return i + 1

    quick_sort_helper(arr, 0, len(arr) - 1)

def radix_sort_anim(arr, capture_step):
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp, capture_step)
        exp *= 10

def counting_sort(arr, exp, capture_step):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]
        capture_step(arr)

def linear_search_anim(arr, target, capture_step):
    found_index = -1
    for i in range(len(arr)):
        capture_step(i, arr[i] == target)  # Save step (index, is_match)
        if arr[i] == target:
            found_index = i
            break
    return found_index