from pysmt.shortcuts import Symbol, And, Not, GE, Plus, Times, Int, get_model, Ite, Iff
from pysmt.typing import INT
import os
import time
import sys


robots_info = {}
task_info = {}
task_utilities = {}
k=0


def solveDecisionProblem(filename):
	global robots_info
	global task_info
	global task_utilities
	global k
	robots_info = {}
	task_info = {}
	task_utilities = {}
	k=0

	file = open(filename, "r")
	mode = 0
	for line in file:
		if line=='\n':
			mode+=1
		elif mode==0:
			k = int(line.strip())
		elif mode==1:
			task_line = line.split()
			task_info[task_line[0]] = [int(resource) for resource in task_line[2:]]
			task_utilities[task_line[0]] = int(task_line[1])
		elif mode == 2:
			robot_line = line.split()
			robots_info[robot_line[0]] = [int(resource) for resource in robot_line[1:]]
	file.close()
		

	# Each robot may be assigned to at most one task
	# runs in time |Robots||Tasks||Tasks|
	oneTask = And([Symbol(robot+taskAssigned).Implies(Not(Symbol(robot+task))) for robot in robots_info.keys() for taskAssigned in task_info.keys() for task in task_info.keys() if (taskAssigned != task)])

	# A task is satisfied if and only if all of its resource requirements are met
	# runs in time |Robots||Tasks||ResourceTypes|
	tasksSatisfied = And([Iff(Symbol(task +"Sat"), And([GE(Plus([Times(Ite(Symbol(robot+task),Int(1), Int(0)), Int(robots_info[robot][i])) for robot in robots_info.keys()]), Int(task_info[task][i])) for i in range(len(task_info[task]))])) for task in task_info.keys()])

	# Is the decision problem satisfied
	# runs in time |Tasks|
	decisionProb = GE(Plus([Times(Ite(Symbol(task+"Sat"), Int(1), Int(0)), Int(task_utilities[task])) for task in task_info.keys()]), Int(k))

	prob = And(oneTask, tasksSatisfied, decisionProb)
	model = get_model(prob)
	return model


def printOutput(model, outfile):
	# format and print output
	file = open(outfile, "w")
	if model == None:
		file.write("0\n")
		file.close()
		return
	total = model.get_py_value(Plus([Times(Ite(Symbol(task+"Sat"), Int(1), Int(0)), Int(task_utilities[task])) for task in task_info.keys()]))
	file.write(str(total)+"\n\n")
	for task in task_info.keys():
		if (model.get_py_value(Symbol(task+"Sat"))):
			ret = task + " " + str(task_utilities[task])
			for robot in robots_info.keys():
				if (model.get_py_value(Symbol(robot+task))):
					ret+= " " + robot
			ret+="\n"
			file.write(ret)
		else:
			file.write(task +" 0\n")
	file.close()



def runExperiment(folder, outfile):
	file = open(outfile, "w")
	for filename in os.listdir(folder):
		print("starting: " + filename)
		model = None
		start = time.clock()
		model=solveDecisionProblem(os.path.join(folder,filename))
		end = time.clock()
		if (model == None):
			file.write(filename + " " + str(end-start) + " " + str(0) +"\n")
		else:
			file.write(filename + " " + str(end-start) + " " + str(model.get_py_value(Plus([Times(Ite(Symbol(task+"Sat"), Int(1), Int(0)), Int(task_utilities[task])) for task in task_info.keys()]))) +"\n")

		print(filename + " " + str(end-start))
		
	file.close()
	

if __name__ == "__main__":
	arg = sys.argv
	if arg[1] == "-e":
		folder = arg[2]
		outfile = arg[3]
		runExperiment(folder, outfile)
	else:
		file = arg[1]
		outfile = arg[2]
		model = solveDecisionProblem(file)
		printOutput(model, outfile)





