import pandas as pd


class DataService:
    @staticmethod
    def filter_data(data, criteria):
        """
        Filter data based on given criteria.

        Parameters:
        data (dict or pd.DataFrame): Data to be filtered.
        criteria (function): A function that defines the filtering criteria.

        Returns:
        pd.DataFrame: Filtered data as a DataFrame.
        """
        df = pd.DataFrame(data)
        filtered_df = df[criteria(df)]
        return filtered_df

    @staticmethod
    def normalize_events_data(data):
        """
        Normalize the JSON data to create a DataFrame.

        Parameters:
        data (list): List of JSON objects to be normalized.

        Returns:
        pd.DataFrame: Normalized data as a DataFrame.
        """
        df = pd.json_normalize(data, record_path=['events'], meta=[
                               'date'], meta_prefix='meta_')
        return df

    # Define the function to filter data based on impacts and/or currencies
    @staticmethod
    def criteria_by_impacts_and_currenciess(df, impacts=None, currencies=None):
        """
        Filter the DataFrame based on the specified impact classes and/or currencies.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the event data.
        impacts (list, optional): A list of impact classes to filter by. Defaults to None.
        currencies (list, optional): A list of currencies to filter by. Defaults to None.

        Returns:
        pd.DataFrame: The filtered DataFrame.
        """
        if impacts is not None and currencies is not None:
            return (df['impactClass'].isin(impacts)) & (df['currency'].isin(currencies))
        elif impacts is not None:
            return df['impactClass'].isin(impacts)
        elif currencies is not None:
            return df['currency'].isin(currencies)
        else:
            return df

    @staticmethod
    def criteria_by_impacts_and_currencies(impacts, currencies):
        """
        Create a filtering criteria function based on impact levels and currencies.

        Parameters:
        impacts (list): List of impact levels (enum values).
        currencies (list): List of currencies (enum values).

        Returns:
        function: A function to be used as a criteria for filtering data.
        """
        def criteria(df):
            impact_mask = df['impactClass'].isin(
                impacts) if impacts is not None else False
            currency_mask = df['currency'].isin(
                currencies) if currencies is not None else False
            return impact_mask & currency_mask

        return criteria

    @staticmethod
    def criteria_by_currency_and_keywords(filters):
        """
        Create a filtering criteria function based on currency and keywords.

        Parameters:
        filters (dict): Dictionary with currencies as keys and list of keywords as values.

        Returns:
        function: A function to be used as a criteria for filtering data.
        """
        def criteria(df):
            combined_mask = pd.Series([False] * len(df), index=df.index)
            for currency, keywords in filters.items():
                keyword_regex = '|'.join(keywords)
                currency_mask = (df['currency'] == currency) & (
                    df['name'].str.contains(keyword_regex, case=False, na=False))
                combined_mask = combined_mask | currency_mask
            return combined_mask

        return criteria
