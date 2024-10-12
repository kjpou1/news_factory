import json
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import os
from datetime import datetime
import pytz  # Optional, if you need timezone-aware dates.

# Import your existing classes
from app.host import Host
from app.models import CommandLineArgs
from app.models.currencies import Currencies
from app.models.impact_class import ImpactClass
from app.models.time_period import TimePeriod

# Configure the logging to log INFO-level messages and above
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Scheduler:
    def __init__(self, tasks_file='app/data/tasks.json', schedule_file='app/data/schedules.json'):
        """
        Initialize the scheduler with paths to task and schedule configuration files.

        Parameters:
        - tasks_file: Path to the JSON file containing task configurations.
        - schedule_file: Path to the JSON file containing schedule configurations.
        """
        
        # Log environment information at initialization
        self.log_environment_info()        
        
        # Initialize the paths for tasks and schedules JSON files
        self.tasks_file = tasks_file
        self.schedule_file = schedule_file

        # Create an instance of APScheduler's AsyncIOScheduler to manage the scheduling
        self.scheduler = AsyncIOScheduler()

        # Load tasks and schedules from their respective JSON files
        self.tasks = self.load_tasks_from_json(self.tasks_file)
        self.schedules = self.load_schedule_from_json(self.schedule_file)
        
        # Initialize the async lock for controlling task execution order
        self.task_lock = asyncio.Lock()        

    def log_environment_info(self):
        """
        Logs important environment information such as current UTC time, local time, timezone, and environment variables.
        """
        # Get current UTC time and timezone-aware local time
        utc_now = datetime.now(pytz.utc)
        local_now = datetime.now().astimezone()

        # Get the local timezone
        local_timezone = local_now.tzinfo

        # Log environment info
        logger.info(f"Scheduler started at UTC time: {utc_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        logger.info(f"Current local time: {local_now.strftime('%Y-%m-%d %H:%M:%S %Z')} (Timezone: {local_timezone})")
        
        # Log only relevant environment variables
        relevant_env_vars = { 
            'OUTPUT_FOLDER': os.getenv('OUTPUT_FOLDER'),
            'BASE_URL': os.getenv('BASE_URL'),
            'IMPACT_FILTERS': os.getenv('IMPACT_FILTERS'),
            'CURRENCY_FILTERS': os.getenv('CURRENCY_FILTERS'),
            'VIRTUAL_ENV': os.getenv('VIRTUAL_ENV'),
            'VIRTUAL_ENV_PROMPT': os.getenv('VIRTUAL_ENV_PROMPT'),
            'NNFX_FILTERS': os.getenv('NNFX_FILTERS'),
            'CALENDAR_TEMPLATE': os.getenv('CALENDAR_TEMPLATE'),
            'PATH': os.getenv('PATH')
        }
        
        logger.info(f"Relevant environment variables: {relevant_env_vars}")
    
    def load_tasks_from_json(self, task_file):
        """
        Load tasks from a JSON file using utf-8 encoding.

        Parameters:
        - task_file: Path to the task configuration file.

        Returns:
        - A dictionary of tasks.
        """
        try:
            # Open the tasks.json file with utf-8 encoding
            with open(task_file, 'r', encoding='utf-8') as f:
                task_data = json.load(f)
            # Return tasks in a dictionary where task names are the keys
            return {task['task_name']: task for task in task_data['tasks']}
        except Exception as e:
            # Log an error message if the tasks file cannot be loaded
            logger.error(f"Failed to load tasks from {task_file}: {e}")
            return {}

    def load_schedule_from_json(self, schedule_file):
        """
        Load schedules from a JSON file using utf-8 encoding.

        Parameters:
        - schedule_file: Path to the schedule configuration file.

        Returns:
        - A list of schedules.

        Special Note:
        - If a cron field is "commented out" in the JSON using a `/*` prefix, the function will ignore that field.
        - This is not standard JSON behavior, but a special feature of this loader to allow for cron field exclusion.
        """
        try:
            # Open the schedules.json file with utf-8 encoding
            with open(schedule_file, 'r', encoding='utf-8') as f:
                schedule_data = json.load(f)
            
            # Iterate through each schedule to handle any "commented-out" cron fields
            for schedule in schedule_data['schedules']:
                cron_schedule = schedule['cron_schedule']
                
                # Check if any cron field is "commented out" with /*
                # If so, the field is removed from the cron schedule, effectively ignoring it
                for key, value in list(cron_schedule.items()):
                    if isinstance(value, str) and value.startswith('/*'):
                        del cron_schedule[key]  # Remove "commented out" lines

            return schedule_data['schedules']
        except Exception as e:
            # Log an error message if the schedule file cannot be loaded
            logger.error(f"Failed to load schedules from {schedule_file}: {e}")
            return []

    async def run_task(self, task_config):
        async with self.task_lock:
            """
            Asynchronous function to run a task based on its configuration.

            Parameters:
            - task_config: A dictionary containing the task's configuration.
            """
            # Get the time period for the task, or log an error if invalid
            time_period = task_config["time_period"]

            # Process time period
            if time_period:
                time_period = TimePeriod.from_text(time_period.strip())

            if not time_period:
                logger.error(f"Invalid time period: {task_config['time_period']}. Skipping task.")
                return

            if time_period == TimePeriod.CUSTOM:
                if not start_date or not end_date:
                    raise ValueError("Both start-date and end-date must be provided for custom time period")
                start_date = TimePeriod.validate_date_format(start_date)
                end_date = TimePeriod.validate_date_format(end_date)

            # Use environment variable OUTPUT_FOLDER if output_folder is null in task config
            output_folder = task_config.get("output_folder") or os.getenv("OUTPUT_FOLDER", './data_files')

            # Log the usage of the default output folder if applicable
            if not task_config.get("output_folder"):
                logger.info(f"Using default output folder: {output_folder}")
                    
            custom_nnfx_filters = task_config.get("custom_nnfx_filters") or None
            custom_calendar_template = task_config.get("custom_calendar_template") or None  # Handle custom calendar template
            start_date = task_config.get("start_date") or None  # Handle start date if provided
            end_date = task_config.get("end_date") or None  # Handle end date if provided

            impact_classes=task_config["impact_classes"]
            
            # Process impact classes
            if impact_classes:
                impact_classes = [ImpactClass.from_text(
                    ic.strip()) for ic in impact_classes.split(',')]
            else:
                impact_classes = []

            currencies=task_config["currencies"]
            
            # Process currencies
            if currencies:
                currencies = [Currencies.from_text(
                    curr.strip()) for curr in currencies.split(',')]
            else:
                currencies = []

            # Log the start of task execution
            logger.info(f"Starting task: {task_config['task_name']} with output_folder: {output_folder}")

            # Construct command-line arguments dynamically from the task configuration
            args = CommandLineArgs(
                impact_classes=impact_classes,
                currencies=currencies,
                time_period=time_period,
                output_folder=output_folder,
                nnfx=task_config["nnfx"],
                custom_nnfx_filters=custom_nnfx_filters,
                custom_calendar_template=custom_calendar_template,
                start_date=start_date,
                end_date=end_date
            )

            # Create a Host object and execute the task asynchronously
            host = Host(args)
            await host.run_async()

            # Log the completion of task execution
            logger.info(f"Completed task: {task_config['task_name']}")

    def schedule_tasks(self):
        """
        Schedule tasks based on the loaded schedules and tasks.
        """
        for schedule in self.schedules:
            task_name = schedule['task_name']
            cron_schedule = schedule['cron_schedule']

            # Log an error if the task name from the schedule doesn't exist in the tasks
            if task_name not in self.tasks:
                logger.error(f"Task {task_name} not found in tasks.json. Skipping schedule.")
                continue

            task_config = self.tasks[task_name]

            # Schedule the task properly to ensure it runs within an event loop
            self.scheduler.add_job(self.run_async_task, 'cron', args=[task_config], **cron_schedule)
            logger.info(f"Scheduled {task_name} with cron: {cron_schedule}")

    async def run_async_task(self, task_config):
        """
        Asynchronously run the task in the event loop.
        """
        await self.run_task(task_config)
    

    async def start_scheduler(self):
        """
        Start the asynchronous scheduler and keep it running.
        """
        # Start the APScheduler scheduler to begin executing tasks
        self.scheduler.start()

        try:
            # Keep the scheduler running indefinitely by awaiting an infinite loop
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            # Log message when the scheduler is gracefully shutting down
            logger.info("Shutting down the scheduler...")

if __name__ == '__main__':
    # Initialize the scheduler
    scheduler = Scheduler()

    # Schedule the tasks based on the loaded schedules and tasks
    scheduler.schedule_tasks()

    # Start the scheduler in the asyncio event loop
    asyncio.run(scheduler.start_scheduler())
