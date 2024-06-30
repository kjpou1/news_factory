from datetime import datetime

import pandas as pd

from app.config.config import Config
from app.services import DataService


class AnalyzeService:

    SELECTED_FIELDS = [
        'meta_date', 'date', 'country', 'currency', 'impactClass',
        'impactTitle', 'name', 'trimmedPrefixedName', 'dateline', 'forecast', 'previous'
    ]

    @staticmethod
    def clean_data(data):
        """
            Cleans the provided DataFrame by selecting specific fields to display.

            Parameters:
            data (pd.DataFrame): The input DataFrame to be cleaned.

            Returns:
            pd.DataFrame: A cleaned DataFrame containing only the selected fields.
            """
        # right now we just select columns
        selected_fields_data = data[AnalyzeService.SELECTED_FIELDS]

        # Detect the local time zone
        # local_timezone = pytz.timezone()  # Example timezone, replace with detection logic if needed
        local_timezone = datetime.now().astimezone().tzinfo

        # Avoiding the SettingWithCopyWarning by creating a new DataFrame for the operation
        selected_df_copy = selected_fields_data.copy()

        # Create a new column 'timestamp' from the 'dateline' column, which contains Unix timestamps
        selected_df_copy['timestamp'] = pd.to_datetime(
            selected_df_copy['dateline'], unit='s', utc=True).dt.tz_convert('US/Eastern')
        selected_df_copy['timestamp_local'] = selected_df_copy['timestamp'].dt.tz_convert(
            local_timezone)
        # Create 'event_date' and 'event_time' fields
        selected_df_copy['event_date'] = selected_df_copy['timestamp'].dt.strftime(
            '%Y-%m-%d')
        selected_df_copy['event_time'] = selected_df_copy['timestamp'].dt.time

        # Create 'event_date_local' and 'event_time_local' fields from the 'timestamp'
        selected_df_copy['event_date_local'] = selected_df_copy['timestamp_local'].dt.strftime(
            '%Y-%m-%d')
        selected_df_copy['event_time_local'] = selected_df_copy['timestamp_local'].dt.time

        # Use .loc to safely set the 'date' column to datetime format
        selected_df_copy.loc[:, 'date'] = pd.to_datetime(
            selected_df_copy['date'])

        # Sort the DataFrame by 'date' and 'currency'
        sorted_df = selected_df_copy.sort_values(
            by=['event_date_local', 'event_time_local'])

        return sorted_df

    @staticmethod
    async def analyze_data(days_array):
        """
        Analyzes the provided data by normalizing, cleaning, and optionally filtering it
        based on configuration settings.

        Parameters:
        days_array (list): The raw data to be analyzed.

        Returns:
        pd.DataFrame: The analyzed data.
        """
        config = Config()

        # Normalize events data
        normalized_df = DataService.normalize_events_data(days_array)

        if normalized_df.empty:
            return {'normalized_data': normalized_df}

        # Clean the data frame
        cleaned_df = AnalyzeService.clean_data(normalized_df)

        if cleaned_df.empty:
            return {
                'normalized_data': normalized_df,
                'cleaned_data': cleaned_df
            }

        results = {
            'normalized_data': normalized_df,
            'cleaned_data': cleaned_df
        }

        # Filter the data by impact class and currency
        impact_filters = config.get_impact_filter_list()
        currency_filters = config.get_currency_filter_list()
        if impact_filters and currency_filters:
            impact_currency_criteria = DataService.criteria_by_impacts_and_currencies(
                impact_filters, currency_filters)
            filtered_df = DataService.filter_data(
                cleaned_df, impact_currency_criteria)
            results['filtered_data'] = filtered_df
        else:
            filtered_df = cleaned_df

        if filtered_df.empty:
            return results

        # Optionally filter the data if NNFX filters are provided
        if config.nnfx:
            nnfx_criteria = DataService.criteria_by_currency_and_keywords(
                config.nnfx_filters_dict)
            nnfx_filtered_df = DataService.filter_data(
                filtered_df, nnfx_criteria)
            results['nnfx_filtered_data'] = nnfx_filtered_df

        return results
