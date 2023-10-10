"""
CMSC 14100, Winter 2023
Homework #4

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

EMPTY="Empty"

def how_many_fit(group_sizes, num_seats):
    """
    Determines how many groups can fit in a bus according to group sizes and
    the number of seats on the bus.

    Inputs:
        group_sizes [list[int]]: sizes of the groups
        num_seats [int]: number of seats on the bus
    
    Returns [int]: the number of groups that fit on the bus
    """

    groups_fit = 0
    for group in group_sizes:
        if num_seats - group >= 0:
            num_seats = num_seats - group
            groups_fit += 1
        elif num_seats - group < 0:
            return groups_fit
    return groups_fit


def gen_passengers(group_names, group_sizes):
    """
    Generates names for passengers and puts all the names in a list.

    Inputs:
        group_names [list[str]]: names for each group
        group_sizes [list[int]]: size of each group

    Returns [list]: names of the passengers according to group
    """
    assert len(group_names) == len(group_sizes)

    names_of_passengers = []
    for idx, name_group in (enumerate(group_names)):
        for n in range(group_sizes[idx]):
            names_of_passengers.append(group_names[idx]+"-"+str(n+1))
    return names_of_passengers


def fill_bus(group_names, group_sizes, bus_config):
    """
    Generate a bus map using a list of group names, group sizes, and the
    bus configuration. 

    Inputs:
        group_names [list[str]]: list of group names
        group_sizes [list[int]]: list of group sizes
        bus_config [tuple[int]]: dimensions of the bus

    Returns [list[str]]: bus map with names and positions
    """

    bus_map = []
    num_seats = bus_config[0] * bus_config[1]
    passenger_list = gen_passengers(group_names, group_sizes)
    if num_seats > len(passenger_list):
        for i in range(num_seats - len(passenger_list)):
            passenger_list.append("Empty")
    position = 0
    for n in range(bus_config[0]):
        people_list = ",".join(passenger_list[position:position+bus_config[1]])
        bus_map.append(people_list)
        position += bus_config[1]
    return bus_map

def mk_fleet(group_names, group_sizes, bus_config):
    """
    Generates a fleet of buses with a certain configuration so that 
    all groups are assigned to a bus.

    Inputs:
        group_names [list[str]]: list of group names
        group_sizes [list[int]]: list of group sizes
        bus_config [tuple[int]]: dimensions of the bus

    Returns [list[str]]: a list of passengers in their respective busses
    """
    num_seats = bus_config[0] * bus_config[1]
    gs_bus = []
    gn_bus = []
    bus_name = []
    bus_size = []
    total = 0
    for idx, val in enumerate(group_sizes):
        total += val
        bus_name.append(group_names[idx])
        bus_size.append(val)
        if idx + 1 == len(group_sizes):
            gs_bus.append(bus_size)
            gn_bus.append(bus_name)
            break
        if total + group_sizes[idx + 1] > num_seats:
            gs_bus.append(bus_size)
            gn_bus.append(bus_name)
            bus_size = []
            bus_name = []
            total = 0
    bus_fleet = []
    for idx, val in enumerate(gs_bus):
        bus_fleet.append(fill_bus(gn_bus[idx], val, bus_config))
    return bus_fleet
