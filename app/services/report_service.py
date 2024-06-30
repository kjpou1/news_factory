import asyncio
import logging

import aiofiles

from app.config.config import Config

# Initialize the logger for this module
logger = logging.getLogger(__name__)


class ReportService:

    @staticmethod
    def load_template():
        """
        Load the HTML template.

        Returns:
        str: The HTML template as a string.
        """
        config = Config()
        return config.load_template()

    @staticmethod
    def reformat_meta_date_no_repeat(df):
        """
        Reformat the meta_date field and only output on date change without repeating the same date.

        Parameters:
        df (pd.DataFrame): DataFrame containing the meta_date field.

        Returns:
        pd.DataFrame: DataFrame with reformatted meta_date field.
        """
        df['meta_date_reformatted'] = ''  # Initialize a new column for reformatted dates
        previous_date = None  # Keep track of the previous date

        for index, row in df.iterrows():
            current_date = row['meta_date']
            if current_date != previous_date:
                # Reformat the date to replace <span> with <br/> and remove </span>
                formatted_date = current_date.replace(
                    '<span>', '<br/>').replace('</span>', '')
                df.at[index, 'meta_date_reformatted'] = formatted_date
                previous_date = current_date  # Update the previous date to the current date

        return df

    @staticmethod
    def select_and_rename_fields(df):
        """
        Select and rename specific fields for the HTML report.

        Parameters:
        df (pd.DataFrame): DataFrame to be processed.

        Returns:
        pd.DataFrame: DataFrame with selected and renamed fields.
        """
        # Select specific fields to display
        fields = ['meta_date_reformatted', 'event_time_local',
                  'currency', 'name', 'forecast', 'previous', 'impactClass']
        df = df[fields]

        # Rename the selected fields
        rename_dict = {'meta_date_reformatted': 'Event Date', 'event_time_local': 'Time',
                       'currency': 'Currency', 'name': 'Title', 'forecast': 'Forecast',
                       'previous': 'Previous', 'impactClass': 'Impact'}
        df = df.rename(columns=rename_dict)

        return df

    @staticmethod
    def generate_html_with_colors(df):
        """
        Generate HTML with custom CSS styling and row colors based on impactClass.

        Parameters:
        df (pd.DataFrame): DataFrame to be converted to HTML.

        Returns:
        str: HTML string with custom CSS styling and conditional row colors.
        """
        html = '<table>\n'
        html += '  <thead>\n    <tr>\n'
        for col in df.columns[:-1]:  # Exclude impactClass from header
            html += f'      <th>{col}</th>\n'
        html += '    </tr>\n  </thead>\n  <tbody>\n'

        for _, row in df.iterrows():
            impact_class = row['Impact']
            html += f'    <tr class="{impact_class}">\n'
            for col in df.columns[:-1]:  # Exclude impactClass from data rows
                html += f'      <td>{row[col]}</td>\n'
            html += '    </tr>\n'

        html += '  </tbody>\n</table>'
        return html

    @staticmethod
    async def write_html_report_from_dataframe_async(dataframe, file_path, repeat_date=False, encoding='utf-8', report_name="Report"):
        """
        Generate an HTML report from a pandas DataFrame and save it to a file (asynchronous).

        Parameters:
        dataframe (pd.DataFrame): DataFrame to be converted to an HTML report.
        file_path (str): The path of the file where the HTML report will be saved.
        repeat_date (bool): Whether to repeat the date or not. Default is False.
        encoding (str): The encoding format.
        report_name (str): The name of the report to be inserted in the HTML template.
        """
        if 'event_time_local' not in dataframe.columns:
            logger.warning(
                "DataFrame does not contain 'event_time_local' column. Skipping HTML report generation.")
            return -1

        if not repeat_date:
            dataframe = ReportService.reformat_meta_date_no_repeat(dataframe)
        dataframe = ReportService.select_and_rename_fields(dataframe)
        table_html = ReportService.generate_html_with_colors(dataframe)

        # Load the HTML template
        template_content = ReportService.load_template()

        if not template_content:
            logger.error("Invalid template content")
            return -1

        # Replace placeholders with actual content
        html_content = template_content.replace(
            '{{event_title}}', report_name).replace('{{event_table}}', table_html)

        try:
            # Open the file asynchronously and write the HTML content
            async with aiofiles.open(file_path, 'w', encoding=encoding) as html_file:
                await html_file.write(html_content)
            logger.info(
                "Successfully generated HTML report from DataFrame to %s", file_path)
        except Exception as e:
            logger.error("Error generating HTML report from DataFrame: %s", e)
            return -1

        return 0

    @staticmethod
    def write_html_report_from_dataframe(dataframe, file_path, repeat_date=False, encoding='utf-8', report_name="Report"):
        """
        Generate an HTML report from a pandas DataFrame and save it to a file (synchronous).

        Parameters:
        dataframe (pd.DataFrame): DataFrame to be converted to an HTML report.
        file_path (str): The path of the file where the HTML report will be saved.
        repeat_date (bool): Whether to repeat the date or not. Default is False.
        encoding (str): The encoding format.
        report_name (str): The name of the report to be inserted in the HTML template.
        """
        asyncio.run(ReportService.write_html_report_from_dataframe_async(
            dataframe, file_path, repeat_date, encoding, report_name))
