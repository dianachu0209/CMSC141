"""
CMSC 14100
Winter 2023

Homework #2

We will be using anonymous grading, so please do NOT include your name
in this file

People Consulted:
   If you discussed this assignment with anyone other than the course staff,
   list their name(s) here.  Listing other students by name in
   this section will not interfere with anonymous grading.

Online resources consulted:
   List the URL of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.

[RESUBMISSIONS ONLY: Explain how you addressed the grader's comments
 for your original submission.  If you did not submit a solution for the
 initial deadline, please state that this submission is new.]
"""

def add_one_and_multiply(a, x):
    """
    Add 1 to a, and multiply by x

    Inputs:
        a [int]: an integer value
        x [int]: another integer value


    Returns [int]: result of adding 1 to a and then multiplying by x.
    """
    return (a + 1) * x


def have_different_remainders(a, b, n):
    """
    Do a and b have different integer remainders when divided by n?

    Inputs:
        a [int]: an integer value
        b [int]: another integer value
        n [int]: the divisor

    Returns [bool]: True if a and b have different remainders when divided by n,
        and False otherwise.
    """

    return (a % n) != (b % n)


def compute_time(payoff_amount, principal, rate_as_percent):
    """
    Compute the amount of time it will take earn a given payoff amount
    for a given starting principal amount and rate assuming
    simple interest.

    Inputs:
        payoff_amount [float]: the amount paid off at the end
        principal [float]: the face value of the bond
        rate_as_percent [float]: the annual interest rate for the loan
            specified as a percentage

    Return [float]: time period for the bond
    """
    # The next three lines verify that the parameters make sense
    # for the task.
    assert principal > 0
    assert rate_as_percent > 0
    assert payoff_amount >= principal
    interest_per_year = ((1 + rate_as_percent / 100) * principal) - principal
    return (payoff_amount - principal) / (interest_per_year)

# Constants used in Exercises 4-7

TRUCK_WEIGHT_THRESHOLD = 4500
URBAN_SPEED_LIMIT = 25
RURAL_CAR_SPEED_LIMIT = 70
RURAL_TRUCK_SPEED_LIMIT = 55

def is_truck(weight):
    """
    Determine whether the vehicle qualifies as a truck.

    Inputs:
        weight [float]: the weight of the vehicle

    Returns [bool]: True if vehicle is at or above the heavy vehicle
        limit.  False, otherwise.
    """
    # The assertion verifies that the value supplied for the weight
    # is appropriate for the task.
    assert weight > 0

    return weight >= TRUCK_WEIGHT_THRESHOLD


def urban_is_speeding(speed):
    """
    Is a vehicle speeding in an urban area?

    Inputs:
        speed [float]: the vehicle's speed

    Returns [bool]: Returns True, if the vehicle considered to be speeding,
        False, otherwise.
    """

    return speed > URBAN_SPEED_LIMIT


def rural_is_speeding(weight, speed):
    """
    Is a vehicle speeding?  The speed limit is set based on the weight
    of the vehicle and whether the vehicle is travelling in a rural area.

    Inputs:
        weight [float]: the weight of the vehicle
        speed [float]: the vehicle's speed

    Returns [bool]: Returns True, if the vehicle considered to be speeding,
        False, otherwise.
    """
    # The assertions verify that the value supplied for the weight
    # and the value supplied for the speed are appropriate for the
    # task.
    assert weight > 0
    assert speed >= 0

    return ((is_truck(weight) and (speed > RURAL_TRUCK_SPEED_LIMIT)) 
        or (speed > RURAL_CAR_SPEED_LIMIT))

def is_not_speeding(weight, speed, is_urban):
    """
    Determines if a car is speeding based on its weight, speed, and whether
    or not it is in an urban environment.

    Inputs:
        weight [float]: the weight of the vehicle
        speed [float]: the vehicle's speed
        is_urban [bool]: True if vehicle is in urban environment
            and false otherwise

    Returns [bool]: Returns True, if the vehicle is not speeding with the given
        conditions, False, otherwise
    """
    # The assertions verify that the value supplied for the weight
    # and the value supplied for the speed are appropriate for the
    # task.
    assert weight > 0
    assert speed >= 0

<<<<<<< HEAD
    ### Exercise 7
    ### Replace pass with an appropriate return statement

    ### See the writeup for additional requirements for this task.
    return (((speed < URBAN_SPEED_LIMIT) and is_urban) 
        and (rural_is_speeding(weight, speed)))
=======
    return not (rural_is_speeding(weight, speed) or
        (urban_is_speeding(speed) and is_urban))