"""
CMSC 14100, Autumn 2022
Homework #5

We will be using anonymous grading, so please do NOT include your name
in this file

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

# Color constants that will be useful for testing purposes.
# You will not need to use these constants in your solution.

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def add_triples(triple1, triple2):
    """
    Computes the sum of integers in tuples, creating a new tuple with the
    three sums.

    Inputs:
        triple1 [tuple(int,int,int)]: first tuple of three integers
        triple2 [tuple(int,int,int)]: second tuple of three integers

    Returns [tuple(int,int,int)]: sum of the two tuples for each index 
    """
    tuple_sum = []
    for idx, val in enumerate(triple1):
        total = val + triple2[idx]
        tuple_sum.append(total)
    tuple_add = tuple(tuple_sum)
    return tuple_add

def scale_triple(triple, factor):
    """
    Computes the product of a set of tuples and a floating point factor, 
    creating a new tuple with the products.

    Inputs:
        triple [tuple(int,int,int)]: tuple of three integers
        factor [float]: factor that the integers will be multiplied by

    Returns [tuple(int,int)]: a tuple with each value in the initial tuple 
        modified by the factor
    """
    tuple_product = []
    for val in triple:
        product = int(val * factor)
        tuple_product.append(product)
    tuple_multiply = tuple(tuple_product)
    return tuple_multiply


def choose_pixel(foreground, background, screen_color, loc):
    """
    Determines the tuple for the pixel at the foreground or background at a
    location in an image depending on screen color. 

    Inputs:
        foreground [list[tuple(int,int,int)]]: the list of pixels making 
            up the foreground image
        background [list[tuple(int,int,int)]]: the list of pixels making 
            up the background image
        screen_color [tuple(int,int)]: color of the screen
        loc [tuple(int,int)]: location being checked
    
    Returns [tuple(int,int,int)]: the pixel code of the correct pixel
    """
    i, j = loc
    if foreground[i][j] != screen_color:
        return foreground[i][j]
    elif foreground[i][j] == screen_color:
        return background[i][j]


def combine_images(foreground, background, screen_color):
    """
    Creates a new image by replacing pixels of a specified color in the
    foreground image with the background image.

    Inputs:
        foreground [list[tuple(int, int, int)]]: the list of pixels making 
            up the foreground image
        background [list[tuple(int, int, int)]]: the list of pixels making 
            up the background image
        screen_color [tuple(int, int, int)]: color of the screen

    Returns [list[tuple(int, int, int)]]: the new image with correctly 
        replaced pixels
    """
    new_image = []
    row_list = []
    for num, row in enumerate(foreground):
        for idx, val in enumerate(row):
            if screen_color != val:
                foreground_pixel = foreground[num][idx]
                row_list.append(foreground_pixel)
            elif screen_color == val:
                background_pixel = background[num][idx]
                row_list.append(background_pixel)
        new_image.append(row_list)
        row_list = []
    return new_image
                

def is_color_in_region(image, region_locs, screen_color):
    """
    Given an image, a list of the locations in a region, and a color,
    determines if the color occurs in the region.

    Inputs:
        image [list[tuple(int, int, int)]]: image with pxels
        region_locs [list[tuple(int, int)]]: list of locations in region
        screen_color [tuple(int, int, int)]: color of the screen
    
    Returns [bool]: True if color occurs at any location in the region,
        False, otherwise
    """
    for points in region_locs:
        x, y = points
        if image[x][y] == screen_color:
            return True
    return False
            

def find_region_locations(image, loc, radius):
    """
    Given an image, a location, and a radius, produces a list of
    locations in the specified radius.

    Inputs:
        image [list[tuple(int, int, int)]]: image with pixels
        loc [tuple(int,int)]: location being checked
        radius [int]: size of radius around a location

    Returns [list[tuple(int, int)]]: all the locations of values that are
        within the given radius at a given location
    """
    i, j = loc
    in_neighborhood = []
    for idx, row in enumerate(image):
        for col, _ in enumerate(row):
            if abs(idx - i) <= radius and abs(col - j) <= radius:
                in_pixel = [idx, col]
                tup_pix = tuple(in_pixel)
                in_neighborhood.append(tup_pix)
            in_pixel = []
    return in_neighborhood


def pixel_blur(foreground, background, screen_color, loc, radius):
    """
    Blurs a pixel in a given environment.

    Inputs:
        foreground [list[tuple(int, int, int)]]: the list of pixels making 
            up the foreground image
        background [list[tuple(int, int, int)]]: the list of pixels making 
            up the background image
        screen_color [tuple(int, int, int)]: color of the screen
        loc [tuple(int,int)]: location being checked
        radius [int]: size of radius around a location

    Returns [tuple(int, int, int)]: a new tuple designating the blurred color
        of the pixel
    """
    image = combine_images(foreground, background, screen_color)
    total = (0,0,0)
    i, j = loc
    all_pixels = find_region_locations(image, loc, radius)
    if is_color_in_region(foreground, all_pixels, screen_color):
        for pix in all_pixels:
            pixel = image[pix[0]][pix[1]]
            total = add_triples(total,pixel)
        averaged = scale_triple(total,1/len(all_pixels))
        return averaged
    else:
        return foreground[i][j]


def combine_with_blurring(foreground, background, screen_color, radius):
    """
    Given two images, blur each pixel in the image after combining them 
    according to screen color and radius. 

    Inputs:
        foreground [list[tuple(int, int, int)]]: the list of pixels making 
            up the foreground image
        background [list[tuple(int, int, int)]]: the list of pixels making 
            up the background image
        screen_color [tuple(int, int, int)]: color of the screen
        radius [int]: size of radius around a location
    
    Returns [list[tuple(int, int, int)]]: the new image with correctly 
        blurred pixels
    """
    
    rows = len(foreground)
    columns = len(foreground[0])
    blurred_image = []
    for i in range(rows):
        blurred_row = []
        for j in range(columns):
            loc = (i, j)
            col = pixel_blur(foreground, background, screen_color, loc, radius)
            blurred_row.append(col)
        blurred_image.append(blurred_row)
    return blurred_image
