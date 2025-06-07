import heapq
import time
import re

def heap_sort(arr):
    heapq.heapify(arr)  # Convert the list into a heap
    sorted_arr = [heapq.heappop(arr) for _ in range(len(arr))]  # Pop elements in sorted order
    return sorted_arr

def bubble_sort(arr):
    n = len(arr)
    # Traverse through all elements in the array
    for i in range(n):
        # Last i elements are already in place, no need to check them
        swapped = False
        for j in range(0, n-i-1):
            # Traverse the array from 0 to n-i-1 and swap if the element found is greater than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        if not swapped:
            break  # If no elements were swapped, the list is already sorted
    return arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        left_half = arr[:mid]  # Dividing the elements into two halves
        right_half = arr[mid:]

        merge_sort(left_half)  # Sorting the first half
        merge_sort(right_half)  # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays left_half[] and right_half[]
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1



with open("data.txt", "r") as data_file:
    N, D = data_file.readlines()
    data = re.findall("\d+", D)
    N, A = int(N), [int(x) for x in data]

begin = time.time()
A = heap_sort(A)
out = time.time()
print(f"堆排序所花时间:{(out - begin) * 1000}毫秒")

A = [int(x) for x in data]
begin = time.time()
A = bubble_sort(A)
out = time.time()
print(f"冒泡排序所花时间:{(out - begin) * 1000}毫秒")

A = [int(x) for x in data]
begin = time.time()
merge_sort(A)
out = time.time()
print(f"合并排序所花时间:{(out - begin) * 1000}毫秒")