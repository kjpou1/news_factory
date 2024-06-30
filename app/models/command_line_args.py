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
