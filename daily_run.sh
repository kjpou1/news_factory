#!/bin/bash

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --output-folder|-o) OUTPUT_FOLDER="$2"; shift ;;
        --clear|-c) CLEAR_DIR="yes" ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Check if output folder argument is provided
if [ -z "$OUTPUT_FOLDER" ]; then
  echo "Usage: $0 --output-folder|-o <output-folder> [--clear|-c]"
  exit 1
fi

# Clear the directory if the --clear flag is specified
if [ "$CLEAR_DIR" == "yes" ]; then
  echo "Clearing directory: $OUTPUT_FOLDER"
  rm -rf "$OUTPUT_FOLDER"/*
fi

# Activate the virtual environment
source ./.venv/bin/activate

# Log file for storing script output
LOG_FILE="daily_run.log"

# Function to run Python script and log output
run_task() {
    local time_period=$1
    echo "Running for time period: $time_period" | tee -a "$LOG_FILE"
    python ./run_async.py --impact-classes orange,red,gray --time-period "$time_period" --nnfx --output-folder "$OUTPUT_FOLDER" >> "$LOG_FILE" 2>&1
    
    # Check for errors
    if [ $? -ne 0 ]; then
        echo "Error running task for $time_period. Check $LOG_FILE for details." | tee -a "$LOG_FILE"
        exit 1
    fi
}

# Run the tasks for different time periods
run_task "today"
run_task "this week"
run_task "this month"

# Deactivate the virtual environment
deactivate
