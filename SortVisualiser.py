import pygame
import random

pygame.init()


class DrawInformation:  # These are the colors I am using in our project
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    LAVENDER = 230, 230, 250
    RED = 255, 0, 0
    YELLOW = 255, 255, 0
    BLUE = 135, 206, 235
    ROSE_GOLD = 183, 110, 121
    EMERALD_GREEN = 80, 200, 120
    CHAMPAGNE = 247, 231, 206
    CHARCOAL_GREY = 54, 69, 79
    BURGUNDY = 128, 0, 32
    BACKGROUND_COLOR = CHAMPAGNE
    
    GRADIENTS = [   #Colors for the bars to differentiate
        (0, 31, 63),  ## NAVY BLUE
        (80, 200, 120), # EMERALD GREEN
        (183, 110, 121) # ROSE GOLD
    ]
    
    FONT = pygame.font.SysFont('Brass Mono Regular', 14)
    LARGE_FONT = pygame.font.SysFont('Brass Mono Regular', 26)
    
    SIDE_PAD = 100
    TOP_PAD = 150
    # Both the above variables are for padding in px

    def __init__(
        self, width, height, lst
    ):  # this constructor takes widht, height, and a list to sort

        self.width = width
        self.height = height

        self.window = pygame.display.set_mode(
            (width, height)
        )  # This part is to set an actual display for the pygame to visualise our code

        pygame.display.set_caption("Sorting Algorithm Visualiser")  # Title
        self.set_list(lst)

    def set_list(self, lst):  # creates a list
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.bar_width = round((self.width - self.SIDE_PAD) / len(lst))  

        # Avoid division by zero & ensure scaling works properly
        range_val = max(self.max_val - self.min_val, 1)
        self.scale_factor = (self.height - self.TOP_PAD) / range_val  

        self.start_x = self.SIDE_PAD // 2  


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", True, draw_info.ROSE_GOLD)
    draw_info.window.blit(title, (draw_info.width // 2 - title.get_width() // 2, 10))

    controls = draw_info.FONT.render("R - Reset  |  SPACE - Sort  |  A - Ascending  |  D - Descending", True, draw_info.CHARCOAL_GREY)
    draw_info.window.blit(controls, (draw_info.width // 2 - controls.get_width() // 2, 50))

    sorting = draw_info.FONT.render("1 - Bubble Sort | 2 - Count Sort | 3 - Insertion Sort | 4 - Merge Sort | 5 - Quick Sort | 6 - Selection Sort | 7 - Stalin Sort | 8 - Bogo Sort | 9 - Orwell Sort", True, draw_info.CHARCOAL_GREY)
    draw_info.window.blit(sorting, (draw_info.width // 2 - sorting.get_width() // 2, 80))
    sorting = draw_info.FONT.render("B - Deletion Sort", True, draw_info.CHARCOAL_GREY)
    draw_info.window.blit(sorting, (draw_info.width // 2 - sorting.get_width() // 2, 120))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions = {}, clear_bg = False): # Sizes, heights, colors of bars in a list.
        lst = draw_info.lst

        if clear_bg:
            clear_rect  = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
            pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
        
        
        for i, val in enumerate(lst):
            x = draw_info.start_x + i * draw_info.bar_width
            height = (val - draw_info.min_val) * draw_info.scale_factor  # height of the bars
            y = draw_info.height - height  # Ensure bars start from the bottom

            color = draw_info.GRADIENTS[i % 3]  # i % 3 because for 3 diff colors if needed 4 then i % 4
            
            if i in color_positions:
                color = color_positions[i]
            
            
            pygame.draw.rect(draw_info.window, color, (x, y, draw_info.bar_width, height))  # rectangle function

        if clear_bg:
            pygame.display.update()


def generate_starting_list(
    n, min_val, max_val
):  # Creates a list in between the range of minval given and maxVal given to the system. Inclusive of minVal and maxVal
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def deletion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    
    while len(lst) > 1:
        min_or_max = min(lst) if ascending else max(lst)
        lst.remove(min_or_max)  # Keep deleting the min/max element
        draw_list(draw_info, {i: draw_info.RED for i in range(len(lst))}, True)
        yield True
    
    return lst

def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst
    
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            
            if (lst[j] > lst[j + 1] and ascending) or (lst[j] < lst[j + 1] and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j : draw_info.RED, j + 1 : draw_info.BLUE}, True)
                yield True
    
    return lst

def stalin_sort(draw_info, ascending=True):
    lst = draw_info.lst
    
    if not lst:
        return lst
    
    sorted_lst = [lst[0]]  # Start with the first element
    draw_list(draw_info, {0: draw_info.BLUE}, True)
    yield True
    
    for i in range(1, len(lst)):
        if (ascending and lst[i] >= sorted_lst[-1]) or (not ascending and lst[i] <= sorted_lst[-1]):
            sorted_lst.append(lst[i])
            draw_list(draw_info, {i: draw_info.BLUE}, True)
            yield True
    
    draw_info.lst = sorted_lst  # Update the list in draw_info
    return sorted_lst

def bogo_sort(draw_info, ascending=True):
    lst = draw_info.lst
    
    def is_sorted(lst):
        return all(lst[i] <= lst[i+1] for i in range(len(lst)-1)) if ascending else all(lst[i] >= lst[i+1] for i in range(len(lst)-1))
    
    while not is_sorted(lst):
        random.shuffle(lst)
        draw_list(draw_info, {i: draw_info.BLUE for i in range(len(lst))}, True)
        yield True
    
    return lst


def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]
        j = i

        while j > 0 and ((lst[j - 1] > current and ascending) or (lst[j - 1] < current and not ascending)):
            lst[j] = lst[j - 1]  # Shift element to the right
            j -= 1
            draw_list(draw_info, {j: draw_info.RED, j - 1: draw_info.BLUE}, True)
            yield True  # Yield to update visualization

        lst[j] = current  # Place the current element in the correct position
        draw_list(draw_info, {j: draw_info.EMERALD_GREEN}, True)
        yield True  # Yield to update visualization

    return lst

def selection_sort(draw_info, ascending = True):
    lst = draw_info.lst
    
    for i in range(len(lst)):
        min_idx = i
        
        for j in range(i + 1, len(lst)):
            if (lst[min_idx] > lst[j] and ascending) or (lst[min_idx] < lst[j] and not ascending):
                min_idx = j
                draw_list(draw_info, {min_idx : draw_info.RED, i : draw_info.BLUE}, True)
                yield True
        
        
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_info, {i : draw_info.EMERALD_GREEN}, True)
        yield True
 
    return lst

def merge_sort(draw_info, ascending=True):
    def merge(lst, l, m, r):
        left = lst[l:m + 1]
        right = lst[m+1:r+1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            if (left[i] <= right[j] and ascending) or (left[i] >= right[j] and not ascending):
                lst[k] = left[i]
                i += 1
            else:
                lst[k] = right[j]
                j += 1
            draw_list(draw_info, {k: draw_info.RED}, True)
            yield True
            k += 1
        while i < len(left):
            lst[k] = left[i]
            draw_list(draw_info, {k: draw_info.RED}, True)
            yield True
            i += 1
            k += 1
        while j < len(right):
            lst[k] = right[j]
            draw_list(draw_info, {k: draw_info.RED}, True)
            yield True
            j += 1
            k += 1
    
    def merge_sort_helper(lst, l, r):
        if l < r:
            m = (l + r) // 2
            yield from merge_sort_helper(lst, l, m)
            yield from merge_sort_helper(lst, m + 1, r)
            yield from merge(lst, l, m, r)
    
    yield from merge_sort_helper(draw_info.lst, 0, len(draw_info.lst) - 1)
    return draw_info.lst
    
def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst  

    def quick(lst, low, high):
        if low < high:
            pivot_index = yield from partition(lst, low, high)  # Correctly retrieve pivot index
            
            yield from quick(lst, low, pivot_index - 1)
            yield from quick(lst, pivot_index + 1, high)

    def partition(lst, low, high):
        pivot = lst[high]  # Choosing the last element as the pivot
        i = low - 1  # Pointer for smaller elements

        for j in range(low, high):
            if (ascending and lst[j] <= pivot) or (not ascending and lst[j] >= pivot):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]  # Swap
                draw_list(draw_info, {i: draw_info.RED, j: draw_info.BLUE}, True)
                yield True  # Yield to visualize steps

        # Swap pivot to its correct position
        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        draw_list(draw_info, {i + 1: draw_info.EMERALD_GREEN}, True)
        yield True

        return i + 1  # Correctly return pivot index after partitioning

    yield from quick(lst, 0, len(lst) - 1)

def count_sort(draw_info, ascending=True):
    lst = draw_info.lst
    
    maxx = max(lst)
    count_arr = [0] * (maxx + 1)
    
    # Count occurrences
    for v in lst:
        count_arr[v] += 1

    if ascending:
        i = 0
        order = range(len(count_arr))  # Ascending order
    else:
        i = 0
        order = range(len(count_arr) - 1, -1, -1)  # Descending order

    for k in order:
        while count_arr[k] > 0:
            lst[i] = k
            count_arr[k] -= 1
            draw_list(draw_info, {i: draw_info.RED}, True)  # Update visualization
            yield True  # Yield to allow visualization update
            i += 1

    return lst

def orwell_sort(draw_info, ascending=True):
    lst = draw_info.lst
    
    # No matter what, claim the list is sorted
    draw_list(draw_info, {i: draw_info.BLUE for i in range(len(lst))}, True)
    yield True
    
    return lst


def main():  # Contains main driver code Used for the button interactions, PyGame Event loop
     
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1366, 720, lst)

    sorting = False
    ascending = True  # Keep track of sorting order

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type != pygame.KEYDOWN:
                continue
            
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
                
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                
            elif event.key == pygame.K_a and not sorting:
                ascending = True  # Set sorting order to ascending
                
            elif event.key == pygame.K_d and not sorting:
                ascending = False  # Set sorting order to descending
                
            elif event.key == pygame.K_3 and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name  = "Insertion Sort"
            elif event.key == pygame.K_1 and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_6 and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
            elif event.key == pygame.K_4 and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"
            elif event.key == pygame.K_5 and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_2 and not sorting:
                sorting_algorithm = count_sort
                sorting_algo_name = "Count Sort"
            elif event.key == pygame.K_7 and not sorting:
                sorting_algorithm = stalin_sort
                sorting_algo_name = "Stalin Sort"
            elif event.key == pygame.K_8 and not sorting:
                sorting_algorithm = bogo_sort
                sorting_algo_name = "Bogo Sort"
            elif event.key == pygame.K_9 and not sorting:
                sorting_algorithm = orwell_sort
                sorting_algo_name = "Orwell Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = deletion_sort
                sorting_algo_name = "Deletion Sort"

    pygame.quit()


if __name__ == "__main__":  # If name == main it just runs the main function.
    main()
