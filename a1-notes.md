# CSB551 - Assignment 1:  Searching
Fall 2021 October 8, 2021
Pradeep Rokkam, Joy Zayatz

[link to google doc version](https://docs.google.com/document/d/1M894JdJTCfkp1vTF8Db_MiFHWmYv2sLi0xKOMlqHuVk/edit?usp=sharing)



## Part 1:  The 2021 Puzzle
Objective.  Use A* search to find a sequence of moves that gets the puzzle back in order.   

__Question 1:__ What is the branching factor of the search tree?  
The branching factor (b) is the number of successors from a given state.  For this game, every move is possible from any board configuration, so b = 24.  (5 row moves + 5 column moves + 1 outer ring move + 1 inner ring move) * 2 directions for each move.


__Question 2:__ If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A* search?  (a rough answer is fine)  
Because breadth first search explores every state before going deeper into the graph, worst case scenario, If the solution has a depth (d), BFS would explore $b^{d}$ states to find the solution,  which in this case is $24^{7} \approx 2\times 10^{20}$ states.

__Formulating the search problem__   
Abstraction
* state space:  The state space is all possible configurations of the 5 X 5 board. Numbers 1 through 25 are arranged one number per space.  
* initial state: The initial state is a randomly generated board configuration.
* successor function:  The successor function generates 24 possible successor states from any given state that represent each of the possible moves: L1, L2, L3, L4, L5, R1, R2, R3, R4, R5, U1, U2, U3, U4, U5, D1, D2, D3, D4, D5, Oc, Occ, Ic, Icc.  The successor function returns both the board configuration and the move to get there from the parent state.
* edge weights: The cost of moves is uniform so each move will be counted as one.  
* goal state.  There is a single goal state: where the numbers are arranged in sequential order with 1 in the upper left corner and 15 in the lower right corner.
* heuristic functions:  For A* search to be complete and optimal, the heuristic function used always has to underestimate the cost to reaching the goal. The heuristic function used here counts the number of tiles that are not in the correct row or not in the correct column and divides by 5 (number of tiles changed in each row/column move).  

Data structures:  fringe states and visited states are numpy arrays that contain for each state: the board configuration, cost to get to that board configuration from the start state (g), the last move to reach the board configuration, and the estimated cost to reach the goal (f = g+h). 


__How search algorithm works__  
A-star search uses best first search to find a goal state from a start state that minimizes the path between the two states.  This is implemented with a fringe that contains a priority queue where states are stored with an associated f value. The algorithm looks through the fringe for the state with the lowest f value to explore next.  f is the sum of g and h (cost current state and predicted cost to reach goal state).  The steps are as follows:
1. given an initial state, check if initial state is goal state.  
2.  if the initial state is not the goal state, add the initial state to the fringe.  In this setup, we’re assuming that we are given a board that needs solving so the initial board is directly added to the fringe with a g value of 0, ‘starting point’ as previous move, and an f value of 0.
3.  Remove the item from the fringe that has the lowest value of f.  If there is more than one state that has the same value of f, one of those states is chosen at random.
4.  Find the successors that that state
5.  For each successor:
	* Check if successor is the goal state.  If it is, trace back the optimal path and return it.
	* If it is not the goal state, calculate h, add to g+1 to get f and add that state to the fringe.  
6. Repeat steps 3, 4, and 5  until the goal state is found, or there are no more items in the fringe.

__Discussion__
Challenges:  The branching factor for the problem is very high.  There are always 24 valid successors for any given state.  This is a challenge for the search because the number of states grows so quickly.  The longer the search goes on, the more memory is consumed by storing the fringe and list of visited states which makes the search slow down dramatically.  

Simplifications:  To find an admissible heuristic, we simplified the goal state to be just the tile in the correct row and column, but don’t have to be in sequence.

 Decisions made
* Compared to search algorithm 3 (which also requires a consistent heuristic function),  using search algorithm 2 with an admissible heuristic ran much faster because each successor is not compared to every element in the fringe and visited lists before adding it to the finge .  However, it will repeatedly go back to visited states.
* To decrease the number of revisited states, states that share the lowest f value in the fringe are chosen at random to be removed from the fringe.



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
         * ![image](https://media.github.iu.edu/user/18258/files/769b9100-2701-11ec-8fe5-dac1c8f944cf)
            * If we change R(radius of the earth) into miles we get our answer in miles 
      * _Segments:_ Estimated distance given by Haversine formula / Maximum distance between two segments in miles in the entire map . This is also an admissible function
      * _Time:_ Estimated distance given by Haversine formula / Maximum speed between two segments in miles per hour(mph) in the entire map . This is also an admissible function
      * _Delivery Time:_  We can use the same heuristic as the Time here as time is the best case scenario of delivery time. So the heuristic function would be Estimated distance given by Haversine formula / Maximum speed between two segments in miles per hour(mph) in the entire map . This is also an admissible function

   * **Data structures** :We used a priority queue (priority f(s) = g(s)+h(s)) as the data structure which gives the functionality of the A* search 

__How search algorithm works__  
A-star search uses best first search to find a goal state from a start state that minimizes the path between the two states.  This is implemented with a fringe that contains a priority queue where states are stored with an associated f value. The algorithm looks through the fringe for the state with the lowest f value to explore next.  f is the sum of g and h (cost current state and predicted cost to reach goal state).  The steps are as follows:
1. given an initial state, check if initial state is goal state.  
2. if the initial state is not the goal state, add the initial state to the fringe.  In this setup, we’re assuming that we are given a with a start city and our driver wants to navigate to the destination city based on the given cost function 
3.  Remove the city from the fringe that has the lowest value of f.  If there is more than one city that has the same value of f, one of those cities is chosen at random.
4.  Check the city that is removed from the fringe is a destination city or not. If yes return the path. If not:
6.  Find the successors for the city and add them to the fringe 

__Discussion__
_Challenges:_ 
1. As most AI problems we have the problem of exploring huge number of states. Our branching factor varies based on the number of successer cities between two cities. When theis is combine depth we will end up with the huge number of states. This is a challenge for the search because the number of states grows so quickly. The longer the search goes on, the more memory is consumed by storing the fringe and list of visited states which makes the search slow down dramatically. 
	* This is when A.* come in handy 
2. Second problem is the that lack of information for few segments, it is difficult to estimate the hueristic distacne between two cities if we dont have information about the lattitudes and longitudes
	* To take care of this what we have done is  we took its predecessor estimated distance - the distance of the road segment between source predecessor city and current city
	* However,this may fail sometimes 


Simplifications:  To find an admissible heuristic, we assumed that the distance between between any two cities is the least possible distance 

 Decisions made
* Compared to search algorithm 3 (which also requires a consistent heuristic function),  using search algorithm 2 with an admissible heuristic ran much faster because each successor is not compared to every element in the fringe and visited lists before adding it to the finge .  However, it will repeatedly go back to visited states.
* To decrease the number of revisited states, states that share the lowest f value in the fringe are chosen at random to be removed from the fringe.


## Part 3:  Choosing Teams

Objective:  Assign students to teams that minimizes total amount of work for instructors
Multiple solutions allowed.  Solution can start with an approximate answer while continuing to look for better ones

__Formulating the search problem__  
Abstraction
* state space:  All possible groupings of students who submitted a survey where all students are assigned a group and groups contain either 1, 2, or 3 people.
* start state:  The start state for each local search area is a grouping of students where teams are assigned as much as possible based on preference going in order of the survey from top to bottom, and remaining students are assigned at random.
* successor function:  The successors of each state (area of each local search) are 100 states chosen by the method described above to generate the start state.  
* cost function: the cost for each state is the total time (in minutes) required by the instructors to grade the assignments submitted by each group and deal with various tasks associated with students not getting their preferred teammates, group size, or having to work with someone they don’t want work with.  
* goal state:  The goal state is the grouping of students that has the lowest cost.  In terms of optimization, this goal state is the global minimum of the state space.  

Data structures:  The survey data is initially stored as a numpy array and then sliced and stored as lists.  Group assignments and cost calculations were completed with either numpy or list operations.

__How search algorithm works__  
This problem was framed as a local search problem where given a list of students and their preferences, each student is assigned their desired group starting from the top of the list and moving down.  If a person indicates ‘zzz’ or ‘xxx’ they are assigned a random available person.  If a student’s entire preferred group can not be met, they are skipped.  After assigning groups by preference from the top of the list to the bottom, remaining students are assigned to groups of 3.  There may be a group of 2 or 1  if the number of remaining students is not evenly divisible by 3.  After all students are assigned the cost of that state of groupings is calculated and compared to the minimum cost of all groupings so far.  The grouping and cost of the lower is kept.  This process is repeated 100 times.  After 100 times, the survey data is shuffled and the above process is repeated.  The search is completed after the survey data is shuffled 1000 times.  


__Discussion__
* Challenges: Identifying a way to find the direction of a lower cost group given the group you already have was difficult.  It was difficult to predict how making a change for one person affects the total cost of that set of teams.  
* Assumptions:  In isolation, the most costly group is one where a person is assigned to work with someone that they expressly do not want to work with. But starting from this basis to assign groups was challenging so, based on the small test cases, we noticed that there were not many potential conflicts where a one person wanted to work with someone that doesn’t want to work with them.  Also, it seems that more people have stated preferences for groups rather than requests not to work with certain people.  
*  Decisions made:  We decided to use a semi-random search to give each the start of each search location that has been at least optimized slightly, and also decrease the number of possible neighbors for a given start state.  Given the survey sizes, 100 random samples covers a significant set of possible successors from each start state.  Shuffling the survey data 1000 is a way to randomly move the start of the local search to a new location.  This exposes the search to 100,000 states.  To save memory, we are not saving visited states, so states can be revisited repeatedly.  However, the randomness of the search parameters, and not keeping track of searched states should help search through more states to compensate.

