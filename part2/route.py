#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Pradeep Reddy Rokkam and Joy Zayatz
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys

# Code to read the cities and their GPS co-ordiantes (Lattitudes and Longitudes)
def city_gps_read():
    print("Pradeep Reddy Rokkam")
    city_gps_detail={}
    i=0
    with open('city-gps.txt','r') as f:
        for line in f:
            city_gps_detail[line.split()[0]]=line.split()[1:]
            # print(i,end="--")
            i+=1
    return city_gps_detail

# Code to read the cities and gets all the connected cities with the information of distance, speed limit and the highway that needs to taken to reach from source city to its connected city 
def road_segments_read():
    print("Pradeep Reddy Rokkam")
    road_segment_detail={}
    i=0
    with open('road-segments.txt','r') as f:
        for line in f:
            if line.split()[0] in road_segment_detail:
                road_segment_detail[line.split()[0]].append(line.split()[1:])
            else:
                road_segment_detail[line.split()[0]]=[]
                road_segment_detail[line.split()[0]].append(line.split()[1:])
            # print(i,end="--")
            i=i+1
        return road_segment_detail




def get_route(start, end, cost):

    
    city_gps=city_gps_read() # Has dictionary of cities as the keys and the values being their lattitudes and longitudes in a list 
    print("The number of cities are ")
    print(len(city_gps.keys()))
    print(city_gps['Bloomington,_Indiana'])

    road_segment=road_segments_read() #Has a dictinary of cities as the keys and their values are list of lists, where the lists has information of its connected cities and the info for navigation like distance,max spee dof the route and teh high way infromation
    print("The number of keys are")
    print(len(road_segment.keys()))





    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
                   ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
                   ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    
    return {"total-segments" : len(route_taken), 
            "total-miles" : 51., 
            "total-hours" : 1.07949, 
            "total-delivery-hours" : 1.1364, 
            "route-taken" : route_taken}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


