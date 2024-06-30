import json
import logging
import os

from dotenv import load_dotenv

from app.helpers import Utils, ResourceLoader
from app.models import SingletonMeta
from app.models.currencies import Currencies
from app.models.impact_class import ImpactClass
from app.models.time_period import TimePeriod


class Config(metaclass=SingletonMeta):

    BASE_URL_KEY = 'BASE_URL'
    CURRENCY_FILTERS_KEY = 'CURRENCY_FILTERS'
    IMPACT_FILTERS_KEY = 'IMPACT_FILTERS'
    NNFX_FILTERS_KEY = 'NNFX_FILTERS'
    CALENDAR_TEMPLATE_KEY = 'CALENDAR_TEMPLATE'
    EXTRA_HTTP_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    _is_initialized = False

    def __init__(self, base_dir=None, custom_nnfx_filters=None, custom_calendar_template=None):
        load_dotenv()  # Load environment variables from .env file
        # Prevent re-initialization
        if not self._is_initialized:
            # Initialize other configuration settings here
            self.base_dir = base_dir
            self.custom_nnfx_filters = custom_nnfx_filters
            self.custom_calendar_template = custom_calendar_template
            self.nnfx = False  # Default value for nnfx
            self._is_initialized = True

        self.impact_filters = [ImpactClass.from_text(
            ic.strip()) for ic in Config.get(
            Config.IMPACT_FILTERS_KEY, '').split(',')] if Config.get(Config.IMPACT_FILTERS_KEY) else []
        self.currency_filters = [Currencies.from_text(
            curr.strip()) for curr in Config.get(
            Config.CURRENCY_FILTERS_KEY, '').split(',')] if Config.get(Config.CURRENCY_FILTERS_KEY) else []
        self.time_period = TimePeriod.TODAY
        # Load NNFX filters from resource file or custom file if specified
        self.nnfx_filters_dict = self.load_nnfx_filters()
        self.logger = logging.getLogger(__name__)

    @classmethod
    def initialize(cls, base_dir):
        # Convenience method to explicitly initialize the Config
        # This method can be expanded to include more initialization parameters if needed
        cls(base_dir=base_dir)

    @staticmethod
    def get(key, default=None):
        return os.getenv(key, default)

    def set_filters(self, impact_classes=None, currencies=None):
        if impact_classes is not None and len(impact_classes) > 0:
            self.impact_filters = impact_classes
        if currencies is not None and len(currencies) > 0:
            self.currency_filters = currencies

    def set_time_period(self, time_period=None):
        if time_period is not None:
            if isinstance(time_period, TimePeriod):
                self.time_period = time_period
            else:
                raise ValueError(f"Invalid TimePeriod value: '{time_period}'")

    def get_href(self):
        return TimePeriod.to_href(self.time_period)

    def get_url(self):
        url = Utils.create_full_url(Config.get(
            Config.BASE_URL_KEY), self.get_href())
        return url

    def get_impact_filter_list(self):
        impact_filters = self.impact_filters
        return [item.value for item in impact_filters] if len(impact_filters) > 0 else None

    def get_currency_filter_list(self):
        currency_filters = self.currency_filters
        return [item.value for item in currency_filters] if len(currency_filters) > 0 else None

    def set_nnfx(self, nnfx):
        self.nnfx = nnfx

    def load_nnfx_filters(self):
        if self.custom_nnfx_filters:
            self.logger.info('Loading custom nnfx filters: %s',
                             self.custom_nnfx_filters)
            filters_content = ResourceLoader.load_resource_file(
                self.custom_nnfx_filters)
        else:
            filters_content = ResourceLoader.load_resource_file_by_key(
                Config.NNFX_FILTERS_KEY)
        try:
            return json.loads(filters_content) if filters_content else {}
        except json.JSONDecodeError:
            self.logger.error("Failed to decode JSON for NNFX filters")
            return {}

    def load_template(self):
        """
        Load the HTML template from the specified file.

        Returns:
        str: The HTML template as a string.
        """
        if self.custom_calendar_template:
            self.logger.info('Loading custom calendar template: %s',
                             self.custom_calendar_template)
            template_content = ResourceLoader.load_resource_file(
                self.custom_calendar_template)
        else:
            template_content = ResourceLoader.load_resource_file_by_key(
                Config.CALENDAR_TEMPLATE_KEY)
        return template_content
