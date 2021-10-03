#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Pradeep Reddy Rokkam and Joy Zayatz
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
from os import get_inheritable
import sys
import math
# from typing import ContextManager

# Code to read the cities and their GPS co-ordiantes (Lattitudes and Longitudes)
def city_gps_read():
    city_gps_detail={}
    with open('city-gps.txt','r') as f:
        for line in f:
            city_gps_detail[line.split()[0]]=line.split()[1:]
            # print(i,end="--")
    return city_gps_detail

# Code to read the cities and gets all the connected cities with the information of distance, speed limit and the highway that needs to taken to reach from source city to its connected city 
def road_segments_read():
    road_segment_detail={}
    with open('road-segments.txt','r') as f:
        for line in f:
            # Get the cities and their connected cities information. This will take care of one way information. Remember this road can work in other way as well. That will be handled in the next if statement
            if line.split()[0] in road_segment_detail:
                road_segment_detail[line.split()[0]].append(line.split()[1:]) 
            else:
                road_segment_detail[line.split()[0]]=[]
                road_segment_detail[line.split()[0]].append(line.split()[1:])
            
            # This will take care of two way routes
            if line.split()[1] in road_segment_detail:
                road_segment_detail[line.split()[1]].append(list((line.split()[0],line.split()[2],line.split()[3],line.split()[4])))
            else:
                road_segment_detail[line.split()[1]]=[]
                road_segment_detail[line.split()[1]].append(list((line.split()[0],line.split()[2],line.split()[3],line.split()[4])))
            
        return road_segment_detail

# For the given road segments get the distance such that it has maximum distance between two segments
def get_max_dist_segment():
    distance=[]
    with open('road-segments.txt','r') as f:
        for line in f:
            a=line.split()[2]
            distance.append(a)
    return (max(distance))
               
# For the given road segments get the spped that has maximum speed between two segments
def get_max_speed_segment():
    speed=[]
    with open('road-segments.txt','r') as f:
        for line in f:
            a=line.split()[3]
            speed.append(a)
    return (max(speed))


# Get the Estimated distance between two cities, this is will be used as the heuristic function. This is crucial to our program 
def estimated_dist(city_gps,curr_city,dest_city):
    
    #How does our heuristic function should be?
        # Our heuristics function should take inputs as lattititudes and longitudes, and output as a distance in  miles
            #Why only miles:
                #Because the curr distance g(s) is miles and we want our estimated distance in miles as well
    # Using the Haversine Formula we can get distance between two co ordinates

    lat1=float(city_gps[str(curr_city)][0])
    long1= float(city_gps[str(curr_city)][1])
    lat2=float(city_gps[str(dest_city)][0])
    long2= float(city_gps[str(dest_city)][1])


    #Converting the the lattiudes and longitudes into radians
    pii=math.pi

    lat1 = lat1*(pii/180)
    long1 = long1*(pii/180)
    lat2 = lat2*(pii/180)
    long2 = long2*(pii/180)
    
    a=( math.sin((lat1-lat2)/2) * math.sin((lat1-lat2)/2) ) +  (  math.cos(lat1) *  math.cos(lat2) * (math.sin((long1-long2)/2) * math.sin((long1-long2)/2))  )

    c= 2* math.atan2 (math.sqrt(a),math.sqrt(1-a))

    distance = 3958.8 * c

    return distance




