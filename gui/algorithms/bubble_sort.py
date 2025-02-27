import time

def bubble_sort_visual(arr, update_canvas):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                update_canvas(arr, [j, j+1])
                time.sleep(0.1)
    return arr
