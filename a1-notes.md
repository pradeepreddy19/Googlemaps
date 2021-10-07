# CSB551 - Assignment 1:  Searching
Fall 2021 October 8, 2021
Pradeep Rokkam, Joy Zayatz

[link to google doc version](https://docs.google.com/document/d/1M894JdJTCfkp1vTF8Db_MiFHWmYv2sLi0xKOMlqHuVk/edit?usp=sharing)



## Part 1:  The 2021 Puzzle
Objective.  Use A* search to find sequence of moves that gets puzzle back in order.   
(baseline:  solve board1.txt in 11 moves found in less than 15 mins)

__Question 1:__ What is the branching factor of the search tree?  
24?  (5+5+2) axes of motion * 2 directions each

__Question 2:__ If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A* search?  (a rough answer is fine)

__Formulating the search problem__ 
* abstraction
    * state space
    * successor function
    * edge weights
    * goal state
    * heuristic functions (admissible? consistent? accurate? easy to compute?)  
* data structures

__How search algorithm works__  


__Discussion__
* challenges 
* assumptions
* simplifications
*  decisions made



## Part 2:  Road Trip!!!

Objective:  use A* search to find driving directions between two cities and cost function given by the user.  
Bonus points for finding shortest route that passes through at least one city in each 48 contiguous states.



__Formulating the search problem__ 
* abstraction
    * state space
    * successor function
    * edge weights
    * goal state
    * heuristic functions (admissible? consistent? accurate? easy to compute?)  
* data structures

__How search algorithm works__  


__Discussion__
* challenges 
* assumptions
* simplifications
*  decisions made

Please read the simplification in the discussion segment for the sake of better comprehension

__Formulating the search problem__ 
* **_Abstraction_**
    * **State Space:** All possible towns/cities that our driver can navigate to 
    * **Successor function** For a given city that our driver is currently located at, the successor function will give all the possible next cities that our driver can be travel to
    * **Cost function:** Sum of all the edge costs and it varies for the given cost function:
       * _Distance:_ Sum of the **distances** of all roads that were travelled from source city to destination city
       * _Segments:_ Sum of **number of towns/cities** that were travelled from source city to destination city
       * _Time:_ Sum of **time taken to travel** of all roads that were travelled from source city to destination city
       * _Delivery Time:_ Sum of **time taken to travel (from delivery standpoint)** of all roads that were travelled from source city to destination city
      * As discussed above edge weights vary based on the cost function.
         * For eg: Two routes may have same distance in miles between them, however one route is faster than the other from time standpoint may be because that particular route has higher speed limit than the other
    * **Goal state:** Our goal state is the destination city our driver wants to navigate to
    * **Heuristic functions:** : Just like cost function our heuristic function changes based on the specified cost function
      * _Distance:_ The heuristic function between a given city and the destination is distance given by the Haversine formula by making use lattitudes and longitudes of the source and destination. It is an admissible function as the estimate is always lesser than or equal to the true distance 
         * The haversine formula is as follows:
         *  Please read the simplification in the discussion segment for the sake of better comprehension

__Formulating the search problem__ 
* abstraction
    * state space:
All possible towns/cities that our pichu can navigate to 
    * successor function
For a given city that our pichu is currently located at, the successor function will give all the possible next cities that our pichu can be placed at:
    * edge weights
Edge weights vary based on the cost function.
For eg: Two routes may have same distance in miles between them, however one route is faster than the other from time standpoint may be because that particular route has higher speed limit than the other
    * goal state:
Our goal state is the our destination city our pichu wants to navigate to
    * heuristic functions (admissible? consistent? accurate? easy to compute?) :
I think based on cost functions our heuristic function changes. Assuming that we came up with the heuristics functions for each of these cost functions, we need to verify that is the heuristic function easy to compute? Or Is it admissible?
Heuristic function based on the distance. To implement this we need to use the Haversine Formula as followed



If we change R(radius of the earth) into miles we get our answer in miles 

* data structures
We will be using the priority queue here as this gives the functionality of the A* search 
__How search algorithm works__  


__Discussion__
* challenges:
I don’t see any difference between the cost function “time” and “delivery”. Why would our pichu/driver travels more than the speed limit of the given highway
* assumptions:
* simplifications:
For the sake of simplicity and discussion purpose,let's think that we are helping pichu to navigate from the source city/town to the destination city/town in the shortest possible criteria our pichu desires ( segments,distance,time, delivery and if possible statetour)
I think we can take inspiration from the route pichu problem in the Assignment 0. I see a lot of similarities between that problem and this particular problem
*  decisions made:


       * _Segments:_ Sum of **number of towns/cities** that were travelled from source city to destination city
       * _Time:_ Sum of **time taken to travel** of all roads that were travelled from source city to destination city
       * _Delivery Time:_ Sum of **time taken to travel (from delivery standpoint)** of all roads that were travelled from source city to destination city
      * As discussed above edge weights vary based on the cost function.

Heuristic function based on the distance. To implement this we need to use the Haversine Formula as followed



If we change R(radius of the earth) into miles we get our answer in miles 

* data structures
We will be using the priority queue here as this gives the functionality of the A* search 
__How search algorithm works__  


__Discussion__
* challenges:
I don’t see any difference between the cost function “time” and “delivery”. Why would our pichu/driver travels more than the speed limit of the given highway
* assumptions:
* simplifications:
For the sake of simplicity and discussion purpose,let's think that we are helping pichu to navigate from the source city/town to the destination city/town in the shortest possible criteria our pichu desires ( segments,distance,time, delivery and if possible statetour)
I think we can take inspiration from the route pichu problem in the Assignment 0. I see a lot of similarities between that problem and this particular problem
*  decisions made:






## Part 3:  Choosing Teams

Objective:  Assign students to teams that minimizes total amount of work for instructors
Multiple solutions allowed.  program can start with an approximate answer while continuing to look for better ones



__Formulating the search problem__ 
* abstraction
    * state space
    * successor function
    * edge weights
    * goal state
    * heuristic functions (admissible? consistent? accurate? easy to compute?)  
* data structures

__How search algorithm works__  


__Discussion__
* challenges 
* assumptions
* simplifications
*  decisions made
