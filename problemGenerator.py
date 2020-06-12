import os
import random

r_low = 5
r_high = 30
r_interval = 5
task_low = 5
task_high = 5
task_interval = 1
resource_low = 3
resource_high = 3
trials = 20

outFolder = "ToC_problems"

if not os.path.exists(outFolder):
	os.makedirs(outFolder)
for a in range(r_low, r_high+1, r_interval):
	for t in range(task_low, task_high+1, task_interval):
		for r in range(resource_low, resource_high+1):
			for i in range(trials):
				file = open(os.path.join(outFolder, str(a)+"A"+str(t)+"T"+str(r) + "R" + str(i)+".txt"), "w")
				tasks = {}
				task_utilities = {}
				robots = {}
				for j in range(t):
					j_resources  = [0 for l in range(1, r+1)]
					while (sum(j_resources)==0):
						j_resources = [random.randrange(0, 6) for x in j_resources]
					j_resources = [str(x) for x in j_resources]
					tasks["t"+str(j)] = j_resources
					task_utilities["t"+str(j)] = random.randrange(1, 20)
				for j in range(a):
					j_resources  = [0 for l in range(1, r+1)]
					while sum(j_resources)==0:
						j_resources = [random.randrange(0, 5) for x in j_resources]
					j_resources = [str(x) for x in j_resources]
					robots["r"+str(j)] = j_resources

				k = random.randrange(1, sum(task_utilities.values()))
				file.write(str(k)+"\n\n")
				for task in tasks.keys():
					file.write(task + " " + str(task_utilities[task]) + " " + " ".join(tasks[task]) + "\n")
				file.write("\n")
				for robot in robots.keys():
					file.write(robot + " "  + " ".join(robots[robot]) + "\n")


				file.close()
