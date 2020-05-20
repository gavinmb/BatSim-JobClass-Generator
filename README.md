## BatSim Job Workload Generator

This program takes in an input JSON file of Job Class types and coverts it to a BatSim JSON workload file that can be run with BatSim. Wall-clock times are normally distributed and submit times are exponentially distributed.
The input JSON must be of this format:

```json
{
  "Class A": [
  {
    "num_nodes": 1,
    "Average_wallclock_time": 120,
    "SD_wallclock_time": 10,
    "Percentage_of_workload": 0.3
	}
],
  "Class B": [
  {
    "num_nodes": 2,
    "Average_wallclock_time": 3600,
    "SD_wallclock_time": 500,
    "Percentage_of_workload": 0.2
  }
]
```

All profiles are set up with the following configuration:

```json
  "type": "parallel_homogeneous",
  "cpu": 50e10,
  "com": 0
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
