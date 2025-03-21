# NEWS FACTORY

This Python library retrieves calendar event data from Forex Factory for specific time periods. The information is saved in both JSON and HTML formats for further analysis and personal use.

Options are also available to filter by [No Nonsense Forex](https://nononsenseforex.com/forex-basics/forex-news-trading/) rules.

See sister project [news_factory_server](https://github.com/kjpou1/news_factory_server) for serving an icalendar subscriptions.

## Table of Contents

- [NEWS FACTORY](#news-factory)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command Line Arguments](#command-line-arguments)
    - [Examples](#examples)
  - [Configuration](#configuration)
  - [Shell Script](#shell-script)
    - [Shell Script Logging](#shell-script-logging)
    - [Shell Script Examples](#shell-script-examples)
    - [Shell Script Output](#shell-script-output)
    - [Running the Shell Script](#running-the-shell-script)
  - [Task Scheduler](#task-scheduler)
    - [Task Definition (`tasks.json`)](#task-definition-tasksjson)
    - [Schedule Definition (`schedules.json`)](#schedule-definition-schedulesjson)
    - [Running the Scheduler](#running-the-scheduler)
    - [Logging and Environment Info](#logging-and-environment-info)
  - [License](#license)
  - [Disclaimer](#disclaimer)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/kjpou1/news_factory.git
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
<pre>
╔════════════════════════════════════════════════════════════╗
║ Looks like Playwright was just installed or updated.       ║
║ Please run the following command to download new browsers: ║
║                                                            ║
║     playwright install                                     ║
║                                                            ║
║ <3 Playwright Team                                         ║
╚════════════════════════════════════════════════════════════╝
</pre>
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
- `--time-period, -t`: Time period (Tomorrow, Next Week, Next Month, Today, This Week, This Month, Yesterday, Last Week, Last Month, Custom)
- `--output-folder, -o`: Folder where the output files will be saved (default: current directory)
- `--nnfx, -n`: Boolean switch that will filter event data specific to nnfx method
- `--custom-nnfx-filters, -f`: Path to a custom NNFX filters JSON file
- `--custom-calendar-template, -m`: Path to a custom calendar template file
- `--start-date`: Start date for the custom time period (YYYY-MM-DD)
- `--end-date`: End date for the custom time period (YYYY-MM-DD)

> [!NOTE]
> `--nnfx` switch follows the [No Nonsense Forex](https://nononsenseforex.com/forex-basics/forex-news-trading/) news events filtering.

> [!TIP]
> See [resources](./resources) directory of the repo source to see what can be modified.

### Examples

To retrieve and process data for today and save it in the specified output folder:

```bash
python run_async.py --impact-classes orange,red,gray --time-period 'today' --nnfx --output-folder '/path/to/output/folder'
```

```bash
python run_async.py -i orange,red,gray -t 'today' -n -o '/path/to/output/folder'
```

To retrieve and process data `this month` only for `USD` and save it in the specified output folder:

```bash
python run_async.py --impact-classes orange,red,gray --currencies USD --time-period 'This Month' --nnfx --output-folder '/path/to/output/folder'
```


To use a custom NNFX filters file and a custom calendar template:

```bash
python run_async.py --impact-classes orange,red,gray --time-period 'this week' --nnfx --output-folder '/path/to/output/folder' --custom-nnfx-filters 'path/to/nnfx_filters.json' --custom-calendar-template 'path/to/calendar_template.html'
```

To retrieve and process data for a custom date range:

```bash
python run_async.py --impact-classes orange,red,gray --time-period 'custom' --start-date '2024-06-01' --end-date '2024-06-11' --nnfx --output-folder '/path/to/output/folder'
```

```bash
python run_async.py -i orange,red,gray -t 'custom' -o '/path/to/output/folder' --start-date '2024-06-01' --end-date '2024-06-11'
```

## Configuration

The configuration settings are managed through environment variables and can be set in a .env file in the root directory of the project. 
Example .env file:

``` 
BASE_URL = 'https://www.forexfactory.com'
IMPACT_FILTERS = 'yellow,orange,red,gray'
CURRENCY_FILTERS = 'AUD,CAD,CHF,EUR,GBP,JPY,NZD,USD'
NNFX_FILTERS = './resources/nnfx_filters.json'
CALENDAR_TEMPLATE = './resources/calendar_template.html'
```

> [!NOTE]
> An `example_env` file is provided to get started.  Copy the file to `.env` before running:

## Shell Script

A shell script `daily_run.sh` is provided to automate the execution of the script for different time periods.

### Shell Script Logging

The `daily_run.sh` script logs all output to a file called `daily_run.log`. If any errors occur during the execution of the script, the log file will contain detailed information. The script will also halt further execution if any task fails.

**Example usage**:

```bash
./daily_run.sh --output-folder "/path/to/output/folder" --clear
```

**Log file**:

Logs are stored in the `daily_run.log` file. You can inspect the log for details on the execution:

```bash
cat daily_run.log
```

If an error occurs during execution, it will be recorded in the log, and the script will stop further tasks from running.

### Shell Script Examples

Example `daily_run.sh`:

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

### Shell Script Output

The `--output-folder` argument is required for the shell script. This specifies the folder where output files will be saved. If the `--clear` flag is provided, the script will delete all files from the output folder before generating new reports.

**Example usage**:

```bash
./daily_run.sh --output-folder "/path/to/output/folder" --clear
```

Without the `--clear` flag, the script will overwrite existing files but will not clear the folder before running:

```bash
./daily_run.sh --output-folder "/path/to/output/folder"
```

### Running the Shell Script

To run the script and clear the directory before running:

```bash
./daily_run.sh --output-folder "/path/to/output/folder" --clear
```

To run the script without clearing the directory, this will overwrite the files that are already generated:

```bash
./daily_run.sh --output-folder "/path/to/output/folder"
```

Based on your latest updates, here are the additions and modifications for the README to incorporate the recent changes to the task scheduler and configuration of tasks.

## Task Scheduler

This library now supports defining tasks and schedules dynamically using a JSON-based configuration file. This is managed using APScheduler to automatically schedule tasks based on time periods like 'today', 'this week', or 'this month'.

The tasks and schedules are defined in separate JSON files:
- `tasks.json`: Defines the task configuration, including impact classes, currencies, time period, and other optional settings.
- `schedules.json`: Defines the cron-based scheduling for each task.

### Task Definition (`tasks.json`)

The `tasks.json` file contains the configuration for each task. Example structure:

```json
{
  "tasks": [
    {
      "task_name": "Today Task",
      "impact_classes": "orange,red,gray",
      "currencies": "AUD,CAD,CHF,EUR,GBP,JPY,NZD,USD",
      "time_period": "TODAY",
      "output_folder": "./data_files",
      "nnfx": true,
      "custom_nnfx_filters": null,
      "custom_calendar_template": null,
      "start_date": null,
      "end_date": null
    },
    {
      "task_name": "This Week Task",
      "impact_classes": "orange,red,gray",
      "currencies": "AUD,CAD,CHF,EUR,GBP,JPY,NZD,USD",
      "time_period": "THIS_WEEK",
      "output_folder": "./data_files",
      "nnfx": true,
      "custom_nnfx_filters": null,
      "custom_calendar_template": null,
      "start_date": null,
      "end_date": null
    }
  ]
}
```

### Schedule Definition (`schedules.json`)

The `schedules.json` file contains the cron-based schedule for each task. Example structure:

```json
{
  "schedules": [
    {
      "task_name": "Today Task",
      "cron_schedule": {
        "hour": 9,
        "minute": 30
      }
    },
    {
      "task_name": "This Month Task",
      "cron_schedule": {
        "day": "/*1",  /* This day field is commented out and will be ignored */
        "hour": 9,
        "minute": 24
      }
    }
  ]
}
```

> **Special Note:**
> - If a cron field's **value** is prefixed with `/*` (e.g., `"/*1"`), that field will be ignored during schedule processing.
> - This allows you to temporarily disable certain cron fields without removing them from the configuration file.
> - For example, in the above `"This Month Task"`, the `"day": "/*1"` field is ignored, so only the `hour` and `minute` fields will be considered when scheduling.

### Running the Scheduler

To start the scheduler, run the following command:

```bash
python scheduler_script.py
```

This will:
- Load tasks and schedules from their respective JSON files.
- Run each task according to its schedule.
- Ensure tasks are executed one at a time, completing the previous one before starting the next.

The logs will provide detailed information about the tasks being executed and their progress.

### Logging and Environment Info

The scheduler will log system environment variables and information such as:
- UTC and local time when the scheduler starts.
- Relevant environment variables (like `OUTPUT_FOLDER`, `IMPACT_FILTERS`, etc.).

The logs will also capture the execution flow for each task and any potential issues during the task execution.

Would you like to proceed with incorporating this new section into your README?

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


## Disclaimer
> [!CAUTION]
> This project uses web scraping to retrieve data from a commercial website. Please be aware of the following:
> * Respect the Website's Terms of Service: Ensure that your usage of this tool complies with the websites terms of service. Frequent scraping can put undue load on their servers.
> * Responsible Usage: Use this tool responsibly to avoid disrupting the services provided by Forex Factory.
> * Legal Considerations: Be aware of the legal implications of web scraping. This tool is provided for personal use and educational purposes only.
