"""
CMSC 14100
Winter 2023

Homework #3

We will be using anonymous grading, so please do NOT include your name
in this file

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URL of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.


[RESUBMISSIONS ONLY: Explain how you addressed the grader's comments
 for your original submission.  If you did not submit a solution for the
 initial deadline, please state that this submission is new.]
"""

# Provided function
def is_car(weight):
    """
    Does a vehicle qualify as a car?

    Inputs:
        weight [float]: vehicle's weight

    Returns [bool]: True, if the vehicle qualifies as a car.
        False, otherwise.
    """
    return weight < 4500

# Constants used in Exercises 1-2

URBAN_SPEED_LIMIT = 25
SUBURBAN_SPEED_LIMIT = 55
RURAL_CAR_SPEED_LIMIT = 70
RURAL_TRUCK_SPEED_LIMIT = 55

def determine_speed_limit(area_type, weight):
    """
    Determine the speed limit for a vehicle based on the type of area
    in which it is travelling and its weight.

    Inputs:
        area_type [string]: one of "urban", "suburban", and "rural"
        weight [float]: the weight of the vehicle

    Returns [int]: the speed limit for the vehicle
    """
    # Verify that the parameters have sensible values
    assert area_type in ("urban", "suburban", "rural")
    assert weight > 0

    if area_type == "urban":
        return URBAN_SPEED_LIMIT
    elif area_type == "suburban":
        return SUBURBAN_SPEED_LIMIT
    elif area_type == "rural":
        if is_car(weight):
            return RURAL_CAR_SPEED_LIMIT
        else:
            return RURAL_TRUCK_SPEED_LIMIT

def is_over_limit(area_type, weight, speed):
    """
    Determine whether a vehicle is speeding based on the type of area it is
    traveling in, its weight, and its speed.

    Inputs:
        area_type [string]: one of "urban", "suburban", and "rural"
        weight [float]: the weight of the vehicle
        speed [float]: the speed of the vehicle

    Returns [bool]: Returns True, if vehicle is over the speed limit depending
        on given conditions, False, otherwise.
    """
    # Verify that the parameters have sensible values
    assert area_type in ("urban", "suburban", "rural")
    assert weight > 0
    assert speed >= 0

    return speed > determine_speed_limit(area_type, weight)

def min_in_neighborhood(values, location):
    """
    Determines the minimum value in a neighborhood around the specified
    index position.

    Inputs:
        values [list]: list of values in neighborhood
        location [int]: position in the index

    Returns [int]: minimum value around a specified index position
    """
    # Verify that the list has at least one element
    assert len(values) > 0
    # Verify that location is a legal non-negative index for values.
    assert 0 <= location < len(values)
  
    max_idx = len(values) - 1
    left_idx = location - 1
    right_idx = location + 1
    if left_idx < 0:
        left_idx = 0
    if right_idx > max_idx:
        right_idx = max_idx
    if (values[location] <= values[left_idx] and
        values[location] <= values[right_idx]):
        return values[location]
    elif (values[left_idx] <= values[location] and 
        values[left_idx] <= values[right_idx]):
        return values[left_idx]
    elif (values[right_idx] <= values[location] and
        values[right_idx] <= values[left_idx]):
        return values[right_idx]

def idx_min_neighborhood(values, location):
    """
    Determines the index with the minimum value in a neighborhood around 
    the specified index position, returning the lower index if two values
    are the same.

    Inputs:
        values [list]: list of values in neighborhood
        location [int]: position in the index

    Returns [int]: index position with the minimum value
    """
    # Verify that the list has at least one element
    assert len(values) > 0
    # Verify that location is a legal (non-negative) index for values.
    assert 0 <= location < len(values)

    max_idx = len(values) - 1
    left_idx = location - 1
    right_idx = location + 1
    if left_idx < 0:
        left_idx = 0
    if right_idx > max_idx:
        right_idx = max_idx
    if (values[location] < values[left_idx] and
        values[location] < values[right_idx]):
        return location
    elif (values[location] == values[left_idx] and
        values[location] < values[right_idx]):
        return left_idx
    elif (values[left_idx] <= values[location] and 
        values[left_idx] <= values[right_idx]):
        return left_idx
    elif (values[right_idx] < values[location] and
        values[right_idx] < values[left_idx]):
        return right_idx
    elif (values[right_idx] == values[location] and
        values[right_idx] < values[left_idx]):
        return location
    elif (values[left_idx] == values(location) == values[right_idx]):
        return left_idx

def sum_reciprocals(vals):
    """
    Compute the sum of the reciprocals of all integers in a list.

    Input:
        vals list [int]: list of numbers n

    Returns [float]: sum of all the reciprocals from a list of integers 
        as a float
    """

    total = 0
    for n in vals:
        total = total + (1 / n)
    return total

def count_trucks(vehicle_weights):
    """
    Computes the number of trucks in a list according to vehicle weight.

    Input:
        vehicle_weights list [float]: list of the weights of vehicles v
    
    Returns [int]: number of trucks in the list of vehicles
    """
 
    total = 0
    for v in vehicle_weights:
        if not is_car(v):
            total = total + 1
    return total


def largest_divisible_by(vals, divisor):
    """
    Determines the largest integer in a list that is divisible by a given
    divisor.

    Inputs:
        vals list [int]: list of numbers n
        divisor [int]: the divisor being used on the numbers in the list

    Returns [int | None]: largest integer divisible by the divisor.
        None otherwise
    """

    max_num = None
    for n in vals:
        if n % divisor == 0 and max_num == None:
            max_num = n
        elif n % divisor == 0 and n > max_num:
            max_num = n
    return max_num