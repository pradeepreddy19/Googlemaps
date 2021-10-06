#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import time
import numpy as np


#Cost functions
def grading(groups):
    n_groups = len(groups)
    
    return n_groups*5


def wrong_group_size(group_assigned, want_group_size, groups_size):

    assigned_group_size=[groups_size[group] for group in group_assigned]
    group_size_compare = [assigned_group_size[n]==want_group_size[n] for n in range(len(group_assigned))]
    n_wrong_groups = len(group_assigned) - np.count_nonzero(group_size_compare)
    
    return n_wrong_groups*2



def wanted_not_in_assigned(people_assigned, want):

    people_assigned_mask = people_assigned.copy()
    for n, row in enumerate(want):
        for m, item in enumerate(row):
            if item in ['xxx','zzz']:
                people_assigned_mask[n] = people_assigned_mask[n]+['xxx','zzz']

    match_wanted_assigned = [[want[i][n] in people_assigned_mask[i] for n in range(len(want[i]))] for i in range(len(people_assigned))]
    match_wanted_assigned = [elem for row in match_wanted_assigned for elem in row]
    
    wanted_not_assigned = len(match_wanted_assigned)- np.count_nonzero(match_wanted_assigned)
    
    return wanted_not_assigned *(0.05*60)


def not_wanted_in_assigned(people_assigned, not_want):    
    match_not_want_assigned = [[not_want[i][n] in people_assigned[i] for n in range(len(not_want[i]))] for i in range(len(people_assigned))]
    match_not_want_assigned = [elem for row in match_not_want_assigned for elem in row]
    not_want_assigned = np.count_nonzero(match_not_want_assigned)

    return not_want_assigned*10




#assign preferred groups, then random after that

def top_down_pref(people, want):
    picked_groups = []
    avail_people = list(people.copy())
    #     print(f'want {want}\n')



    for n in range(len(want)):
        try:
            grp = []
            for m in range (len(want[n])):
                if want[n][m] in avail_people:
    #                     print(f'{want[n][m]} available')
                    grp.append(want[n][m])
    #                     print(f'grp {grp}')
                    avail_people.remove(want[n][m])
    #                     print(f'avail_people {avail_people}')

                if want[n][m] in ['xxx','zzz']:
    #                     print(f'{want[n][m]} is wildcard')
                    rand_avail = np.random.choice(avail_people, 1)[0]
                    grp.append(rand_avail)
    #                     print(f'grp {grp}')
                    avail_people.remove(rand_avail)
    #                     print(f'avail_people {avail_people}')

            picked_groups.append(grp)
    #             print(f'picked_groups {picked_groups}\n')
        except:
            continue

    picked_groups = [x for x in picked_groups if x!= []]
    # print (f'picked_groups {picked_groups}')


    picked_people = [item for sublist in picked_groups for item in sublist]
    # print(f'picked_people {picked_people}')

    people_left = list(people.copy())
    [people_left.remove(picked_people[n]) for n in range(len(picked_people))]
    # print(f'people_left {people_left}')


    if people_left != []:
        picked_groups.append(people_left)
    #     print(f'picked groups {picked_groups}')



    n_group_check = [len(grp) for grp in picked_groups]
    # print(f'n_group_check {n_group_check}')
    if max(n_group_check)>3:
        group_to_split_idx = [n_group_check.index(x) for x in n_group_check if x>3][0]
    #     print(f'group_to_split_idx {group_to_split_idx}')
        group_to_split = picked_groups.pop(group_to_split_idx)
        n =3
        [picked_groups.append(group_to_split[i*n:(i+1)*n]) for i in range((len(group_to_split)+n-1)//n)]
#         print(f'picked_groups {picked_groups}')

    return picked_groups


#check 100 samples then shuffle list and repeat.
#yield when lower cost group is found

def solver(input_file):
    with open(input_file) as f:
        lines = f.readlines()
    
    survey_text = [line.rstrip('\n') for line in lines]
    survey_data = np.array([entry.split() for entry in survey_text])


    min_cost = 100000000
    while min_cost >0:
  
        np.random.shuffle(survey_data)

        #survey inputs
        people = survey_data[:,0]
        want = [item.split('-') for item in survey_data[:,1]]
        not_want = [item.split(',') for item in survey_data[:,2]]
        want_group_size = [len(item) for item in want]

        # print(f'\npeople {people}')

        runs = 100
        for n in range(runs):
            groups = top_down_pref(people, want)
            # print(f'groups {groups}')

            # group stats
            n_groups = len(groups)
            
            groups_size = [len(group) for group in groups]

            people_group_mat = [[people[x] in group for group in groups] for x in range(len(people))]
            group_assigned = [people_group_mat[n].index(1) for n in range(len(people_group_mat))]
            people_assigned =[groups[n] for n in group_assigned]

            #calculate cost
            cost_grading = grading(groups)
            cost_wrong_group_size = wrong_group_size(group_assigned, want_group_size, groups_size)
            cost_wanted_not_in_group = wanted_not_in_assigned(people_assigned, want)
            cost_not_wanted_in_group = not_wanted_in_assigned(people_assigned, not_want)

            cost = cost_grading + cost_wrong_group_size + cost_wanted_not_in_group + cost_not_wanted_in_group

            if cost < min_cost:
                min_cost_groups = groups
                min_cost = cost
    #                 print(n, min_cost_groups, min_cost)

                min_cost_groups_str = ['-'.join(x) for x in min_cost_groups]
                # print (f'min_cost_group after {runs} random samples is {min_cost_groups_str, min_cost}')

                result = {"assigned-groups": min_cost_groups_str,
                        "total-cost" : min_cost}
                
                yield(result)
                
                

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
