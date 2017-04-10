## Environment

1. Python 3.6.1
2. pandas 0.19.2

## Approach
* Reading the **_log.txt_** file  
 * Locate the **_log.txt_** file by Relative Path
 * read the **_log_** file as CSV file
 * Chose and assign names for each column
 
* Feature 1  
Count the Host with the **_value\_counts()_** function

* Feature 2  
 * Convert the Bytes column from string to integer
 * Replace "-" with "0"
 * Group the results by resources
 
* Feature 3
 * Convert the **_Time stamp_** so that can be sorted with ascending order
 * For each **_Time stamp_**, add the records count for the 3601th second and decrease the record count for the current second
 * Sort and convert the result back to its original format
 
* Feature 4
 * Create 3 lists for **failure time, failure hosts,** and **block list**
 * When log fail(**401**), count the fails and record the fail intervals
 * When log successfully after 5 min from the last failure, then unblock the host
 * When any host has 3 or more failure records, then append it to block list.

* Extra Feature 5:   
Identified the top 10 hosts which use the bandwidth the most.
 * Convert the Bytes column from string to integer
 * Replace "-" with "0"
 * Group the results by hosts
 
## Structure: 

    ├── run.sh
    ├── src
    │   └── process_log.py
    ├── log_input
    │   └── log.txt
    ├── log_output
    |   └── hosts.txt
    |   └── hours.txt
    |   └── resources.txt
    |   └── blocked.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_features
            |   ├── log_input
            |   │   └── log.txt
            |   |__ log_output
            |   │   └── hosts.txt
            |   │   └── hours.txt
            |   │   └── resources.txt
            |   │   └── blocked.txt
            ├── your-own-test
                ├── log_input
                │   └── your-own-log.txt
                |__ log_output
                    └── hosts.txt
                    └── hours.txt
                    └── resources.txt
                    └── blocked.txt


