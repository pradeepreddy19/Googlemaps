'''test_choose_team.py
Usage: 
python3 test_choose_team.py user1-user2-user3-a1/part3
It is not always possible to get the best solution so we will check whether the solution is below a threshold in order to pass the test case.
For final grading we will be using more complex test cases.
'''
import pytest
import assign
import signal
time_ = 100

def handler(signum, frame):
	raise Exception("timeout")


def get_solution(test_file):
	results = [[]]
	try:
		for i in assign.solver(test_file):
			results.append([list(i['assigned-groups']), i['total-cost']])
	except Exception:
		return results
	return results


def check_names(test_file,result):
	names_ = [j for i in [i.split('-') for i in result[0]] for j in i]
	names = set(names_)
	with  open(test_file,'r') as f:
		original_names = set()
		for i in f.readlines():
			original_names.add(i.split()[0])
	return (original_names==names and len(names)==len(original_names))


def check_solution(test_file,result,threshold = float('inf')):
	assert len(result) != 0, "No solution yielded in {} seconds".format(str(time_))
	assert result[1] >= 0, "Score cannot be negative" 
	assert check_names(test_file,result) == True, 'Everyone should be assigned to a team'
	assert type(result[1]) in (int,float), 'Cost should be of type int or float'
	
	# using calculated score rather than their score
	survey = load_survey(test_file)
	score = get_cost(survey, result[0])

	assert score <= threshold, 'The cost of the group assignments was not optimal enough'


def load_survey(test_file):
    with open(test_file, 'r') as f:
        survey = {key[0]: (key[1].split('-'), key[2].split(',') if key[2] != '_' else [])
                  for key in [line.strip().split(' ') for line in f]}

    return survey


def get_cost(survey, result):
    # 5 minutes per team
    cost = 5 * len(result)
    print(survey)
    for team in result:
        people = team.split('-')

        for i, p in enumerate(people):
            # 2 minutes for each person who is placed in a different sized group then they asked
            cost += 2 if len(survey[p][0]) != len(people) else 0

            # 0.05 * 60 minutes (3 minutes) for each person who is not assigned someone they requested to work with
            cost += sum(3 for r in [requested for requested in survey[p][0] if requested not in ('zzz', 'xxx') and requested != p]
                        if r not in (people[:i] + people[i + 1:]))

            # 10 minutes for each person who is assigned to work with someone they requested not to work with
            cost += sum(10 for other in (people[:i] + people[i + 1:]) if other in survey[p][1])

    return cost


def test_p3_case_1():
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(time_)
	test_file = 'test1.txt'
	check_solution(test_file,get_solution(test_file)[-1],30) 

def test_p3_case_2():
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(time_)
	test_file = 'test2.txt'
	check_solution(test_file,get_solution(test_file)[-1],50) 

def test_p3_case_3():
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(time_)
	test_file = 'test3.txt'
	check_solution(test_file,get_solution(test_file)[-1], 90)

def test_p3_case_4():
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(time_)
	test_file = 'test4.txt'
	check_solution(test_file,get_solution(test_file)[-1], 80)

def test_p3_case_5():
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(60)
	test_file = 'test5.txt'
	check_solution(test_file,get_solution(test_file)[-1], 10)
