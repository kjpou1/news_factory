# NEWS FACTORY

This Python library retrieves calendar event data from Forex Factory for specific time periods. The information is saved in both JSON and HTML formats for further analysis and personal use.

## Table of Contents

- [NEWS FACTORY](#news-factory)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command Line Arguments](#command-line-arguments)
    - [Examples](#examples)
  - [Configuration](#configuration)
  - [Shell Script](#shell-script)
    - [Shell Script Examples](#shell-script-examples)
    - [Running the Shell Script](#running-the-shell-script)
  - [License](#license)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/news-factory.git
    cd news-factory
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Install playwrite** 

    ```bash
    playwrite --install
    ```

5. **Set environment file**

    Copy or rename the `example_env` file to `.env` before running

    ```bash
    cp example_env .env
    ```

## Usage

To run the library, use the provided `run_async.py` script with appropriate command-line arguments.

### Command Line Arguments

- `--impact-classes, -i`: Comma-separated list of impact classes (yellow, orange, red, gray)
- `--currencies, -c`: Comma-separated list of currencies (AUD, CAD, CHF, EUR, GBP, JPY, NZD, USD)
- `--time-period, -t`: Time period (Tomorrow, Next Week, Next Month, Today, This Week, This Month, Yesterday, Last Week, Last Month)
- `--output-folder, -o`: Folder where the output files will be saved (default: current directory)
- `--nnfx, -n`: Boolean switch that is true if specified and false if not
- `--custom-nnfx-filters, -f`: Path to a custom NNFX filters JSON file
- `--custom-calendar-template, -m`: Path to a custom calendar template file

### Examples

To retrieve and process data for today and save it in the specified output folder:

```bash
python run_async.py --impact-classes orange,red,gray --time-period 'today' --nnfx --output-folder '/path/to/output/folder'
```


To use a custom NNFX filters file and a custom calendar template:

```bash
python run_async.py --impact-classes orange,red,gray --time-period 'this week' --nnfx --output-folder '/path/to/output/folder' --custom-nnfx-filters 'path/to/nnfx_filters.json' --custom-calendar-template 'path/to/calendar_template.html'
```

Note: See `resources` directory of the repo source to see what can be modified.

## Configuration

The configuration settings are managed through environment variables and can be set in a .env file in the root directory of the project. 
Example .env file:

``` 
BASE_URL=https://www.forexfactory.com
CURRENCY_FILTERS=AUD,CAD,CHF,EUR,GBP,JPY,NZD,USD
IMPACT_FILTERS=yellow,orange,red,gray
NNFX_FILTERS=nnfx_filters.json
CALENDAR_TEMPLATE=calendar_template.html
```

Note: An example_env file is provided to get started.  Copy the file to `.env` before running:

## Shell Script

A shell script daily_run.sh is provided to automate the execution of the script for different time periods.

### Shell Script Examples

Example `daily_run.sh`

```bash
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

```

### Running the Shell Script

To run the script and clear the directory before running:

```bash
python run_async.py --impact-classes orange,red,gray --time-period 'this week' --nnfx --output-folder '/path/to/output/folder' --custom-nnfx-filters 'path/to/nnfx_filters.json' --custom-calendar-template 'path/to/calendar_template.html'
```

To run the script without clearing the directory, this will overwrite the files that are already generated:

```bash
./daily_run.sh --output-folder "/path/to/output/folder"
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.