import time

def quick_sort_visual(arr, low, high, update_canvas):
    if low < high:
        pi = partition(arr, low, high, update_canvas)
        quick_sort_visual(arr, low, pi - 1, update_canvas)
        quick_sort_visual(arr, pi + 1, high, update_canvas)

def partition(arr, low, high, update_canvas):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            update_canvas(arr, [i, j])
            time.sleep(0.1)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    update_canvas(arr, [i+1, high])
    time.sleep(0.1)
    return i + 1
