import pygame
import random
pygame.init()

class Drawing_Information:

    #Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    PURPLE = (128, 0, 128)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GREY = (128, 128, 128)
    BACKGROUND_COLOR = BLACK


    #sounds
    before_swap = pygame.mixer.Sound("b4.mp3")
    after_swap = pygame.mixer.Sound("aftr.mp3")
    after_swap.set_volume(0.1)
    before_swap.set_volume(0.3)

    #fonts
    p_font = pygame.font.SysFont('Ariel', 30)
    header_font = pygame.font.SysFont('Ariel', 50)
    Title_font = pygame.font.SysFont('Ariel', 50)

    #bar colors 
    bar_clr = [
        #purple 
        (128, 0, 128),
        #darker purple
        (160, 32, 240),
        #lighter purple
        (192, 32, 240),
    ]

    #this is to tell our screen we want 50 px on each side
    L_R_Padding = 150

    #this is to tell our screen we want 100 px on the top
    Top_Padding = 150


    #this init function intitializes the screen 
    #and the height and width of the screen
    def __init__(self, width, height, array):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.initialize_array(array)

    #this function will contain the information about the array
    def initialize_array(self, array):
        self.array = array

        #this is the min and max value of the array
        self.min_val = min(array)
        self.max_val = max(array)

        self.bar_width = int((self.width - self.L_R_Padding) / len(array))
        self.bar_height = int((self.height - self.Top_Padding) / (self.max_val - self.min_val))

        #this is the starting x position of the bars
        self.starting_x = self.L_R_Padding // 2

#this function will draw the bars and give them random values
def Gen_list(length, min, max):
    return [random.randint(min, max) for _ in range(length)]

def Determine_time(algo_name):
    if algo_name == "Merge Sort":
        return "O(n^2 log(n))"
    elif algo_name == "Quick Sort":
        return "O(n log(n))"
    else:
        return "O(n^2)"
    

