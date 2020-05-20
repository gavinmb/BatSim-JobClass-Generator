import sys
import argparse
import json
import random
import string
import math
import numpy as np

alphabets = string.ascii_uppercase

numOfJobs = None
inputFileName = None
outputFileName = None

parser = argparse.ArgumentParser(usage='-j <job count> -b <scale parameter> [-r <total resources>] -i <input file name> -o <output file name> \n\nUse -h for help at the command line', description="Arguments for BatSim JSON generation")
parser.add_argument('-j', required="True", dest='numOfJobs', type=int, help='Total job count of the workload')
parser.add_argument('-b', required="True", dest='scaleParam', type=int, help='Scale parameter (beta) of the exponentially distributed submit times')
parser.add_argument('-r', dest='nbRes', type=int, default=0, help="Total number of resources [optional]")
parser.add_argument('-i', required="True", dest='inputFileName', type=str, help='Input file name (Job class JSON file)')
parser.add_argument('-o', required="True", dest='outputFileName', type=str, help='Output file name (must have JSON extension)')

args = parser.parse_args()

numOfJobs = args.numOfJobs
inputFileName = args.inputFileName
outputFileName = args.outputFileName
scaleParam = args.scaleParam
nbRes = args.nbRes

try:
    with open(inputFileName) as file:
        data = json.load(file)
except:
    print("Input file not found")
    sys.exit(0)

jobClasses = alphabets[:len(data)]

# default nb_res will equal the max required resources of a class if none is supplied
nodes = []
maxNodes = 0
for x in jobClasses:
    nodes.append(data["Class {}".format(x)][0]['num_nodes'])
if (nbRes == 0):
    nbRes = max(nodes)
elif (nbRes < max(nodes)):
    print("WARNING: the total number of resources supplied is less than what some of the job classes require. Therefore, some jobs may fail to run.")


# Calculate the number of jobs for each class percentage
# Accounts for job count round errors
classJobs = [] # the number of jobs of each class
excess = []
for x in jobClasses:
    percentage = (data["Class {}".format(x)][0]['Percentage_of_workload'])
    mainNum = (percentage * numOfJobs)
    decimalNum = (mainNum % 1)
    mainNum = math.floor(mainNum)
    classJobs.append(mainNum)
    excess.append(decimalNum)
while (sum(classJobs) != numOfJobs):
    ind = excess.index(max(excess))
    classJobs[ind] = classJobs[ind] + 1
    excess[ind] = 0

# dictionary of jobs and profiles
# creates according to each class (wallclock, number of nodes)
profiles = {}
jobs = []
classJobsIndex = 0
profileIndex = 1
for ind, val in enumerate(jobClasses):
    nodes = (data["Class {}".format(val)][0]['num_nodes'])
    mean = (data["Class {}".format(val)][0]['Average_wallclock_time'])
    SD = (data["Class {}".format(val)][0]['SD_wallclock_time'])
    for y in range(0, classJobs[classJobsIndex]):
        wallclock = np.random.normal(mean, SD)
        j = {
            "id": "",
            "profile": "Profile{}{}".format(val, profileIndex),
            "res": nodes,
            "subtime": "",
            # "walltime": round(wallclock)
            }
        p = {
            "Profile{}{}".format(val, profileIndex): {
            "type": "delay",
            "delay": round(wallclock),
            }
        }
        profiles.update(p)
        jobs.append(j)
        profileIndex = profileIndex + 1
    classJobsIndex = classJobsIndex + 1
random.shuffle(jobs)

# assign job id and submit time
totalJobs = 1
sTime = 0
for job in jobs:
    job['id'] = totalJobs
    job['subtime'] = sTime
    totalJobs = totalJobs + 1
    sTime = sTime + round(np.random.exponential(scaleParam))


# final workload dictionary (nested)
workload = {
    "description": "Workload from Class JSON",
    "nb_res": nbRes,
    "jobs": [
    ],
    "profiles": {
    }
}

# attach profiles and jobs to workload dictionary
workload['profiles'] = profiles
workload['jobs'] = jobs

# dump to JSON
with open(outputFileName, 'w') as fp:
    json.dump(workload, fp, indent = 5)
