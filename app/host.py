import asyncio
import logging
import os

from app.config import Config
from app.models import CommandLineArgs
from app.models.time_period import TimePeriod
from app.services import (AnalyzeService, ForexFactoryScraperService,
                          OutputService)
from app.services.report_service import ReportService


class Host:
    def __init__(self, args: CommandLineArgs):
        """
        Initialize the Host class with command line arguments and configuration.

        Parameters:
        args (CommandLineArgs): Command line arguments passed to the script.
        """
        self.args = args
        self.config = Config(custom_nnfx_filters=self.args.custom_nnfx_filters,
                             custom_calendar_template=args.custom_calendar_template)

        # Set filters and time period on the config object
        self.config.set_filters(self.args.impact_classes, self.args.currencies)
        self.config.set_time_period(self.args.time_period)
        self.config.set_nnfx(self.args.nnfx)

        # Set custom dates if specified
        if self.args.time_period == TimePeriod.CUSTOM:
            self.config.set_custom_dates(self.args.start_date, self.args.end_date)

        self.ff_scraper = ForexFactoryScraperService(url=self.config.get_url())
        self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Run the asynchronous run_async method.
        """
        return asyncio.run(self.run_async())

    async def run_async(self):
        """
        Asynchronous method to perform the main logic:
        - Fetch calendar data
        - Write raw data to a JSON file
        - Analyze the data
        - Write analyzed data to JSON files
        """
        self.logger.info("Starting to retrieve calendar data.")

        # Fetch calendar data
        days_array = await self.ff_scraper.get_calendar_async()

        # Write the raw calendar data to a JSON file
        days_output_json = f'calendar_data_{
            TimePeriod.to_file_name_ending(self.config.time_period)}.json'
        days_output_json = os.path.join(
            self.args.output_folder, days_output_json)
        await OutputService.write_json_to_file_async(days_array, days_output_json)
        self.logger.info("Calendar data written to file: %s", days_output_json)

        # Analyze the data
        self.logger.info("Starting to analyze the data.")
        analyzed_data = await AnalyzeService.analyze_data(days_array)

        # Initialize counter for the number of outputs
        json_output_count = 0
        html_output_count = 0

        # Output the analyzed data to JSON files
        for key, df in analyzed_data.items():
            if df is not None:
                # Write analyzed data to a JSON file
                output_file_json = f'calendar_data_{
                    TimePeriod.to_file_name_ending(self.config.time_period)}_{key}.json'
                output_path_json = os.path.join(
                    self.args.output_folder, output_file_json)
                await OutputService.write_dataframe_to_json_async(df, output_path_json)
                json_output_count += 1

                # Write analyzed data to an HTML file
                output_file_html = f'calendar_data_{
                    TimePeriod.to_file_name_ending(self.config.time_period)}_{key}.html'
                output_path_html = os.path.join(
                    self.args.output_folder, output_file_html)
                html_result = await ReportService.write_html_report_from_dataframe_async(df, output_path_html, repeat_date=False, report_name=f"{
                    TimePeriod.to_file_name_ending(self.config.time_period)} {key} Data")
                html_output_count += 1 if html_result == 0 else 0

        # Print a summary of the outputs
        self.logger.info("Summary: %d JSON files written.", json_output_count)
        self.logger.info("Summary: %d HTML files written.", html_output_count)

# if __name__ == '__main__':
#     # Setup logging configuration
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     )

#     # Example usage, adjust how args are passed in your actual implementation
#     args = CommandLineArgs(
#         impact_classes=[],
#         currencies=[],
#         time_period=TimePeriod.TODAY,
#         output_folder='.',
#         nnfx=False,
#         custom_nnfx_filters=None
#     )
#     host = Host(args)
#     host.run()
