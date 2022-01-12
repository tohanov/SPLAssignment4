#!/bin/bash

./zipCommands.sh
mv ID1_ID2.zip testing/
cd testing/
python3 test_assignment.py ID1_ID2.zip example_input/config.txt example_input/orders.txt true_output.txt true_database.db
cd ..
