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

source ./.venv/bin/activate

python ./run_async.py --impact-classes orange,red,gray --time-period 'today' --nnfx --output-folder "$OUTPUT_FOLDER"
python ./run_async.py --impact-classes orange,red,gray --time-period 'this week' --nnfx --output-folder "$OUTPUT_FOLDER"
python ./run_async.py --impact-classes orange,red,gray --time-period 'this month' --nnfx --output-folder "$OUTPUT_FOLDER"

deactivate
