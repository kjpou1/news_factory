from dataclasses import dataclass

from app.models.currencies import Currencies
from app.models.impact_class import ImpactClass
from app.models.time_period import TimePeriod


@dataclass
class CommandLineArgs:
    impact_classes: list[ImpactClass]
    currencies: list[Currencies]
    time_period: TimePeriod
    output_folder: str
    nnfx: bool
    custom_nnfx_filters: str
    custom_calendar_template: str
    start_date: str = None  
    end_date: str = None    

    def __post_init__(self):
        if self.time_period == TimePeriod.CUSTOM:
            if not self.start_date or not self.end_date:
                raise ValueError("Start date and end date must be provided for custom time period")
            self.start_date = TimePeriod.validate_date_format(self.start_date)
            self.end_date = TimePeriod.validate_date_format(self.end_date)    
