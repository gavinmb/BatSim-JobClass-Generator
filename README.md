## BatSim Job Workload Generator

This program takes in an input JSON file of Job Class types and coverts it to a BatSim JSON workload file that can be run with BatSim. Execution times are normally distributed and submit times are exponentially distributed.
The input JSON must be of this format:

```json
{
   "Class A":[
      {
         "num_nodes":1,
         "Average_execution_time":120,
         "SD_execution_time":10,
         "Percentage_of_workload":0.3
      }
   ],
   "Class B":[
      {
         "num_nodes":2,
         "Average_execution_time":3600,
         "SD_execution_time":500,
         "Percentage_of_workload":0.2
      }
   ],
}
```

All profiles are set up with the BatSim delay profile (the following configuration):

```json
  "type": "delay",
  "delay": (execution time)
```

## Usage

job_generator.py

Usage: -j <job count> -b <scale parameter> [-r <total resources>] -i <input file name> -o <output file name>

* -j The total number of jobs
* -b The scale parameter (beta) of the exponentially distributed submit times
* -r [optional] The total number of resources (defaults to max of num_nodes from Classes)
* -i The input job class JSON file
* -o The output BatSim JSON file (must have JSON extension)

Use -h for help at the command line
