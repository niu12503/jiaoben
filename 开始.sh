#!/bin/bash

# Prompt the user to input the number of times to run the program
echo -n "输入运行次数: "
read times

# Check if the input is a valid positive integer
if ! [[ $times =~ ^[1-9][0-9]*$ ]]; then
    echo "Invalid input. Please enter a positive integer."
    exit 1
fi

# Run the program according to the user input
for ((i = 1; i <= times; i++)); do
    sleep_time=$((($i - 1) * 5))  # Calculate the sleep time based on the iteration
    sleep $sleep_time  # Wait for the calculated sleep time
    screen -dmS test bash -c "挖矿程序.sh"  # Run the program
done
