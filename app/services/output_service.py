import asyncio
import json
import logging

import aiofiles
import pandas as pd

from app.encoders.date_time_json_encoder import DateTimeJSONEncoder

# Initialize the logger for this module
logger = logging.getLogger(__name__)


class OutputService:
    @staticmethod
    def write_json_to_file(data, file_path, encoding='utf-8'):
        """
        Write JSON data to a file (synchronous).

        Parameters:
        data (dict): Data to be written to the file.
        file_path (str): The path of the file where data will be written.
        encoding (str): The encoding format.
        """
        asyncio.run(OutputService.write_json_to_file_async(
            data, file_path, encoding))

    @staticmethod
    async def write_json_to_file_async(data, file_path, encoding='utf-8'):
        """
        Write JSON data to a file (asynchronous).

        Parameters:
        data (dict): Data to be written to the file.
        file_path (str): The path of the file where data will be written.
        encoding (str): The encoding format.
        """
        try:
            async with aiofiles.open(file_path, 'w', encoding=encoding) as json_file:
                await json_file.write(json.dumps(data, indent=4))
            logger.info("Successfully wrote JSON data to %s", file_path)
        except Exception as e:
            logger.error("Error writing JSON to file: %s", e)

    @staticmethod
    def generate_html_report_from_json(json_data, file_path, encoding='utf-8'):
        """
        Generate an HTML report from JSON data and save it to a file (synchronous).

        Parameters:
        json_data (dict): JSON data to be converted to an HTML report.
        file_path (str): The path of the file where the HTML report will be saved.
        encoding (str): The encoding format.
        """
        asyncio.run(OutputService.generate_html_report_from_json_async(
            json_data, file_path, encoding))

    @staticmethod
    async def generate_html_report_from_json_async(json_data, file_path, encoding='utf-8'):
        """
        Generate an HTML report from JSON data and save it to a file (asynchronous).

        Parameters:
        json_data (dict): JSON data to be converted to an HTML report.
        file_path (str): The path of the file where the HTML report will be saved.
        encoding (str): The encoding format.
        """
        try:
            df = pd.DataFrame(json_data)
            html_content = df.to_html()
            async with aiofiles.open(file_path, 'w', encoding=encoding) as html_file:
                await html_file.write(html_content)
            logger.info(
                "Successfully generated HTML report from JSON data to %s", file_path)
        except Exception as e:
            logger.error("Error generating HTML report from JSON: %s", e)

    @staticmethod
    def generate_html_report_from_dataframe(dataframe, file_path, encoding='utf-8'):
        """
        Generate an HTML report from a pandas DataFrame and save it to a file (synchronous).

        Parameters:
        dataframe (pd.DataFrame): DataFrame to be converted to an HTML report.
        file_path (str): The path of the file where the HTML report will be saved.
        encoding (str): The encoding format.
        """
        asyncio.run(OutputService.generate_html_report_from_dataframe_async(
            dataframe, file_path, encoding))

    @staticmethod
    async def generate_html_report_from_dataframe_async(dataframe, file_path, encoding='utf-8'):
        """
        Generate an HTML report from a pandas DataFrame and save it to a file (asynchronous).

        Parameters:
        dataframe (pd.DataFrame): DataFrame to be converted to an HTML report.
        file_path (str): The path of the file where the HTML report will be saved.
        encoding (str): The encoding format.
        """
        try:
            html_content = dataframe.to_html()
            async with aiofiles.open(file_path, 'w', encoding=encoding) as html_file:
                await html_file.write(html_content)
            logger.info(
                "Successfully generated HTML report from DataFrame to %s", file_path)
        except Exception as e:
            logger.error("Error generating HTML report from DataFrame: %s", e)

    @staticmethod
    def write_dataframe_to_json(dataframe, file_path, encoding='utf-8'):
        """
        Write a pandas DataFrame to a JSON file (synchronous).

        Parameters:
        dataframe (pd.DataFrame): DataFrame to be written to the file.
        file_path (str): The path of the file where data will be written.
        encoding (str): The encoding format.
        """
        asyncio.run(OutputService.write_dataframe_to_json_async(
            dataframe, file_path, encoding))

    @staticmethod
    async def write_dataframe_to_json_async(dataframe, file_path, encoding='utf-8'):
        """
        Write a pandas DataFrame to a JSON file (asynchronous).

        Parameters:
        dataframe (pd.DataFrame): DataFrame to be written to the file.
        file_path (str): The path of the file where data will be written.
        encoding (str): The encoding format.
        """
        try:
            data = dataframe.to_dict(orient='records')
            async with aiofiles.open(file_path, 'w', encoding=encoding) as json_file:
                await json_file.write(json.dumps(data, indent=4, cls=DateTimeJSONEncoder))
            logger.info(
                "Successfully wrote DataFrame to JSON file %s", file_path)
        except Exception as e:
            logger.error("Error writing DataFrame to JSON file: %s", e)
