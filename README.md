# Environment

1. Python 3.6.1
2. pandas 0.19.2

### Feature 5: 
Indentified the top 10 hosts which use the bandwidth the most.
 
### Structure: 

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