def get_route(start, end, cost):

    # Fringe tha thas all the un-expanded cities along with their proirity( lower the number higher the priority)
        #Priority may vary based on the cost function
            # First lets obtain the right answer for the cost function distance 
            # This involves the heuristic function f(s)=g(s)+h(s) where g(s) is the cost of the path so far and h(s) is the heuristic function that will estimate the cost from the current city to the destination city
            # What is the Heuristic Function in our case?
                # Shortest Possible distance (asuuming a staright line path and no obstacles in between) between the current city and the destination city through lattitudes and longitudes
                    # Check if latitiudes and longitudes are the legal ones are not 
                    # Make sure the distance is not negative
                    # Also make sure that it is a straight line distance i.e. it is the shortest distance possible and is less than the optimal cost. This condition ensures the admissibilty 

    city_gps=city_gps_read() # Has dictionary of cities as the keys and the values being their lattitudes and longitudes in a list 

    road_segment=road_segments_read() #Has a dictinary of cities as the keys and their values are list of lists, where the lists has information of its connected cities and the info for navigation like distance,max spee dof the route and teh high way infromation

    # Check if the source and destination cities are in the City GPS and Segment File
    if start not in city_gps.keys() or start not in road_segment.keys() or end not in city_gps.keys() or end not in road_segment.keys()  :
        return False

    if start==end:
        return "Your source and destination are same"

    count_2=0

    if cost=="distance":
        #Add the fringe Data Structure
        curr_dist=0
        est_dist= estimated_dist(city_gps,start,end)
        # Creating a list of tuples to store the route taken 
        route_taken=[[]]
        time_taken=0
        delivery_time=0
        fringe=[(start,curr_dist,est_dist,time_taken,delivery_time,route_taken)] # Adding the start city and the priority(f(s)= g(s)+h(s)) to the fringe

        while fringe:   
            
            high_priority= min([x[1]+x[2] for x in fringe]) # Get the city that has the highest priority (also means the city with the lowest heuristic distance)

            index_high_prty= [x[1]+x[2] for x in fringe].index(high_priority) #Get the index where the highest priority lies in 

            curr_city_prty=fringe.pop(index_high_prty) # Pop the city with the highest priority 

            # print("The city with the highest priority that was popped {}".format(curr_city_prty[0:3]))
            curr_city=curr_city_prty[0]
            curr_dist=curr_city_prty[1]
            curr_est_distance=curr_city_prty[2]
            time_taken=curr_city_prty[3]
            delivery_time=curr_city_prty[4]
            route_taken=curr_city_prty[5]
            
            # Check if the city that is popped out from the from fringe is the destination city, if it is tru then break out of the loop
            if curr_city==end:
                # print("-------------------------*-------------------------You have reached your destination -------------------------*--------------------------")
                route_taken.pop(0)
                # print(route_taken)
                break
            
            #Adding the successors to the fringe 
            for next_city in road_segment[curr_city]:
               
                dist_travelled=curr_dist+float(next_city[1]) # This gives the distance travelled byb our driver to reach this particular city 
                time_travelled=time_taken + (float(next_city[1])/float(next_city[2])) # Distance divided by Speed Limit will give us the time taken

                # Code to get delivery time 
                if float(next_city[2])<50:
                    del_time=delivery_time + (float(next_city[1])/float(next_city[2]))
                else:
                    del_time= delivery_time +(float(next_city[1])/float(next_city[2])) + (math.tanh(float(next_city[1])/1000 * 2 * (delivery_time + ((float(next_city[1])/float(next_city[2])) ))))

                # If a city's information is not avialble in the city-gps.txt, it difficult to evalute the estimated distance between the given city and the destination as we dont have any co-ordinates information
                if next_city[0] not in city_gps.keys() and next_city[0] in road_segment.keys(): 
                    # print("-----",curr_city,"--------",next_city[0])
                    estimated_distance=curr_est_distance
              
                elif next_city[0] not in city_gps.keys() and next_city[0]  not in road_segment.keys(): 
                    continue
                else:
                    estimated_distance=estimated_dist(city_gps,next_city[0],end)

                # We wiil only add a city to the fringe if it is not already on the fringe
                if next_city[0] not in [x[0] for x in fringe]:

                    curr_route= [[next_city[0],"{} for {} miles".format(next_city[3],next_city[1])]] # Routr to move from the previous city to this city 

                    curr_route= route_taken+curr_route #Adding the rout from previous city to the current city to the route of that has info to recah from source to the prvious city. This will give us the entire route from source to destination

                    fringe.append((next_city[0],dist_travelled,estimated_distance,time_travelled,del_time,curr_route)) # Append all the successor information to the fringe 
            # print(fringe)
      # Counter to see the number of times the loop has run
            if count_2%1000==0:
                print(count_2)
            count_2+=1


    if cost=="segments":
        #Add the fringe Data Structure
        curr_segments=0
        curr_dist=0
        max_dist_seg= get_max_dist_segment()

        print(max_dist_seg)

        est_segments= estimated_dist(city_gps,start,end) / float(max_dist_seg)
        est_dist=estimated_dist(city_gps,start,end)
        # Creating a list of tuples to store the route taken 
        route_taken=[[]]
        time_taken=0
        delivery_time=0
        fringe=[(start,curr_dist,est_dist,curr_segments,est_segments,time_taken,delivery_time,route_taken)] # Adding the start city and the priority(f(s)= g(s)+h(s)) to the fringe

        while fringe:   

            high_priority= min([x[3]+x[4] for x in fringe]) # Get the city that has the highest priority (also means the city with the lowest heuristic distance)

            index_high_prty= [x[3]+x[4] for x in fringe].index(high_priority) #Get the index where the highest priority lies in 

            curr_city_prty=fringe.pop(index_high_prty) # Pop the city with the highest priority 

            # print("The city with the highest priority that was popped {}".format(curr_city_prty))
            curr_city=curr_city_prty[0]
            curr_dist=curr_city_prty[1]
            curr_est_distance=curr_city_prty[2]
            curr_segments=curr_city_prty[3]
            time_taken=curr_city_prty[5]
            delivery_time=curr_city_prty[6]
            route_taken=curr_city_prty[7]
            
            # Check if the city that is popped out from the from fringe is the destination city, if it is tru then break out of the loop
            if curr_city==end:
                print("-------------------------*-------------------------You have reached your destination -------------------------*--------------------------")
                route_taken.pop(0)
                # print(route_taken)
                break
            
            #Adding the successors to the fringe 
            for next_city in road_segment[curr_city]:
                
                dist_travelled=curr_dist+float(next_city[1]) # This gives the distance travelled byb our driver to reach this particular city 
                segments=curr_segments+1
                time_travelled=time_taken + (float(next_city[1])/float(next_city[2])) # Distance divided by Speed Limit will give us the time taken

                 # Code to get delivery time 
                if float(next_city[2])<50:
                    del_time=delivery_time + (float(next_city[1])/float(next_city[2]))
                else:
                    del_time= delivery_time +(float(next_city[1])/float(next_city[2])) + (math.tanh(float(next_city[1])/1000 * 2 * (delivery_time + ((float(next_city[1])/float(next_city[2])) ))))

                # If a city's information is not avialble in the city-gps.txt, it difficult to evalute the estimated distance between the given city and the destination as we dont have any co-ordinates information
                               # If a city's information is not avialble in the city-gps.txt, it difficult to evalute the estimated distance between the given city and the destination as we dont have any co-ordinates information
                if next_city[0] not in city_gps.keys() and next_city[0] in road_segment.keys(): 
                    # print("-----",curr_city,"--------",next_city[0])
                    estimated_distance=curr_est_distance
              
                elif next_city[0] not in city_gps.keys() and next_city[0]  not in road_segment.keys(): 
                    continue
                else:
                    estimated_distance=estimated_dist(city_gps,next_city[0],end)

                # We wiil only add a city to the fringe if it is not already on the fringe
                if next_city[0] not in [x[0] for x in fringe]:

                    curr_route= [[next_city[0],"{} for {} miles".format(next_city[3],next_city[1])]] # Routr to move from the previous city to this city 

                    curr_route= route_taken+curr_route #Adding the rout from previous city to the current city to the route of that has info to recah from source to the prvious city. This will give us the entire route from source to destination

                    est_segments = estimated_distance / float(max_dist_seg)
                    fringe.append((next_city[0],dist_travelled,estimated_distance,segments,est_segments,time_travelled,del_time,curr_route)) # Append all the successor information to the fringe 
            
      # Counter to see the number of times the loop has run
            if count_2%1000==0:
                print(count_2)
            count_2+=1
        
    if cost=="time":
        #Add the fringe Data Structure
        curr_dist=0
        max_speed_seg= get_max_speed_segment()
       

        est_time= estimated_dist(city_gps,start,end) / float(max_speed_seg)
        est_dist=estimated_dist(city_gps,start,end)
        # Creating a list of tuples to store the route taken 
        route_taken=[[]]
        time_taken=0
        delivery_time=0
        fringe=[(start,curr_dist,est_dist,time_taken,est_time,delivery_time,route_taken)] # Adding the start city and the priority(f(s)= g(s)+h(s)) to the fringe

        while fringe:   

            high_priority= min([x[3]+x[4] for x in fringe]) # Get the city that has the highest priority (also means the city with the lowest heuristic distance)

            index_high_prty= [x[3]+x[4] for x in fringe].index(high_priority) #Get the index where the highest priority lies in 

            curr_city_prty=fringe.pop(index_high_prty) # Pop the city with the highest priority 

            # print("The city with the highest priority that was popped {}".format(curr_city_prty[0:4]))
            curr_city=curr_city_prty[0]
            curr_dist=curr_city_prty[1]
            curr_est_distance=curr_city_prty[2]
            time_taken=curr_city_prty[3]
            delivery_time=curr_city_prty[5]
            route_taken=curr_city_prty[6]
            
            # Check if the city that is popped out from the from fringe is the destination city, if it is tru then break out of the loop
            if curr_city==end:
                print("-------------------------*-------------------------You have reached your destination -------------------------*--------------------------")
                route_taken.pop(0)
                # print(route_taken)
                break
            
            #Adding the successors to the fringe 
            for next_city in road_segment[curr_city]:
                
                dist_travelled=curr_dist+float(next_city[1]) # This gives the distance travelled byb our driver to reach this particular city 

                time_travelled=time_taken + (float(next_city[1])/float(next_city[2])) # Distance divided by Speed Limit will give us the time taken

                # Code to get delivery time 
                if float(next_city[2])<50:
                    del_time=delivery_time + (float(next_city[1])/float(next_city[2]))
                else:
                    del_time= delivery_time +(float(next_city[1])/float(next_city[2])) + (math.tanh(float(next_city[1])/1000 * 2 * (delivery_time + ((float(next_city[1])/float(next_city[2])) ))))

                # If a city's information is not avialble in the city-gps.txt, it difficult to evalute the estimated distance between the given city and the destination as we dont have any co-ordinates information
                if next_city[0] not in city_gps.keys() and next_city[0] in road_segment.keys(): 
                    # print("-----",curr_city,"--------",next_city[0])
                    estimated_distance=curr_est_distance
              
                elif next_city[0] not in city_gps.keys() and next_city[0]  not in road_segment.keys(): 
                    continue
                else:
                    estimated_distance=estimated_dist(city_gps,next_city[0],end)

                # We wiil only add a city to the fringe if it is not already on the fringe
                if next_city[0] not in [x[0] for x in fringe]:

                    curr_route= [[next_city[0],"{} for {} miles".format(next_city[3],next_city[1])]] # Routr to move from the previous city to this city 

                    curr_route= route_taken+curr_route #Adding the rout from previous city to the current city to the route of that has info to recah from source to the prvious city. This will give us the entire route from source to destination

                    est_time = estimated_distance / float(max_speed_seg)
                    fringe.append((next_city[0],dist_travelled,estimated_distance,time_travelled,est_time,del_time,curr_route)) # Append all the successor information to the fringe 
            
      # Counter to see the number of times the loop has run
            if count_2%1000==0:
                print(count_2)
            count_2+=1

    if cost=="delivery":
        #Add the fringe Data Structure
        curr_dist=0
        max_speed_seg= get_max_speed_segment()
        est_time= estimated_dist(city_gps,start,end) / float(max_speed_seg)
        est_dist=estimated_dist(city_gps,start,end)
        # Creating a list of tuples to store the route taken 
        route_taken=[[]]
        time_taken=0
        delivery_time=0
        fringe=[(start,curr_dist,est_dist,time_taken,delivery_time,est_time,route_taken)] # Adding the start city and the priority(f(s)= g(s)+h(s)) to the fringe

        while fringe:   

            high_priority= min([x[4]+x[5] for x in fringe]) # Get the city that has the highest priority (also means the city with the lowest heuristic distance)

            index_high_prty= [x[4]+x[5] for x in fringe].index(high_priority) #Get the index where the highest priority lies in 

            curr_city_prty=fringe.pop(index_high_prty) # Pop the city with the highest priority 

            # print("The city with the highest priority that was popped {}".format(curr_city_prty[0:4]))
            curr_city=curr_city_prty[0]
            curr_dist=curr_city_prty[1]
            curr_est_distance=curr_city_prty[2]
            time_taken=curr_city_prty[3]
            delivery_time=curr_city_prty[4]
            route_taken=curr_city_prty[6]
            
            # Check if the city that is popped out from the from fringe is the destination city, if it is tru then break out of the loop
            if curr_city==end:
                print("-------------------------*-------------------------You have reached your destination -------------------------*--------------------------")
                route_taken.pop(0)
                # print(route_taken)
                break
            
            #Adding the successors to the fringe 
            for next_city in road_segment[curr_city]:
                
                dist_travelled=curr_dist+float(next_city[1]) # This gives the distance travelled byb our driver to reach this particular city 

                time_travelled=time_taken + (float(next_city[1])/float(next_city[2])) # Distance divided by Speed Limit will give us the time taken
                
                # Code to get delivery time 
                if float(next_city[2])<50:
                    del_time=delivery_time + (float(next_city[1])/float(next_city[2]))
                else:
                    del_time= delivery_time +(float(next_city[1])/float(next_city[2])) + (math.tanh(float(next_city[1])/1000 * 2 * (delivery_time + ((float(next_city[1])/float(next_city[2])) ))))

                # If a city's information is not avialble in the city-gps.txt, it difficult to evalute the estimated distance between the given city and the destination as we dont have any co-ordinates information
                if next_city[0] not in city_gps.keys() and next_city[0] in road_segment.keys(): 
                    # print("-----",curr_city,"--------",next_city[0])
                    estimated_distance=curr_est_distance
                elif next_city[0] not in city_gps.keys() and next_city[0]  not in road_segment.keys(): 
                    continue
                else:
                    estimated_distance=estimated_dist(city_gps,next_city[0],end)

                # We wiil only add a city to the fringe if it is not already on the fringe
                if next_city[0] not in [x[0] for x in fringe]:

                    curr_route= [[next_city[0],"{} for {} miles".format(next_city[3],next_city[1])]] # Routr to move from the previous city to this city 

                    curr_route= route_taken+curr_route #Adding the rout from previous city to the current city to the route of that has info to recah from source to the prvious city. This will give us the entire route from source to destination

                    est_time = estimated_distance / float(max_speed_seg)
                    fringe.append((next_city[0],dist_travelled,estimated_distance,time_travelled,del_time,est_time,curr_route)) # Append all the successor information to the fringe 
            
      # Counter to see the number of times the loop has run
            if count_2%1000==0:
                print(count_2)
            count_2+=1
            

    
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

    
    #Converting list of lists into list of tuples for the route taken (because our main function was designed to handle list of tuples)
    route_taken= [(x[0],x[1]) for x in route_taken]

    # print(route_taken)
    return {"total-segments" : len(route_taken), 
            "total-miles" : curr_dist, 
            "total-hours" : time_taken, 
            "total-delivery-hours" : delivery_time, 
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


