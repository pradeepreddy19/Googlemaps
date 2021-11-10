import pandas as pd
#For Grading A1
def pytest_sessionfinish(session, exitstatus):
	anum=0
	qnums=1
	casenums=5
	reporter = session.config.pluginmanager.get_plugin('terminalreporter')
	report={}
	points={'test_puzzle_2021_case1':10,'test_puzzle_2021_case2':10,'test_puzzle_2021_case3':10, 'test_puzzle_2021_case4':10, 'test_puzzle_2021_case5':10}
	total=0
	try:
		for test in reporter.stats['passed']:
			report[test.location[2]+"_status"]=[test.outcome]
			report[test.location[2]+"_points"]=[points[test.location[2]]]
			total+=points[test.location[2]]
	except KeyError:
		pass
	try:
		for test in reporter.stats['failed']:
			report[test.location[2]+"_status"]=[test.outcome]
			report[test.location[2]+"_points"]=[0]
	except KeyError:
		pass
	report=pd.DataFrame.from_dict(report)
	report.sort_index(axis=1, inplace=True)
	report['Part1_Total']=[total]
	report.T.to_csv("autograding_report1.csv",header=False)