#this function is what actually displays info to the screen
def Draw_Screen(draw_info: Drawing_Information, algo_name):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    Title = draw_info.Title_font.render("Algorithm visualizer", 1, draw_info.WHITE)

    algorithms = draw_info.p_font.render("b - Bubble Sort | s - Selection Sort | i - Insertion Sort | m - Merge Sort | q - Quick Sort", 1, draw_info.WHITE)


    curr_algo_nme = draw_info.p_font.render(f"Current Algorithm: {algo_name} | Time Complexity: { Determine_time(algo_name) } ", 1, draw_info.RED)


    #borders
    border = (draw_info.L_R_Padding // 2, 60, draw_info.width - draw_info.L_R_Padding, 3)
    pygame.draw.rect(draw_info.window, draw_info.WHITE, border, 3)

    border2 = (draw_info.L_R_Padding // 2, 95, draw_info.width - draw_info.L_R_Padding, 3)
    pygame.draw.rect(draw_info.window, draw_info.WHITE, border2, 3)



    draw_info.window.blit(Title, (draw_info.width / 2 - Title.get_width()/2, 10))
    draw_info.window.blit(algorithms, (draw_info.width / 2 - algorithms.get_width()/2, 70))
    draw_info.window.blit(curr_algo_nme, (draw_info.width / 2 - curr_algo_nme.get_width()/2, 105))


    draw_bars(draw_info)
    pygame.display.update()


def draw_bars(draw_info: Drawing_Information, color_pos = {}, clear = False):
    #this grabs the array from the drawing information class
    lst = draw_info.array

    if clear:
        #this will clear the screen where the bars start and end
        clear_screen = (draw_info.L_R_Padding // 2, draw_info.Top_Padding,
         draw_info.width - draw_info.L_R_Padding, draw_info.height - draw_info.Top_Padding)

        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_screen)

    for idx, val in enumerate(lst):
        x = draw_info.starting_x + idx * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.bar_height

        color_bar = draw_info.bar_clr[idx % 3]

        if idx in color_pos:
            color_bar = color_pos[idx]

        pygame.draw.rect(draw_info.window, color_bar, (x,y,draw_info.bar_width, draw_info.height))

    if clear:
        pygame.display.update()


def bubble_sort(draw_info: Drawing_Information):
    lst = draw_info.array

    for i in range(len(lst) - 1):
        for j in range(len(lst) - i - 1):
            tmp1 = lst[j]
            tmp2 = lst[j + 1]
            if (tmp1 > tmp2):
                draw_info.before_swap.play()
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_bars(draw_info, {j : draw_info.RED, j + 1 : draw_info.GREEN},True)
                yield True
                draw_info.after_swap.play()
        

    return lst

def insertion_sort(draw_info: Drawing_Information):
    lst = draw_info.array

    for i in range(1, len(lst)):
        j = i
        while j > 0 and lst[j-1] > lst[j]:
            draw_info.before_swap.play()
            lst[j], lst[j-1] = lst[j-1], lst[j]
            draw_bars(draw_info, {j : draw_info.RED, j - 1 : draw_info.GREEN}, True)
            yield True
            j -= 1
        draw_info.after_swap.play()
    
    return lst

def selection_sort(draw_info: Drawing_Information):
    lst = draw_info.array

    for i in range(len(lst) - 1):
        min = i
        for j in range(i + 1, len(lst)):
            if lst[j] < lst[min]:
                min = j
                draw_info.before_swap.play()
                draw_bars(draw_info, {i : draw_info.RED, min : draw_info.GREEN}, True)
                yield True
                
        lst[i], lst[min] = lst[min], lst[i]
        draw_info.after_swap.play()

    return lst
 
def partition(draw_info: Drawing_Information, low, high):
    lst = draw_info.array
    i = low - 1
    pivot = lst[high]

    for j in range(low, high):
        if lst[j] <= pivot:
            i += 1
            draw_info.before_swap.play()
            lst[i], lst[j] = lst[j], lst[i]
            draw_bars(draw_info, {i : draw_info.RED, j : draw_info.GREEN}, True)
            yield True
            draw_info.after_swap.play()

    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    draw_bars(draw_info, {i + 1 : draw_info.GREEN, high : draw_info.RED}, True)
    yield True
    draw_info.after_swap.play()

    return i + 1

#when you change the length of the array, you need to change the low and high
def quick_sort(draw_info: Drawing_Information, low=0, high = 50 - 1):
    lst = draw_info.array
    if low < high:
        pi = yield from partition(draw_info, low, high)

        yield from quick_sort(draw_info, low, pi - 1)
        yield from quick_sort(draw_info, pi + 1, high)

    return lst

def merge(draw_info: Drawing_Information, l, m, r):
    lst = draw_info.array

    start2 = m + 1

    if lst[m] <= lst[start2]:
        return
    
    while l <= m and start2 <= r:

        if lst[l] <= lst[start2]:
            l += 1
        else:
            draw_info.before_swap.play()
            value = lst[start2]
            index = start2
            draw_bars(draw_info, {index : draw_info.RED, index - 1 : draw_info.GREEN}, True)
            yield True
            draw_info.after_swap.play()

            while index != l:
                draw_info.before_swap.play()
                lst[index] = lst[index - 1]
                draw_bars(draw_info, {index : draw_info.RED, index - 1 : draw_info.GREEN}, True)
                yield True
                draw_info.after_swap.play()
                index -= 1
            
            draw_info.before_swap.play()
            lst[l] = value
            draw_bars(draw_info, {l : draw_info.GREEN, index : draw_info.GREEN}, True)
            yield True
            draw_info.after_swap.play()

            l += 1
            m += 1
            start2 += 1

#when you change the length of the array, you need to change the low and high
def merge_sort(draw_info: Drawing_Information, l=0, r = 50 - 1):
    lst = draw_info.array

    if l < r:
        m = (l + r) // 2

        yield from merge_sort(draw_info, l, m)
        yield from merge_sort(draw_info, m + 1, r)

        yield from merge(draw_info, l, m, r)
    

    return lst

def after_sort(draw_info: Drawing_Information):
    lst = draw_info.array

    for i in range(len(lst)):
        draw_bars(draw_info, {i : draw_info.GREEN}, True)
        yield True

    return lst


def main_():
    run = True
    clock = pygame.time.Clock()


    #this will be the length and min, max of the array
    #max n = 400
    n = 50
    min = 0

    #max = 650
    max = 650
    
    #this will be the array that we will be sorting
    arr = Gen_list(n,min,max)

    #this will be the drawing information class
    Test = Drawing_Information(1000,800,arr)

    #this will be the boolean that will tell us if we are sorting or not
    sorting = False

    #current algorithm
    curr_algo = bubble_sort
    algo_nme = "Bubble Sort"
    sorting_algorithm_generator = None

    #this loop handled all events 
    while run:

        #this controls the framerate of the screen
        clock.tick(30)

        #this will check if we are sorting or not
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            #this draws to the screen
            Draw_Screen(Test, algo_nme)


        for event in pygame.event.get():

            #if the red x is clicked it quits the game
            #if not implemented it WILL NOT EXIT
            if event.type == pygame.QUIT:
                run = False
                break

            #this will check if a key is pressed
            if event.type != pygame.KEYDOWN:
                continue
            
            #this will generate a new array if the r key is pressed
            if event.key == pygame.K_r:
                lst = Gen_list(n,min,max)
                Test.initialize_array(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = curr_algo(Test)
            elif event.key == pygame.K_b and sorting == False:
                algo_nme = "Bubble Sort"
                curr_algo = bubble_sort
            elif event.key == pygame.K_i and sorting == False:
                algo_nme = "Insertion Sort"
                curr_algo = insertion_sort
            elif event.key == pygame.K_s and sorting == False:
                algo_nme = "Selection Sort"
                curr_algo = selection_sort
            elif event.key == pygame.K_q and sorting == False:
                algo_nme = "Quick Sort"
                curr_algo = quick_sort
            elif event.key == pygame.K_m and sorting == False:
                #NOTE this is an in place implementation of merge sort
                #due to this, instead of a time complexity of O(nLogn) it is O(n^2 * Logn)
                algo_nme = "Merge Sort"
                curr_algo = merge_sort
            elif event.key == pygame.K_0:
                Test.after_swap.set_volume(0)
                Test.before_swap.set_volume(0)
            elif event.key == pygame.K_1:
                Test.after_swap.set_volume(0.1)
                Test.before_swap.set_volume(1)

    pygame.quit()


if __name__ == "__main__":
    main_()

